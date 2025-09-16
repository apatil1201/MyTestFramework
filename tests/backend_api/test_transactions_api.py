import logging
from utils.assertions import assert_status_code, assert_field_in_response
import pytest
LOGGER = logging.getLogger(__name__)


def test_transcation_crud(api_client):
    """
    Test CRUD operations for Transaction
    :param api_client:
    :return:
    """
    endpoint = "/transactions/"
    # Create transaction
    LOGGER.info(f"Create new transaction")
    transaction = {"amount": 212.5, "id": "5", "recipientId": "456", "type": "transfer", "userId": "56"}
    transaction_created = api_client.post(endpoint="/transactions", data=transaction)

    assert_status_code(transaction_created, 201)
    assert_field_in_response(transaction_created, "amount",  value=transaction["amount"])
    LOGGER.info(f"Successfully created new transaction: {transaction_created.json()}")

    # Read transaction
    LOGGER.info(f"Read an existing transaction")
    read_transaction = api_client.get(f"{endpoint}{transaction_created.json()['userId']}")

    assert_status_code(read_transaction, 200)
    assert_field_in_response(read_transaction, "userId", value=transaction_created.json()["userId"])
    LOGGER.info(f"Successfully read latest transaction: {read_transaction.json()[-1]}")

    # Update transaction
    LOGGER.info(f"Update an existing transaction")
    new_amount = "555"
    update_transaction = api_client.put(f"{endpoint}{transaction_created.json()['id']}", {"amount": new_amount})

    assert_status_code(update_transaction, 200)
    assert_field_in_response(update_transaction, "amount", value=new_amount)
    LOGGER.info(f"Successfully updated an existing transaction: {update_transaction.json()} ")

    # Delete transaction
    LOGGER.info(f"Delete an transaction")
    delete_transaction = api_client.delete(f"{endpoint}{transaction_created.json()['id']}")

    assert_status_code(delete_transaction, 200)
    assert_field_in_response(delete_transaction, "message", value='Transaction deleted')
    LOGGER.info(f"Successfull deleted an transaction: {delete_transaction.json()}")


def test_transaction_update_negative_amount(api_client):
    """
    Test negative amount update
    :param api_client:
    :param create_user:
    :return:
    """
    LOGGER.info(f"Create new transaction")
    transaction = {"amount": 212.5, "id": "5", "recipientId": "456", "type": "transfer", "userId": "56"}
    transaction_created = api_client.post(endpoint="/transactions", data=transaction)

    new_amount = "-5.0"
    update_transaction = api_client.put(f"/transactions/{transaction_created.json()['id']}", {"amount": new_amount})
    assert_status_code(update_transaction, 400)