from flask import Flask, jsonify
from flask_restplus import Api, Resource, fields
from datetime import datetime


app = Flask(__name__)
api = Api(app,
          version='1.0', title='sudo api',
          description='This api documentation is for test purpose')

# namespaces for api
ns = api.namespace("this is special", description="this is only for special purpose")
home_ns = api.namespace("home_page", description="this is for home page api's")
time_ns = api.namespace("know time", description="this api will used for know time")
login_ns = api.namespace("user login", description="user login api")


@ns.route('/my-resource/<id>', endpoint="test")
@api.doc(params={'id': 'An ID'})
class MyResource(Resource):
    def get(self, id):
        return {"requested id": id, "status": "success"}

    @api.response(403, 'Not Authorized')
    def post(self, id):
        api.abort(403)


@home_ns.route('/home/<user_name>', endpoint="home")
@api.doc(params={'user_name': "A User Name"})
class HomePage(Resource):
    def get(self, user_name):
        user_name = user_name.title()
        return {"status": "success", "message": "welcome {}, to home page".format(user_name)}


@time_ns.route("/get_time", endpoint="time")
# @api.doc()
class TimeCheck(Resource):
    def get(self):
        try:
            cur_date = datetime.now()
            return jsonify({"status": "success", "date": cur_date})
        except Exception as e:
            return {"status": "failure", "Exception": e}


@login_ns.route("/user_login/<int:user_name>", endpoint="login")
@api.doc(params={'user_name': "A User Name this is required"})
class LoginUser(Resource):
    def get(self, user_name):
        try:
            user_name = user_name
            return jsonify({"status": "success", "user_name": user_name})

        except Exception as e:
            return {"status": "failure", "Exception": e}

# test commit
if __name__ == '__main__':
    app.run(debug=True)
