import stripe

from flask_restx import Namespace, Resource, fields

from config import api_key
from database.base import session
from database.models import StripeConnectAccount, TestCustomer


stripe.api_key = api_key


api = Namespace("Connect account", "Create connect account on Stripe API endpoint")

# RESULT MODEL

get_result_model = api.model("Result model", {
    "account_id": fields.String(),
    "account_type": fields.String(),
    "email": fields.String()
})


# UPDATE PAYLOAD MODEL
date_of_birth_model = api.model("Date of birth", {
    "day": fields.Integer(),
    "month": fields.Integer(),
    "year": fields.Integer()
})

business_profile_model = api.model("Business profile", {
    "industry": fields.String(),
    "product_description": fields.String(),

})

update_payload_model = api.model("Update model", {
    "phone": fields.String(),
    "email": fields.String,
    "business_type": fields.String(),
    "first_name": fields.String(),
    "last_name": fields.String(),
    "dob": fields.Nested(date_of_birth_model),
    "business_profile": fields.Nested(business_profile_model)
})


@api.route('/customer/<int:customer_id>')
class StripeAccount(Resource):
    @api.marshal_with(get_result_model)
    def get(self, customer_id):
        is_account_exist = session.query(
            StripeConnectAccount).where(StripeConnectAccount.customer_id == customer_id).first()
        if is_account_exist:
            stripe_account = stripe.Account.retrieve(is_account_exist.account_id)
            result = {"account_id": stripe_account.id,
                      "account_type": stripe_account.type,
                      "email": stripe_account.email}
            return result, 200
        return {"Message": "No accounts were found"}, 404


@api.route('/customer/<int:customer_id>/create')
class StripeAccountCreate(Resource):
    def post(self, customer_id):
        is_account_exist = session.query(
            StripeConnectAccount).where(StripeConnectAccount.customer_id == customer_id).first()
        if is_account_exist:
            return {"Message": "Account for this user is already exist"}, 409
        is_customer_exist = session.query(TestCustomer).where(TestCustomer.id == customer_id).first()
        if is_customer_exist:
            new_stripe_account = stripe.Account.create(
                type="custom",
                country="US",   # Need or no select country?
                email=is_customer_exist.email,
                capabilities={"card_payments": {"requested": True}, "transfers": {"requested": True}})

            new_db_row = StripeConnectAccount(customer_id=is_customer_exist.id,
                                              account_id=new_stripe_account.stripe_id,
                                              account_email=new_stripe_account.email,
                                              account_status=new_stripe_account.charges_enabled)
            session.add(new_db_row)
            session.commit()
            return new_stripe_account
        return {"Message": f"Customer (Id={customer_id}) does not exist"}, 404


@api.route("/customer/<int:customer_id>/onboard")
class StripeAccountUpdate(Resource):
    def post(self, customer_id):
        stripe_account = session.query(StripeConnectAccount).where(
            StripeConnectAccount.customer_id == customer_id).first()

        if stripe_account:
            new_onboard_link = stripe.AccountLink.create(
                account=stripe_account.account_id,
                refresh_url="https://ya.ru",    # site like pass
                return_url="https://ya.ru",    # site like pass
                type="account_onboarding")
            return new_onboard_link
        return {"Message": f"Account for customer (Id={customer_id}) does not exist"}, 404
