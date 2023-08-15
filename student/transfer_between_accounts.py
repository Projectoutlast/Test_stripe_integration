import stripe

from flask_restx import Namespace, Resource, fields

from config import api_key
from database.base import session
from database.models import StripeConnectAccount, TestCustomer


stripe.api_key = api_key


api = Namespace("Add money to connect account", "Add money to connect account on Stripe API endpoint")


@api.route("/transfer/<int:sender_id>/<int:recipient_id>")
class StripeAccountTransfer(Resource):
    def post(self, sender_id, recipient_id):
        sender = session.query(StripeConnectAccount).where(StripeConnectAccount.customer_id == sender_id).first()
        recipient = session.query(StripeConnectAccount).where(StripeConnectAccount.customer_id == recipient_id).first()

        transfer_to_platform = stripe.Charge.create(
            amount=10000,
            currency="usd",
            source=sender.account_id)

        transfer_to_recipient = stripe.Transfer.create(
            amount=10000,
            currency="usd",
            destination=recipient.account_id,
            stripe_account="acct_1NcjNZC8rWSQZ9El"
        )
        return '', 200
