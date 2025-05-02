from flask import Blueprint
from app.controllers.customer_controller import CustomerController

customer_bp = Blueprint('customer', __name__)
customer_controller = CustomerController()

# Routes for customer CRUD operations
@customer_bp.route('/', methods=['GET'])
def get_all_customers():
    return customer_controller.get_all()

@customer_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    return customer_controller.get_by_id(customer_id)

@customer_bp.route('/', methods=['POST'])
def create_customer():
    return customer_controller.create()

@customer_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    return customer_controller.update(customer_id)

@customer_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    return customer_controller.delete(customer_id)