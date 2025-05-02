import pytest
from app import create_app, db
from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository
from datetime import datetime


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def repo(app):
    with app.app_context():
        return CustomerRepository()


@pytest.fixture
def sample_customer(app):
    with app.app_context():
        customer = Customer(
            name="Test User",
            email="test@example.com",
            phone_number="+1234567890",
            registration_date=datetime.utcnow()
        )
        db.session.add(customer)
        db.session.commit()
        return customer


def test_get_all(app, repo, sample_customer):
    with app.app_context():
        customers = repo.get_all()
        assert len(customers) == 1
        assert customers[0].name == "Test User"
        assert customers[0].email == "test@example.com"


def test_get_by_id(app, repo, sample_customer):
    with app.app_context():
        customer = repo.get_by_id(sample_customer.id)
        assert customer is not None
        assert customer.name == "Test User"
        assert customer.email == "test@example.com"

        # Test non-existent ID
        customer = repo.get_by_id(999)
        assert customer is None


def test_get_by_email(app, repo, sample_customer):
    with app.app_context():
        customer = repo.get_by_email("test@example.com")
        assert customer is not None
        assert customer.name == "Test User"

        # Test non-existent email
        customer = repo.get_by_email("nonexistent@example.com")
        assert customer is None


def test_create(app, repo):
    with app.app_context():
        new_customer = Customer(
            name="New User",
            email="new@example.com",
            phone_number="+9876543210"
        )

        created_customer = repo.create(new_customer)
        assert created_customer is not None
        assert created_customer.id is not None
        assert created_customer.name == "New User"
        assert created_customer.email == "new@example.com"

        # Verify it was added to the database
        found_customer = repo.get_by_email("new@example.com")
        assert found_customer is not None
        assert found_customer.name == "New User"


def test_update(app, repo, sample_customer):
    with app.app_context():
        customer = repo.get_by_id(sample_customer.id)
        customer.name = "Updated Name"
        customer.phone_number = "+5555555555"

        updated_customer = repo.update(customer)
        assert updated_customer is not None
        assert updated_customer.name == "Updated Name"
        assert updated_customer.phone_number == "+5555555555"

        # Verify changes were saved
        fresh_customer = repo.get_by_id(sample_customer.id)
        assert fresh_customer.name == "Updated Name"
        assert fresh_customer.phone_number == "+5555555555"


def test_delete(app, repo, sample_customer):
    with app.app_context():
        # Confirm customer exists
        customer = repo.get_by_id(sample_customer.id)
        assert customer is not None

        # Delete the customer
        result = repo.delete(customer)
        assert result is True

        # Verify customer was deleted
        deleted_customer = repo.get_by_id(sample_customer.id)
        assert deleted_customer is None