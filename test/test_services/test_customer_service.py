import pytest
from unittest.mock import Mock, patch
from app.services.customer_service import CustomerService
from app.models.customer import Customer


@pytest.fixture
def mock_repository():
    repository = Mock()
    return repository


@pytest.fixture
def service(mock_repository):
    return CustomerService(repository=mock_repository)


@pytest.fixture
def sample_customer():
    return Customer(
        id=1,
        name="Test User",
        email="test@example.com",
        phone_number="+1234567890"
    )


def test_get_all_customers(service, mock_repository, sample_customer):
    # Setup
    mock_repository.get_all.return_value = [sample_customer]

    # Execute
    customers = service.get_all_customers()

    # Assert
    assert len(customers) == 1
    assert customers[0].name == "Test User"
    mock_repository.get_all.assert_called_once()


def test_get_customer_by_id(service, mock_repository, sample_customer):
    # Setup
    mock_repository.get_by_id.return_value = sample_customer

    # Execute
    customer = service.get_customer_by_id(1)

    # Assert
    assert customer is not None
    assert customer.name == "Test User"
    mock_repository.get_by_id.assert_called_once_with(1)

    # Test not found
    mock_repository.get_by_id.return_value = None
    customer = service.get_customer_by_id(999)
    assert customer is None


def test_create_customer_success(service, mock_repository):
    # Setup
    mock_repository.get_by_email.return_value = None

    def mock_create(customer):
        customer.id = 1
        return customer

    mock_repository.create.side_effect = mock_create

    # Execute
    customer_data = {
        'name': 'New User',
        'email': 'new@example.com',
        'phone_number': '+9876543210'
    }

    customer, error = service.create_customer(customer_data)

    # Assert
    assert error is None
    assert customer is not None
    assert customer.name == 'New User'
    assert customer.email == 'new@example.com'
    mock_repository.get_by_email.assert_called_once_with('new@example.com')
    mock_repository.create.assert_called_once()


def test_create_customer_existing_email(service, mock_repository, sample_customer):
    # Setup
    mock_repository.get_by_email.return_value = sample_customer

    # Execute
    customer_data = {
        'name': 'Another User',
        'email': 'test@example.com',  # Same email as sample_customer
        'phone_number': '+9876543210'
    }

    customer, error = service.create_customer(customer_data)

    # Assert
    assert error == "Customer with this email already exists"
    assert customer is None
    mock_repository.get_by_email.assert_called_once_with('test@example.com')
    mock_repository.create.assert_not_called()


def test_update_customer_success(service, mock_repository, sample_customer):
    # Setup
    mock_repository.get_by_id.return_value = sample_customer
    mock_repository.get_by_email.return_value = None
    mock_repository.update.return_value = sample_customer

    # Execute
    customer_data = {
        'name': 'Updated User',
        'phone_number': '+5555555555'
    }

    customer, error = service.update_customer(1, customer_data)

    # Assert
    assert error is None
    assert customer is not None
    assert customer.name == 'Updated User'
    assert customer.phone_number == '+5555555555'
    mock_repository.get_by_id.assert_called_once_with(1)
    mock_repository.update.assert_called_once()


def test_update_customer_not_found(service, mock_repository):
    # Setup
    mock_repository.get_by_id.return_value = None

    # Execute
    customer_data = {
        'name': 'Updated User',
    }

    customer, error = service.update_customer(999, customer_data)

    # Assert
    assert error == "Customer not found"
    assert customer is None
    mock_repository.get_by_id.assert_called_once_with(999)
    mock_repository.update.assert_not_called()


def test_update_customer_email_conflict(service, mock_repository, sample_customer):
    # Setup
    existing_customer = Customer(
        id=2,
        name="Another User",
        email="existing@example.com",
        phone_number="+9999999999"
    )

    mock_repository.get_by_id.return_value = sample_customer
    mock_repository.get_by_email.return_value = existing_customer

    # Execute
    customer_data = {
        'email': 'existing@example.com'  # Email already in use by another customer
    }

    customer, error = service.update_customer(1, customer_data)

    # Assert
    assert error == "Email already in use by another customer"
    assert customer is None
    mock_repository.get_by_id.assert_called_once_with(1)
    mock_repository.get_by_email.assert_called_once_with('existing@example.com')
    mock_repository.update.assert_not_called()


def test_delete_customer_success(service, mock_repository, sample_customer):
    # Setup
    mock_repository.get_by_id.return_value = sample_customer
    mock_repository.delete.return_value = True

    # Execute
    success, error = service.delete_customer(1)

    # Assert
    assert success is True
    assert error is None
    mock_repository.get_by_id.assert_called_once_with(1)
    mock_repository.delete.assert_called_once_with(sample_customer)


def test_delete_customer_not_found(service, mock_repository):
    # Setup
    mock_repository.get_by_id.return_value = None

    # Execute
    success, error = service.delete_customer(999)

    # Assert
    assert success is False
    assert error == "Customer not found"
    mock_repository.get_by_id.assert_called_once_with(999)
    mock_repository.delete.assert_not_called()


def test_delete_customer_failure(service, mock_repository, sample_customer):
    # Setup
    mock_repository.get_by_id.return_value = sample_customer
    mock_repository.delete.return_value = False

    # Execute
    success, error = service.delete_customer(1)

    # Assert
    assert success is False
    assert error == "Failed to delete customer"
    mock_repository.get_by_id.assert_called_once_with(1)
    mock_repository.delete.assert_called_once_with(sample_customer)