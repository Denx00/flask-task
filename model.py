from flask import Flask, make_response, request, jsonify,session
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()


class LoginModel(db.Model):
    __tablename__='authtable'

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),unique=True)
    email=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(50),nullable=False)

    def __init__(self,username,email,password):
        self.username=username
        self.email=email
        self.password=password

