from app import db
from app.models.customer import Customer
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError


class CustomerRepository:
    @staticmethod
    def get_all() -> List[Customer]:
        """Retrieve all customers from the database"""
        return Customer.query.all()

    @staticmethod
    def get_by_id(customer_id: int) -> Optional[Customer]:
        """Retrieve a customer by ID"""
        return Customer.query.get(customer_id)

    @staticmethod
    def get_by_email(email: str) -> Optional[Customer]:
        """Retrieve a customer by email"""
        return Customer.query.filter_by(email=email).first()

    @staticmethod
    def create(customer: Customer) -> Optional[Customer]:
        """Create a new customer"""
        try:
            db.session.add(customer)
            db.session.commit()
            return customer
        except SQLAlchemyError:
            db.session.rollback()
            return None

    @staticmethod
    def update(customer: Customer) -> Optional[Customer]:
        """Update an existing customer"""
        try:
            db.session.commit()
            return customer
        except SQLAlchemyError:
            db.session.rollback()
            return None

    @staticmethod
    def delete(customer: Customer) -> bool:
        """Delete a customer"""
        try:
            db.session.delete(customer)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False