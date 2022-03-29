from flask import Flask, make_response, request, jsonify,session
from functools import wraps
import jwt


def checkfortoken(func):
    from main import app
    @wraps(func)
    def wrapped(*args,**kwargs):
        token= request.args.get('token')
        if not token:
            return jsonify({'message':'missing token'}),401
        try:
            data=jwt.decode(token,app.config['SECRET_KEY'])
        except:
            return jsonify({'message':'Invalid token'}),401
        return func(*args,**kwargs)
    return wrapped