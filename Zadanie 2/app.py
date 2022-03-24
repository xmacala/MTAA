from enum import unique
from weakref import ReferenceType
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy, Model
from flask_marshmallow import Marshmallow, Schema
from Models_Controller import user_controller as uc
from Models_Controller import student_controller as sc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/studentska_zoznamka'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

#Users section------------------------------------------------
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(), unique = True)
    password = db.Column(db.String())

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/user_create', methods = ['POST'])
def User_create():
    return uc.create_user(Users,user_schema,db)

@app.route('/user_login', methods = ['GET'])
def User_login():
    return uc.get_users(Users, users_schema)

@app.route('/user_get/<id>/', methods = ['GET'])
def User_get(id):
    return uc.get_user_by_id(Users, users_schema, id)

@app.route('/user_update/<id>/', methods = ['PUT'])
def Users_update(id):
    return uc.update_user(Users, db, user_schema, id)

@app.route('/user_delete/<id>/', methods = ['DELETE'])
def Users_delete(id):
    return uc.delete_user(Users, db, user_schema, id)

#Students section------------------------------------------------
class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String())
    phonenumber = db.Column(db.String())
    contacts = db.Column(db.String())
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    hobby = db.Column(db.String())
    haircolor = db.Column(db.String())
    bodytype = db.Column(db.String())
    photo = db.Column(db.String())
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self,fullname, phonenumber, contacts, height, weight, hobby, haircolor, bodytype, photo):
        self.fullname = fullname
        self.phonenumber = phonenumber
        self.contacts = contacts
        self.height = height
        self.weight = weight
        self.hobby = hobby
        self.haircolor = haircolor
        self.bodytype = bodytype
        self.photo = photo

class StudentsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'fullname', 'phonenumber', 'contacts', 'height', 'weight', 'hobby', 'haircolor', 'bodytype', 'photo')

student_schema = StudentsSchema()
students_schema = StudentsSchema(many=True)

@app.route('/student_create', methods = ['POST'])
def Student_add():
    return sc.create_student(Users,user_schema,db)

@app.route('/student_get', methods = ['GET'])
def Student_get():
    return sc.get_student(Users, users_schema)

@app.route('/student_update/<id>/', methods = ['PUT'])
def Student_update(id):
    return sc.update_student(Users, db, user_schema, id)

#Main------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)

