"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
import openaq
import requests
from flask import Blueprint

APP = Flask(__name__)




@APP.route('/')
def root():
    """Base view."""

    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter = 'pm25')
    
    aq_data = body['results'][:]
    data = []
    for i in aq_data:
        data.append(i)
        


    return tuple(data)

# @APP.route('/route')
# def get_data():

    


# breakpoint()