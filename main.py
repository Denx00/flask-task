from crypt import methods
from enum import unique
from functools import wraps
from flask import Flask, make_response, request, jsonify,session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import abort
import psycopg2
import jwt
import datetime
from model import LoginModel
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:rohan241@localhost/ftask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']="flasktask"
db = SQLAlchemy(app)



from functions import checkfortoken



@app.route('/adduser',methods=['POST'])
def adduser():
    try:
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']

        auth=LoginModel(username=username,email=email,password=password)

        db.session.add(auth)
        db.session.commit()

        return jsonify({'message':'user registered successfully'})
    except:
        return jsonify(error=404,message="can't add user")

@app.route('/updateuser/<string:usernm>',methods=['PUT'])
@checkfortoken
def updateuser(usernm):
    username=request.form['username']
    email=request.form['email']
    password=request.form['password']
    result=LoginModel.query.filter_by(username=usernm).first()

    if not result:
        return jsonify(error=404,text="username doesn't exist, cannot update")
        
    else:
        result.username=username
        result.email=email
        result.password=password
        db.session.add(result)
        db.session.commit()
    return jsonify({'message':'user details updated successfully'})

@app.route('/listusers',methods=['GET'])
def listusers():
    all_users=LoginModel.query.all()
    user_details=[]

    for usr in all_users:
        d={}
        d['sno']=usr.id
        d['username']=usr.username
        d['email']=usr.email
        user_details.append(d)
    return jsonify({'users':user_details})
        
@app.route('/auth')
@checkfortoken
def auth():
    return 'authorized login'        

@app.route('/delete/<string:usernm>',methods=['DELETE'])
@checkfortoken
def deleteuser(usernm):
    try:
        duser=LoginModel.query.filter_by(username=usernm).first()
        db.session.delete(duser)
        db.session.commit()
        
        return jsonify({'message':'user deleted successfully'})
    except:
        return jsonify({'message':'an error has occured'})
    

@app.route('/getuser/<string:usernm>',methods=['GET'])
def getuser(usernm):
    try:
        guser=LoginModel.query.filter_by(username=usernm).first()
        return {'sno':guser.id,'username':guser.username,'email':guser.email}
    except:
        return jsonify(error=404,text='error has occured')

@app.route('/login',methods=['POST'])
def login():
    usernm=request.form['username']
    pwd=request.form['password']
    user_exists=LoginModel.query.filter_by(username=usernm).first()
    if not user_exists:
        return jsonify({'message':"Username doesn't exist"})
    elif user_exists.username==usernm and user_exists.password==pwd:
        session['logged_in']=True
        token=jwt.encode({
            'user':request.form['username'],
            'exp':datetime.datetime.utcnow() + datetime.timedelta(seconds=120)
        },
        app.config['SECRET_KEY'])
        return jsonify({'token':token.decode('utf-8')})
    else:
        return jsonify({'message':"Couldn't generate token"})


       





if __name__=='__main__':
    app.run(debug=True)

