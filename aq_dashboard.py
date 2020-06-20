"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
import openaq
import requests
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = openaq.OpenAQ()
status, body = api.measurements(city='Los Angeles', parameter='pm25')
results = body['results']

data = []
data_list = []
for i in results:
    x = i['date']['utc']
    y = i['value']
    data.append(x)
    data_list.append(y)
    merged_list = [(data[k], data_list[k]) for k in range(0, len(data))]


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.String(25))
    value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Record {self.id} {self.datetime}>"

print(merged_list)
print('-------------')
@app.route('/')
def root():
    """Base view."""
    return str(merged_list)

# breakpoint()
print('--------')
@app.route('/refresh', methods=['GET'])
def refresh():
    # breakpoint()
    """Pull fresh data from Open AQ and replace existing data."""
    db.drop_all()
    db.create_all()

    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    # db_id = [i for i in range(1, 101)]
    # db_date = [i[0] for i in merged_list]
    # db_value = [i[1] for i in merged_list]
    for i in merged_list:
        db_date = i[0]
        db_value = i[1]
        # db_airquality.append([db_id, db_date, db_value])
        new_entry = Record(datetime=db_date, value=db_value)
        db.session.add(new_entry)
    # db_airquality = Record(id=db_id, datetime=db_date, value=db_value)

    
   
    db.session.commit()
    return 'Data refreshed!'