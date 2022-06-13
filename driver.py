import json
import sqlite3
from sqlite3 import Error
from flask import Flask, request, jsonify, Response
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Driver(Resource):
    def get(self):
        return jsonify({'message': 'hello'})

    def post(self, status, delta):
        statuses = ('D', 'W', 'OFF')
        try:
            delta_val = int(delta)
        except ValueError:
            return Response("{'error':'bad request'}", status=400, mimetype='application/json')
        if status not in statuses:
            return Response("{'error':'bad request'}", status=400, mimetype='application/json')

        sqlconnection = sqlite3.connect('res/driver.sqlite')
        cursor = sqlconnection.cursor()
        cursor.execute("SELECT Count(*) FROM log")
        cursor.execute("INSERT INTO log (status, delta) values (?,?)", (status, delta_val))
        sqlconnection.commit()

        # TODO delete (testing purposes)
        cursor.execute("SELECT * FROM log")
        print(cursor.fetchall())

        return Response("{'success':'true'}", status=201, mimetype='application/json')

api.add_resource(Driver, '/add/<status>&<delta>')
try:
    connection = sqlite3.connect("res/driver.sqlite")
    cur = connection.cursor()
    cur.execute('''
                    CREATE TABLE IF NOT EXISTS log
                    ([log_id] INTEGER PRIMARY KEY, [status] TEXT, [delta] INTEGER)
                    ''')
except Error as e:
    print(f"sqlite3 error '{e}")

if __name__ == '__main__':
    app.run(debug=True, port=8001)
