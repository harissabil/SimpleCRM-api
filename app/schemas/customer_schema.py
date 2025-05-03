from marshmallow import validate, ValidationError, validates

from app import ma
from app.models.customer import Customer
from app.utils import validate_not_empty, validate_email, validate_phone_number
from app.utils.validators import validate_name_no_numbers


class CustomerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Customer
        load_instance = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True, validate=validate.Length(min=1, max=100))
    email = ma.auto_field(required=True, validate=[
        validate.Length(max=100),
        validate.Email(error="Invalid email format")
    ])
    phone_number = ma.auto_field(required=True, validate=validate.Length(min=10, max=20))
    registration_date = ma.auto_field(dump_only=True)
    created_at = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)

    @validates('name')
    def validate_name(self, value):
        error = validate_not_empty(value, 'Name')
        if error:
            raise ValidationError(error)
        error = validate_name_no_numbers(value)
        if error:
            raise ValidationError(error)

    @validates('email')
    def validate_email_field(self, value):
        error = validate_email(value)
        if error:
            raise ValidationError(error)

    @validates('phone_number')
    def validate_phone_number_field(self, value):
        error = validate_phone_number(value)
        if error:
            raise ValidationError(error)


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
