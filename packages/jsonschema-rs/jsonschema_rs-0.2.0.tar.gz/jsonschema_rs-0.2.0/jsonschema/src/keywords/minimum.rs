use crate::{
    compilation::{CompilationContext, JSONSchema},
    error::{no_error, CompilationError, ErrorIterator, ValidationError},
    keywords::CompilationResult,
    validator::Validate,
};
use num_cmp::NumCmp;
use serde_json::{Map, Value};

pub struct MinimumU64Validator {
    limit: u64,
}
pub struct MinimumI64Validator {
    limit: i64,
}
pub struct MinimumF64Validator {
    limit: f64,
}

macro_rules! validate {
    ($validator: ty) => {
        impl Validate for $validator {
            #[inline]
            fn build_validation_error<'a>(&self, instance: &'a Value) -> ValidationError<'a> {
                #[allow(trivial_numeric_casts)]
                ValidationError::minimum(instance, self.limit as f64)
            }

            fn name(&self) -> String {
                format!("minimum: {}", self.limit)
            }

            #[inline]
            fn is_valid_number(&self, _: &JSONSchema, _: &Value, instance_value: f64) -> bool {
                NumCmp::num_ge(instance_value, self.limit)
            }
            #[inline]
            fn is_valid_signed_integer(
                &self,
                _: &JSONSchema,
                _: &Value,
                instance_value: i64,
            ) -> bool {
                NumCmp::num_ge(instance_value, self.limit)
            }
            #[inline]
            fn is_valid_unsigned_integer(
                &self,
                _: &JSONSchema,
                _: &Value,
                instance_value: u64,
            ) -> bool {
                NumCmp::num_ge(instance_value, self.limit)
            }
            #[inline]
            fn is_valid(&self, schema: &JSONSchema, instance: &Value) -> bool {
                if let Some(instance_value) = instance.as_u64() {
                    self.is_valid_unsigned_integer(schema, instance, instance_value)
                } else if let Some(instance_value) = instance.as_i64() {
                    self.is_valid_signed_integer(schema, instance, instance_value)
                } else if let Some(instance_value) = instance.as_f64() {
                    self.is_valid_number(schema, instance, instance_value)
                } else {
                    true
                }
            }

            #[inline]
            fn validate<'a>(
                &self,
                schema: &'a JSONSchema,
                instance: &'a Value,
            ) -> ErrorIterator<'a> {
                if let Value::Number(instance_number) = instance {
                    if let Some(instance_unsigned_integer) = instance_number.as_u64() {
                        self.validate_unsigned_integer(schema, instance, instance_unsigned_integer)
                    } else if let Some(instance_signed_integer) = instance_number.as_i64() {
                        self.validate_signed_integer(schema, instance, instance_signed_integer)
                    } else {
                        self.validate_number(
                            schema,
                            instance,
                            instance_number
                                .as_f64()
                                .expect("A JSON number will always be representable as f64"),
                        )
                    }
                } else {
                    no_error()
                }
            }
        }
    };
}

validate!(MinimumU64Validator);
validate!(MinimumI64Validator);
validate!(MinimumF64Validator);

#[inline]
pub fn compile(
    _: &Map<String, Value>,
    schema: &Value,
    _: &CompilationContext,
) -> Option<CompilationResult> {
    if let Value::Number(limit) = schema {
        return if let Some(limit) = limit.as_u64() {
            Some(Ok(Box::new(MinimumU64Validator { limit })))
        } else if let Some(limit) = limit.as_i64() {
            Some(Ok(Box::new(MinimumI64Validator { limit })))
        } else {
            let limit = limit.as_f64().expect("Always valid");
            Some(Ok(Box::new(MinimumF64Validator { limit })))
        };
    }
    Some(Err(CompilationError::SchemaError))
}

#[cfg(test)]
mod tests {
    use crate::tests_util;
    use serde_json::{json, Value};
    use test_case::test_case;

    #[test_case(json!({"minimum": 1u64 << 54}), json!(1u64 << 54 - 1))]
    #[test_case(json!({"minimum": 1i64 << 54}), json!(1i64 << 54 - 1))]
    fn is_not_valid(schema: Value, instance: Value) {
        tests_util::is_not_valid(schema, instance)
    }
}
