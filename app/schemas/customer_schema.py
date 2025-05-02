from marshmallow import Schema, fields, validate, ValidationError, validates
from app import ma
from app.models.customer import Customer
import re


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

    @validates('phone_number')
    def validate_phone_number(self, value):
        # Simple phone number validation
        if not re.match(r'^\+?[0-9\s-]{10,20}$', value):
            raise ValidationError('Invalid phone number format')
        return value


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)