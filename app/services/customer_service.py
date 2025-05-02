from app.repositories.customer_repository import CustomerRepository
from app.models.customer import Customer
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime


class CustomerService:
    def __init__(self, repository=None):
        self.repository = repository or CustomerRepository()

    def get_all_customers(self) -> List[Customer]:
        """Get all customers"""
        return self.repository.get_all()

    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        """Get a customer by ID"""
        return self.repository.get_by_id(customer_id)

    def create_customer(self, customer_data: Dict[str, Any]) -> Tuple[Optional[Customer], Optional[str]]:
        """Create a new customer"""
        # Check if email already exists
        existing_customer = self.repository.get_by_email(customer_data['email'])
        if existing_customer:
            return None, "Customer with this email already exists"

        # Create new customer
        try:
            registration_date = customer_data.get('registration_date', datetime.utcnow())
            new_customer = Customer(
                name=customer_data['name'],
                email=customer_data['email'],
                phone_number=customer_data['phone_number'],
                registration_date=registration_date
            )
            created_customer = self.repository.create(new_customer)
            if created_customer:
                return created_customer, None
            return None, "Failed to create customer"
        except Exception as e:
            return None, str(e)

    def update_customer(self, customer_id: int, customer_data: Dict[str, Any]) -> Tuple[
        Optional[Customer], Optional[str]]:
        """Update an existing customer"""
        customer = self.repository.get_by_id(customer_id)
        if not customer:
            return None, "Customer not found"

        # Check if email is being changed and if it already exists
        if 'email' in customer_data and customer_data['email'] != customer.email:
            existing_customer = self.repository.get_by_email(customer_data['email'])
            if existing_customer:
                return None, "Email already in use by another customer"

        # Update customer fields
        try:
            if 'name' in customer_data:
                customer.name = customer_data['name']
            if 'email' in customer_data:
                customer.email = customer_data['email']
            if 'phone_number' in customer_data:
                customer.phone_number = customer_data['phone_number']

            updated_customer = self.repository.update(customer)
            if updated_customer:
                return updated_customer, None
            return None, "Failed to update customer"
        except Exception as e:
            return None, str(e)

    def delete_customer(self, customer_id: int) -> Tuple[bool, Optional[str]]:
        """Delete a customer"""
        customer = self.repository.get_by_id(customer_id)
        if not customer:
            return False, "Customer not found"

        if self.repository.delete(customer):
            return True, None
        return False, "Failed to delete customer"