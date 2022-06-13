# Driver API

### Overview

This is a simple API created in Python3 using Flask and Flask-RESTful. It features two REST-ful endpoints for storing and retrieving information. The API houses clocking information for a driver, including time driving, working, and off the clock. 

### Dependencies

    pip install flask
    pip install flask-restful

### Using the API
It is recommended that you use an API platform, such as Postman, as browsers tend to not play nice with POST requests. Here is a link to the Postman API client: https://www.postman.com/downloads/

#### Requests

1. Start the API from the command line

    python driver.py

2. Use the following request formats:
    1. POST requests:

    http://localhost:8001/add/TYPE&DELTA
    where TYPE is D (Drive), W (Work), or OFF
    and DELTA is the time spent in that status

    2. GET requests:

    http://localhost:8001/summary

#### Responses

Successful POST requests will return a 201 status code with a response body of {'success':'true'}.

Successful GET requests will return a 200 status code, with a JSON response body featuring current Clock information. For example, the following JSON might be returned upon a GET request **after** a 2-hour drive entry, 1-hour work entry, and 11-hour off entry. 

    {"DRIVE clock":{"hours":"0","violationStatus":"OK"},"WORK clock":{"hours":"0","violationStatus":"OK"}}

### Testing

A testing suite has been created to run in the Postman client. Collections of tests are in the Driver\tests folder. The following test collections have been created:

1. **Bad Requests** - tests that bad requests (where TYPE and DELTA params are not of the correct type/format) return 400 status codes.
2. **Example(1-4)** - test collections based on the example responses from the homework document
3. **Multiple Off requests** - collection featuring separated time-off POST requests, checking that both clocks (DRIVE_CLOCK and WORK_CLOCK) were reset to 0 upon consecutive >10 hours of time off.

