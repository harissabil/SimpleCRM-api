import pytest
import json
from unittest.mock import Mock, patch
from app import create_app, db
from app.models.customer import Customer
from app.controllers.customer_controller import CustomerController
from app.services.customer_service import CustomerService
from datetime import datetime


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SERVER_NAME": "localhost"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mock_service():
    return Mock(spec=CustomerService)


@pytest.fixture
def controller(mock_service):
    return CustomerController(service=mock_service)


@pytest.fixture
def sample_customer():
    return Customer(
        id=1,
        name="Test User",
        email="test@example.com",
        phone_number="+1234567890",
        registration_date=datetime.utcnow()
    )


def test_get_all(app, client, mock_service, sample_customer, controller):
    # Setup
    mock_service.get_all_customers.return_value = [sample_customer]

    # Execute
    with app.test_request_context():
        response, status_code = controller.get_all()

    # Assert
    response_data = json.loads(response.get_data(as_text=True))
    assert status_code == 200
    assert response_data['success'] is True
    assert len(response_data['data']) == 1
    assert response_data['data'][0]['name'] == "Test User"
    assert response_data['data'][0]['email'] == "test@example.com"
    mock_service.get_all_customers.assert_called_once()


def test_get_by_id_found(app, client, mock_service, sample_customer, controller):
    # Setup
    mock_service.get_customer_by_id.return_value = sample_customer

    # Execute
    with app.test_request_context():
        response, status_code = controller.get_by_id(1)

    # Assert
    response_data = json.loads(response.get_data(as_text=True))
    assert status_code == 200
    assert response_data['success'] is True
    assert response_data['data']['name'] == "Test User"
    assert response_data['data']['email'] == "test@example.com"
    mock_service.get_customer_by_id.assert_called_once_with(1)


def test_get_by_id_not_found(app, client, mock_service, controller):
    # Setup
    mock_service.get_customer_by_id.return_value = None

    # Execute
    with app.test_request_context():
        response, status_code = controller.get_by_id(999)

    # Assert
    response_data = json.loads(response.get_data(as_text=True))
    assert status_code == 404
    assert response_data['success'] is False
    assert response_data['message'] == "Customer not found"
    mock_service.get_customer_by_id.assert_called_once_with(999)


def test_create_success(app, client, mock_service, sample_customer, controller):
    # Setup
    mock_service.create_customer.return_value = (sample_customer, None)

    # Execute
    customer_data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'phone_number': '+1234567890'
    }

    with app.test_request_context(json=customer_data, method='POST'):
        response, status_code = controller.create()

    # Assert
    response_data = json.loads(response.get_data(as_text=True))
    assert status_code == 201
    assert response_data['success'] is True
    assert response_data['message'] == "Customer created successfully"
    assert response_data['data']['name'] == "Test User"
    assert response_data['data']['email'] == "test@example.com"
    mock_service.create_customer.assert_called_once()


def test_create_validation_error(app, client, mock_service, controller):
    # Setup - invalid data (missing required fields)
    customer_data = {
        'name': 'Test User'
        # Missing email and phone_number
    }

    # Execute
    with app.test_request_context(json=customer_data, method='POST'):
        response, status_code = controller.create()

    # Assert
    response_data = json.loads(response.get_data(as_text=True))
    assert status_code == 400
    assert response_data['success'] is False
    assert 'message' in response_data
    assert 'errors' in response_data


def test_create_service_error(app, client, mock_service, controller):
    # Setup
    mock_service.create_customer.return_value = (None, "Email already exists")

    # Execute
    customer_data = {
        'name': 'Test User',
        'email': 'existing@example.com',
        'phone_number': '+1234567890'
    }

    with app.test_request_context(json=customer_data, method='POST'):
        response, status_code = controller.create()

    # Assert
    response_data = json.loads(response.get_data(as_text=True))
    assert status_code == 400
    assert response_data['success'] is False
    assert response_data['message'] == "Email already exists"
    mock_service.create_customer.assert_called_once()


def test_update_success(app, client, mock_service, sample_customer, controller):
    # Setup
    updated_customer = Customer(
        id=1,
        name="Updated User",
        email="test@example.com",
        phone_number="+5555555555",
        registration_date=datetime.utcnow()
    )
    mock_service.get_customer_by_id.return_value = sample_customer
    mock_service.update_customer.return_value = (updated_customer, None)

    # Execute
    customer_data = {
        'name': 'Updated User',
        'phone_number': '+5555555555'
    }

    with app.test_request_context(json=customer_data, method='PUT'):
        response, status_code = controller.update(1)

    # Assert
    response_data = json.loads(response.get_data(as_text=True))
    assert status_code == 200
    assert response_data['success'] is True
    assert response_data['message'] == "Customer updated successfully"
    assert response_data['data']['name'] == "Updated User"
    assert response_data['data']['phone_number'] == "+5555555555"
    mock_service.get_customer_by_id.assert_called_once_with(1)
    mock_service.update_customer.assert_called_once()


def test_update_not_found(app, client, mock_service, controller):
    # Setup
    mock_service.get_customer_by_id.return_value = None

    # Execute
    customer_data = {
        'name': 'Updated User',
    }

    with app.test_request_context(json=customer_data, method='PUT'):
        response, status_code = controller.update(999)

    # Assert
    response_data = json.loads(response.get_data(as_text=True))
    assert status_code == 404
    assert response_data['success'] is False
    assert response_data['message'] == "Customer not found"
    mock_service.get_customer_by_id.assert_called_once_with(999)
    mock_service.update_customer.assert_not_called()


def test_delete_success(app, client, mock_service, controller):
    # Setup
    mock_service.delete_customer.return_value = (True, None)

    # Execute
    with app.test_request_context(method='DELETE'):
        response, status_code = controller.delete(1)

    # Assert
    response_data = json.loads(response.get_data(as_text=True))
    assert status_code == 200
    assert response_data['success'] is True
    assert response_data['message'] == "Customer deleted successfully"
    mock_service.delete_customer.assert_called_once_with(1)


def test_delete_not_found(app, client, mock_service, controller):
    # Setup
    mock_service.delete_customer.return_value = (False, "Customer not found")

    # Execute
    with app.test_request_context(method='DELETE'):
        response, status_code = controller.delete(999)

    # Assert
    response_data = json.loads(response.get_data(as_text=True))
    assert status_code == 404
    assert response_data['success'] is False
    assert response_data['message'] == "Customer not found"
    mock_service.delete_customer.assert_called_once_with(999)