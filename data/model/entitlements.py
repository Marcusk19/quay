import logging

from data import model
from data.database import RedHatSubscriptions

logger = logging.getLogger(__name__)


def get_web_customer_id(user_id):
    try:
        query = RedHatSubscriptions.get(RedHatSubscriptions.user_id == user_id).account_number
        return query
    except RedHatSubscriptions.DoesNotExist:
        return None


def save_web_customer_id(user, customer_id):
    try:
        return RedHatSubscriptions.create(user_id=user.id, account_number=customer_id)
    except model.DataModelException as ex:
        logger.error("Problem saving account number for %s: %s", user.username, ex)


def update_web_customer_id(user, customer_id):
    try:
        query = RedHatSubscriptions.update({RedHatSubscriptions.account_number: customer_id}).where(
            RedHatSubscriptions.user_id == user.id
        )
        query.execute()
    except model.DataModelException as ex:
        logger.error("Problem updating customer id for %s: %s", user.username, ex)
