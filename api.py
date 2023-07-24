from flask import Flask
from flask_restful import Api, Resource, reqparse
import random
import json

app = Flask("News")
api = Api(app)


class one_news(Resource):
    def get(self, role = ""):
        if role == "director":
            with open('director.json', "r", encoding='utf-8') as fh:
                director_news = json.load(fh)
            return director_news, 200
        if role == "accountant":
            with open('accountant.json', "r", encoding='utf-8') as fh:
                accountant_news = json.load(fh)
            return accountant_news, 200
        if role == "":
            return [random.choice(news)], 200
        return "Role not found", 404

api.add_resource(one_news, "/news", "/news/", "/news/<string:role>") 

if __name__ == '__main__':
    from waitress import serve #
    serve(app, host="127.0.0.1", port=5000) #
    app.run(debug=True)
