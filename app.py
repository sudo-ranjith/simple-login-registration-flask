from flask_jwt_simple import JWTManager, jwt_required, create_jwt 
from flask import Flask , jsonify , request ,render_template , url_for , session , redirect
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_simple import JWTManager, jwt_required, create_jwt, get_jwt_identity


app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'login_registration'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/login_registraion'
app.config['SECRET_KEY'] = 'a5ea0c77491f965420dfa379ddb6105adb0e3e88'
app.config['JWT_SECRET_KEY'] = 'super-secret' 
mongo = PyMongo(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)


@app.route('/register', methods=['POST'])
def register():
    try:
        username = request.json.get('username')
        password = request.json.get('password')  
        mobile = request.json.get('mobile')           
        register_db = mongo.db.login_registration1
        registered_username = register_db.find_one({'username': username})      
        print('check1 and') 
        if registered_username == None:
            print('print part 1')
            pw_hash = bcrypt.generate_password_hash(password)
            # pw_hash=str(pw_hash)
            register_db.insert_one({'username': username , 'password': pw_hash , 'mobile': mobile})
            result_msg = {'msg': 'registered succesfully'}
            return jsonify(result_msg)             
        else:
            print('else part ')
            result_msg = {'msg': 'already exists'}
            return jsonify(result_msg)
    except Exception as e:
        print(e)


@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        our_db = mongo.db.login_registration1
        existing_user = our_db.find_one({'username': username})
        print(existing_user)
        existing_encrypted_password = our_db.find_one({'username': username}, {'password':1 , "_id":0})
        existing_encrypted_password=existing_encrypted_password["password"]
        decrypted_password = bcrypt.check_password_hash(existing_encrypted_password,password)
        print('is it working')
        print(decrypted_password)
        if existing_user==None:
            return jsonify({"msg": "User is not found in the system", "user": existing_user})
        else:
            existing_user_name=existing_user["username"]
            existing_user_password=existing_user["password"]
            # if username == existing_user_name and password == existing_encrypted_password:
            if username == existing_user_name and decrypted_password == True:
                print(existing_user_name , existing_user_name , existing_user_password)
                ret = {'access_token': create_jwt(username)}
                return jsonify(ret), 200
            return jsonify({"msg": "Bad username or password"}), 401
    except Exception as e:
        print(e)


@app.route('/profile', methods=['GET'])
@jwt_required
def profile():
    our_db = mongo.db.login_registration1
    print('welcome to profile page')
    current_user = get_jwt_identity()
    print(current_user)
    user_data_base = our_db.find_one({'username': current_user}, {"_id": 0, "password": 0})
    print(user_data_base)
    return jsonify(user_data_base)


@app.route('/users' , methods=['GET'])
@jwt_required
def users():
    our_db = mongo.db.login_registration1
    
    user_details = our_db.find({}, {'username': 1, '_id': 0}).sort('username')
    user_name = []
    for x in user_details:
        print('this is inside of for loop')
        user_name.append(x)
        print('end forloop')
    print(user_name)
    return jsonify(user_name)


@app.route('/mail_list', methods=['GET'])
@jwt_required
def mail_list():
    db = mongo.db.login_registration1
    user_email_details = db.find({}, {"email": 1, '_id': 0}).sort('email')
    user_email = []
    for y in user_email_details:
        user_email.append(y)
        print(y)
    return jsonify(user_email)


if __name__ == '__main__':
    app.run(debug=True)