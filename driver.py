import json
import sqlite3
from sqlite3 import Error
from flask import Flask, request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Driver(Resource):
    def get(self):
        return jsonify({'message': 'hello'})

    def post(self, status, delta):
        print(status + ' ' + str(delta))
        sqlconnection = sqlite3.connect('res/driver.sqlite')
        cursor = sqlconnection.cursor()
        cursor.execute("SELECT Count(*) FROM log")
        cursor.execute("INSERT INTO log (status, delta) values (?,?)", (status, delta))
        sqlconnection.commit()

        # TODO delete (testing purposes)
        cursor.execute("SELECT * FROM log")
        print(cursor.fetchall())

        # TODO correct HTTP response
        return 201

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
