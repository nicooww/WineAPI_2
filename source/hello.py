#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, request
from flask_restful import reqparse, Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'helle': 'werld'}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('code')
        args = parser.parse_args(strict=True)
        print (args)
        return {'codeReceived': 'ok'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
