//! Schema compilation.
//! The main idea is to compile the input JSON Schema to a validators tree that will contain
//! everything needed to perform such validation in runtime.
use crate::{
    error::{CompilationError, ErrorIterator},
    keywords,
    keywords::Validators,
    resolver::Resolver,
    schemas,
};
use serde_json::Value;
use std::borrow::Cow;
use url::{ParseError, Url};

pub const DEFAULT_ROOT_URL: &str = "json-schema:///";

/// The structure that holds a JSON Schema compiled into a validation tree
#[derive(Debug)]
pub struct JSONSchema<'a> {
    pub(crate) draft: schemas::Draft,
    pub(crate) schema: &'a Value,
    pub(crate) validators: Validators,
    pub(crate) resolver: Resolver<'a>,
}

lazy_static::lazy_static! {
    pub static ref DEFAULT_SCOPE: Url = url::Url::parse(DEFAULT_ROOT_URL).expect("Is a valid URL");
}

impl<'a> JSONSchema<'a> {
    /// Compile the input schema into a validation tree
    pub fn compile(
        schema: &'a Value,
        draft: Option<schemas::Draft>,
    ) -> Result<JSONSchema<'a>, CompilationError> {
        // Draft is detected in the following precedence order:
        //   - Explicitly specified;
        //   - $schema field in the document;
        //   - Draft7;
        let draft = draft.unwrap_or_else(|| {
            schemas::draft_from_schema(schema).unwrap_or(schemas::Draft::Draft7)
        });
        let scope = match schemas::id_of(draft, schema) {
            Some(url) => url::Url::parse(url)?,
            None => DEFAULT_SCOPE.clone(),
        };
        let resolver = Resolver::new(draft, &scope, schema)?;
        let context = CompilationContext::new(scope, draft);

        let mut validators = compile_validators(schema, &context)?;
        validators.shrink_to_fit();

        Ok(JSONSchema {
            draft,
            schema,
            resolver,
            validators,
        })
    }

    /// Run validation against `instance` and return an iterator over `ValidationError` in the error case.
    #[inline]
    pub fn validate(&'a self, instance: &'a Value) -> Result<(), ErrorIterator<'a>> {
        let mut errors = self
            .validators
            .iter()
            .flat_map(move |validator| validator.validate(self, instance))
            .peekable();
        if errors.peek().is_none() {
            Ok(())
        } else {
            Err(Box::new(errors))
        }
    }

    /// Run validation against `instance` but return a boolean result instead of an iterator.
    /// It is useful for cases, where it is important to only know the fact if the data is valid or not.
    /// This approach is much faster, than `validate`.
    #[must_use]
    #[inline]
    pub fn is_valid(&self, instance: &Value) -> bool {
        self.validators
            .iter()
            .all(|validator| validator.is_valid(self, instance))
    }
}

/// Context holds information about used draft and current scope.
#[derive(Debug)]
pub struct CompilationContext<'a> {
    pub(crate) scope: Cow<'a, Url>,
    pub(crate) draft: schemas::Draft,
}

impl<'a> CompilationContext<'a> {
    pub(crate) fn new(scope: Url, draft: schemas::Draft) -> Self {
        CompilationContext {
            scope: Cow::Owned(scope),
            draft,
        }
    }

    #[allow(clippy::doc_markdown)]
    /// Push a new scope. All URLs built from the new context will have this scope in them.
    /// Before push:
    ///    scope = http://example.com/
    ///    build_url("#/definitions/foo") -> "http://example.com/#/definitions/foo"
    /// After push this schema - {"$id": "folder/", ...}
    ///    scope = http://example.com/folder/
    ///    build_url("#/definitions/foo") -> "http://example.com/folder/#/definitions/foo"
    ///
    /// In other words it keeps track of sub-folders during compilation.
    #[inline]
    pub(crate) fn push(&'a self, schema: &Value) -> Result<Self, ParseError> {
        if let Some(id) = schemas::id_of(self.draft, schema) {
            let scope = Url::options().base_url(Some(&self.scope)).parse(id)?;
            Ok(CompilationContext {
                scope: Cow::Owned(scope),
                draft: self.draft,
            })
        } else {
            Ok(CompilationContext {
                scope: Cow::Borrowed(self.scope.as_ref()),
                draft: self.draft,
            })
        }
    }

    /// Build a new URL. Used for `ref` compilation to keep their full paths.
    pub(crate) fn build_url(&self, reference: &str) -> Result<Url, ParseError> {
        Url::options().base_url(Some(&self.scope)).parse(reference)
    }
}

/// Compile JSON schema into a tree of validators.
#[inline]
pub fn compile_validators(
    schema: &Value,
    context: &CompilationContext,
) -> Result<Validators, CompilationError> {
    let context = context.push(schema)?;
    match schema {
        Value::Bool(value) => Ok(vec![
            keywords::boolean::compile(*value).expect("Should always compile")?
        ]),
        Value::Object(object) => {
            if let Some(reference) = object.get("$ref") {
                if let Value::String(reference) = reference {
                    Ok(vec![keywords::ref_::compile(schema, reference, &context)
                        .expect("Should always return Some")?])
                } else {
                    Err(CompilationError::SchemaError)
                }
            } else {
                let mut validators = Vec::with_capacity(object.len());
                for (keyword, subschema) in object {
                    if let Some(compilation_func) = context.draft.get_validator(keyword) {
                        if let Some(validator) = compilation_func(object, subschema, &context) {
                            validators.push(validator?)
                        }
                    }
                }
                Ok(validators)
            }
        }
        _ => Err(CompilationError::SchemaError),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::error::ValidationError;
    use serde_json::*;
    use std::{borrow::Cow, fs::File, io::Read, path::Path};
    use url::Url;

    fn load(path: &str, idx: usize) -> Value {
        let path = Path::new(path);
        let mut file = File::open(&path).unwrap();
        let mut content = String::new();
        file.read_to_string(&mut content).ok().unwrap();
        let data: Value = from_str(&content).unwrap();
        let case = &data.as_array().unwrap()[idx];
        case.get("schema").unwrap().clone()
    }

    #[test]
    fn only_keyword() {
        // When only one keyword is specified
        let schema = json!({"type": "string"});
        let compiled = JSONSchema::compile(&schema, None).unwrap();
        let value1 = json!("AB");
        let value2 = json!(1);
        // And only this validator
        assert_eq!(compiled.validators.len(), 1);
        assert!(compiled.validate(&value1).is_ok());
        assert!(compiled.validate(&value2).is_err());
    }

    #[test]
    fn resolve_ref() {
        let schema = load("tests/suite/tests/draft7/ref.json", 4);
        let compiled = JSONSchema::compile(&schema, None).unwrap();
        let url = Url::parse("json-schema:///#/definitions/a").unwrap();
        if let (resource, Cow::Borrowed(resolved)) = compiled
            .resolver
            .resolve_fragment(schemas::Draft::Draft7, &url, &schema)
            .unwrap()
        {
            assert_eq!(resource, Url::parse("json-schema:///").unwrap());
            assert_eq!(resolved, schema.pointer("/definitions/a").unwrap());
        }
    }

    #[test]
    fn validate_ref() {
        let schema = load("tests/suite/tests/draft7/ref.json", 1);
        let value = json!({"bar": 3});
        let compiled = JSONSchema::compile(&schema, None).unwrap();
        assert!(compiled.validate(&value).is_ok());
        let value = json!({"bar": true});
        assert!(compiled.validate(&value).is_err());
    }

    #[test]
    fn wrong_schema_type() {
        let schema = json!([1]);
        let compiled = JSONSchema::compile(&schema, None);
        assert!(compiled.is_err());
    }

    #[test]
    fn multiple_errors() {
        let schema = json!({"minProperties": 2, "propertyNames": {"minLength": 3}});
        let value = json!({"a": 3});
        let compiled = JSONSchema::compile(&schema, None).unwrap();
        let result = compiled.validate(&value);
        let errors: Vec<ValidationError> = result.unwrap_err().collect();
        assert_eq!(errors.len(), 2);
        assert_eq!(
            errors[0].to_string(),
            r#"{"a":3} has less than 2 properties"#
        );
        assert_eq!(
            errors[1].to_string(),
            r#"'"a"' is shorter than 3 characters"#
        );
    }
}
