from app import db
from models import User

db.create_all()
# insert data
db.session.add(User("1527858909", "michel"))

# commit the changes
db.session.commit()