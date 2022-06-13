import json
import sqlite3
from sqlite3 import Error
from flask import Flask, request, jsonify, Response
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Clock():
    types = ('DRIVE_CLOCK', 'WORK_CLOCK')

    def __init__(self, clock_type):
        if clock_type not in self.types:
            self.clock_type = self.types[0]
            print('Incorrect Clock clock_type provided, defaulting to ' + self.types[0])
        else:
            self.clock_type = clock_type
        self.violationStatus = "OK"
        self.timeValue = 0


DRIVE_CLOCK = Clock("DRIVE_CLOCK")
WORK_CLOCK = Clock("WORK_CLOCK")


class Driver(Resource):
    def __init__(self):
        print("I'VE STARTED")
        # self.drive_clock = Clock("DRIVE_CLOCK")
        # self.work_clock = Clock("WORK_CLOCK")

    def get(self):
        global DRIVE_CLOCK
        global WORK_CLOCK
        resp_json = '{"DRIVE clock":{"hours":"' + str(DRIVE_CLOCK.timeValue) + '","violationStatus":"' \
                    + DRIVE_CLOCK.violationStatus + '"},"WORK clock":{"hours":"' + str(WORK_CLOCK.timeValue) + \
                    '","violationStatus":"' + WORK_CLOCK.violationStatus + '"}}'
        return Response(resp_json, status=200, mimetype='application/json')

    def post(self, status, delta):
        statuses = ('D', 'W', 'OFF')
        try:
            delta_val = float(delta)
        except ValueError:
            return Response("{'error':'bad request'}", status=400, mimetype='application/json')
        if status not in statuses:
            return Response("{'error':'bad request'}", status=400, mimetype='application/json')

        self.log(status, delta_val)

        sqlconnection = sqlite3.connect('res/driver.sqlite')
        with sqlconnection:
            cursor = sqlconnection.cursor()
            cursor.execute("SELECT Count(*) FROM log")
            cursor.execute("INSERT INTO log (status, delta) values (?,?)", (status, delta_val))

            # TODO delete (testing purposes)
            cursor.execute("SELECT * FROM log")
            print(cursor.fetchall())
        # sqlconnection.commit()
        sqlconnection.close()

        return Response("{'success':'true'}", status=201, mimetype='application/json')

    def log(self, status, delta):
        global DRIVE_CLOCK
        if status == "D":
            DRIVE_CLOCK.timeValue += delta
            WORK_CLOCK.timeValue += delta
        elif status == "W":
            WORK_CLOCK.timeValue += delta
        elif status == "OFF":
            WORK_CLOCK.timeValue += delta

            sqlconnection = sqlite3.connect('res/driver.sqlite')
            cursor = sqlconnection.cursor()
            cursor.execute("SELECT * FROM log ORDER BY log_id DESC")
            latest = cursor.fetchall()
            consec = 0
            for row in latest:
                if row[1] == "OFF":
                    consec += row[2]
                else:
                    break
            if consec > 10:
                DRIVE_CLOCK.__init__()
                WORK_CLOCK.__init__()
        self.calculate_status()

    def calculate_status(self):
        global DRIVE_CLOCK
        global WORK_CLOCK
        print(str(DRIVE_CLOCK.timeValue))
        print(str(WORK_CLOCK.timeValue))
        if DRIVE_CLOCK.timeValue > 11:
            DRIVE_CLOCK.violationStatus = "V"
        if WORK_CLOCK.timeValue > 14:
            WORK_CLOCK.violationStatus = "V"


api.add_resource(Driver, '/summary', '/add/<status>&<delta>')
try:
    connection = sqlite3.connect("res/driver.sqlite")
    cur = connection.cursor()
    cur.execute('''
                    CREATE TABLE IF NOT EXISTS log
                    ([log_id] INTEGER PRIMARY KEY, [status] TEXT, [delta] INTEGER)
                    ''')
    connection.close()
except Error as e:
    print(f"sqlite3 error '{e}")

if __name__ == '__main__':
    app.run(debug=True, port=8001)
