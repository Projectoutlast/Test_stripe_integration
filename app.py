from flask import Flask
from flask_restx import Api

from database.base import engine
from database.models import Base
from seller.create_connect_account_api import api as create_connect_account_api
from student.transfer_between_accounts import api as transfer_between_accounts_api


def create_app():

    flask_app = Flask(__name__)
    api = Api(flask_app)

    Base.metadata.create_all(engine)

    stripe_path = "/stripe_account"
    api.add_namespace(create_connect_account_api, stripe_path)
    api.add_namespace(transfer_between_accounts_api, stripe_path)

    return flask_app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
