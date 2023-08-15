from faker import Faker

from database.base import session
from database.models import TestCustomer

fake = Faker()

customer_names = [fake.name() for one_step in range(5)]
customer_email = [fake.email() for step in range(5)]

for i in range(5):
    row = TestCustomer(name=customer_names[i], email=customer_email[i])
    session.add(row)

session.commit()
