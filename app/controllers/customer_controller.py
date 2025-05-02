from flask import request, jsonify
from app.services.customer_service import CustomerService
from app.schemas.customer_schema import customer_schema, customers_schema
from marshmallow import ValidationError


class CustomerController:
    def __init__(self, service=None):
        self.service = service or CustomerService()

    def get_all(self):
        """Get all customers"""
        customers = self.service.get_all_customers()
        return jsonify({
            'success': True,
            'data': customers_schema.dump(customers)
        }), 200

    def get_by_id(self, customer_id):
        """Get a customer by ID"""
        customer = self.service.get_customer_by_id(customer_id)
        if not customer:
            return jsonify({
                'success': False,
                'message': 'Customer not found'
            }), 404

        return jsonify({
            'success': True,
            'data': customer_schema.dump(customer)
        }), 200

    def create(self):
        """Create a new customer"""
        try:
            # Validate and deserialize input
            json_data = request.get_json()
            if not json_data:
                return jsonify({
                    'success': False,
                    'message': 'No input data provided'
                }), 400

            # Validate incoming data with schema
            customer_data = customer_schema.load(json_data, partial=('id',))

            # Create customer
            customer, error = self.service.create_customer(json_data)
            if error:
                return jsonify({
                    'success': False,
                    'message': error
                }), 400

            return jsonify({
                'success': True,
                'message': 'Customer created successfully',
                'data': customer_schema.dump(customer)
            }), 201

        except ValidationError as err:
            return jsonify({
                'success': False,
                'message': 'Validation error',
                'errors': err.messages
            }), 400

        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500

    def update(self, customer_id):
        """Update an existing customer"""
        try:
            # Check if customer exists
            customer = self.service.get_customer_by_id(customer_id)
            if not customer:
                return jsonify({
                    'success': False,
                    'message': 'Customer not found'
                }), 404

            # Validate and deserialize input
            json_data = request.get_json()
            if not json_data:
                return jsonify({
                    'success': False,
                    'message': 'No input data provided'
                }), 400

            # Validate data with schema
            customer_data = customer_schema.load(json_data, partial=True)

            # Update customer
            updated_customer, error = self.service.update_customer(customer_id, json_data)
            if error:
                return jsonify({
                    'success': False,
                    'message': error
                }), 400

            return jsonify({
                'success': True,
                'message': 'Customer updated successfully',
                'data': customer_schema.dump(updated_customer)
            }), 200

        except ValidationError as err:
            return jsonify({
                'success': False,
                'message': 'Validation error',
                'errors': err.messages
            }), 400

        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500

    def delete(self, customer_id):
        """Delete a customer"""
        success, error = self.service.delete_customer(customer_id)
        if error:
            return jsonify({
                'success': False,
                'message': error
            }), 404 if error == "Customer not found" else 500

        return jsonify({
            'success': True,
            'message': 'Customer deleted successfully'
        }), 200