import datetime
from enum import unique
from fileinput import filename
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy, Model
from flask_marshmallow import Marshmallow, Schema
from Models_Controller import adress_controller as ac, message_controller as mc, student_controller as sc, user_controller as uc, post_controller as pc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/studentska_zoznamka'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)


# Users section-------------------------------------------------
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())

    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/user_create', methods=['POST'])
def user_create():
    return uc.create_user(Users,user_schema,db)


@app.route('/user_login', methods=['GET'])        #toto fixnut / done
def user_login():
    return uc.login_user(Users, db)


@app.route('/user_get/<id>/', methods=['GET'])
def user_get(id):
    return uc.get_user_by_id(Users, user_schema, id)


@app.route('/user_update/<id>/', methods=['PUT'])
def users_update(id):
    return uc.update_user(Users, db, user_schema, id)


@app.route('/user_delete/<id>/', methods=['DELETE'])
def users_delete(id):
    return uc.delete_user(Users, Students, Adress, db, user_schema, id)


# Students section------------------------------------------------
class Students(db.Model):
    id = db.Column(db.Integer, primary_key = True )
    fullname = db.Column(db.String())
    phonenumber = db.Column(db.String())
    contacts = db.Column(db.String())
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    hobby = db.Column(db.String())
    haircolor = db.Column(db.String())
    bodytype = db.Column(db.String())
    filename = db.Column(db.String())
    #file = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, fullname, phonenumber, contacts, height, weight, hobby, haircolor, bodytype, filename, user_id):
        self.fullname = fullname
        self.phonenumber = phonenumber
        self.contacts = contacts
        self.height = height
        self.weight = weight
        self.hobby = hobby
        self.haircolor = haircolor
        self.bodytype = bodytype
        self.filename = filename
        self.user_id = user_id


class StudentsSchema(ma.Schema):
    class Meta:
        fields = ('id','fullname', 'phonenumber', 'contacts', 'height', 'weight', 'hobby', 'haircolor', 'bodytype', 'filename')


student_schema = StudentsSchema()


@app.route('/student_create/<user_id>/', methods = ['POST'])
def student_add(user_id):
    return sc.create_student(Students ,db,user_id)


@app.route('/student_get/<user_id>/', methods = ['GET'])
def student_get(user_id):
    return sc.get_student(Students, student_schema, user_id)


@app.route('/student_data_update/<user_id>/', methods = ['PUT'])
def student_data_update(user_id):
    return sc.update_data_student(Students, db, user_id)
    
@app.route('/student_photo_update/<user_id>/', methods = ['PUT'])
def student_photo_update(user_id):
    return sc.update_photo_student(Students, db, user_id)


# Adresses section------------------------------------------------
class Adress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String())
    city = db.Column(db.String())
    postalcode = db.Column(db.String())
    country = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, street, city, postalcode, country, user_id):
        self.street = street
        self.city = city
        self.postalcode = postalcode
        self.country = country
        self.user_id = user_id


class AdressSchema(ma.Schema):
    class Meta:
        fields = ('id', 'street', 'city', 'postalcode', 'country')


adress_schema = AdressSchema()


@app.route('/address_create/<user_id>/', methods=['POST'])
def address_add(user_id):
    return ac.create_address(Adress, adress_schema, db, user_id)


@app.route('/address_get/<user_id>/', methods=['GET'])
def address_get(user_id):
    return ac.get_address(Adress, adress_schema, user_id)


@app.route('/address_update/<user_id>/', methods=['PUT'])
def address_update(user_id):
    return ac.update_address(Adress, db, adress_schema, user_id)


# Message section------------------------------------------------
class MessageText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sent_at = db.Column(db.DateTime, default=datetime.datetime.now)
    content = db.Column(db.String())
    from_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, content, from_id, to_id):
        self.content = content
        self.from_id = from_id
        self.to_id = to_id


class MessageFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sent_at = db.Column(db.DateTime, default=datetime.datetime.now)
    filename = db.Column(db.String())
    attachment = db.Column(db.LargeBinary)
    from_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, filename, attachment, from_id, to_id):
        self.filename = filename
        self.attachment = attachment
        self.from_id = from_id
        self.to_id = to_id


class MessageTextSchema(ma.Schema):
    class Meta:
        fields = ('id', 'sent_at', 'content', 'from_id', 'to_id')


class MessageFileSchema(ma.Schema):
    class Meta:
        fields = ('id', 'sent_at', 'filename', 'from_id', 'to_id')


message_text_schema = MessageTextSchema(many=True)
message_file_schema = MessageFileSchema(many=True)

#Text part---------------

@app.route('/message_text_create/<from_id>/<to_id>/', methods = ['POST'])
def message_text_add(from_id, to_id):
    return mc.create_message_text(MessageText, db, from_id, to_id)


@app.route('/message_text_get/<from_id>/<to_id>/', methods=['GET'])
def message_text_get(from_id, to_id):
    return mc.get_message_text(MessageText, message_text_schema, from_id, to_id)


@app.route('/message_text_update/<id>/', methods=['PUT'])
def message_text_update(id):
    return mc.update_message_text(MessageText, db, id)

#File part----------

@app.route('/message_file_create/<from_id>/<to_id>/', methods = ['POST'])
def message_file_add(from_id, to_id):
    return mc.create_message_file(MessageFile, db, from_id, to_id)


@app.route('/message_file_get/<from_id>/<to_id>/', methods=['GET'])
def message_file_get(from_id, to_id):
    return mc.get_message_file(MessageFile, message_file_schema, from_id, to_id)


@app.route('/message_file_update/<id>/', methods=['PUT'])
def message_file_update(id):
    return mc.update_message_file(MessageFile, db, id)


# Post section------------------------------------------------
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    filename = db.Column(db.String(), unique=True)
    attachment = db.Column(db.LargeBinary)
    likes = db.Column(db.Integer, default = 0)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, filename, attachment, owner_id):
        self.filename = filename
        self.attachment = attachment
        self.owner_id = owner_id

class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'created_at','filename', 'likes')


post_schema = PostSchema()
posts_schema = PostSchema(many=True)


@app.route('/post_create/<user_id>/', methods=['POST'])
def post_create(user_id):
    return pc.create_post(Post, db, user_id)


@app.route('/post_get/<id>/', methods=['GET'])
def post_get(id):
    return pc.get_post(Post, post_schema, id)


@app.route('/post_get_all/<owner_id>/', methods=['GET'])              
def posts_get(owner_id):
    return pc.get_posts(Post, posts_schema, owner_id)


@app.route('/post_liked/<id>/', methods=['PUT'])
def post_liked(id):
    return pc.post_liked(Post, db, id)


@app.route('/post_update/<id>/', methods=['PUT'])
def post_update(id):
    return pc.post_update(Post, db, id)


@app.route('/post_delete/<id>/', methods=['DELETE'])
def delete_post(id):
    return pc.delete_post(Post, db, id)


# Main------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)

