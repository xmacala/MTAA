import jwt
from functools import wraps
import datetime
from enum import unique
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy, Model
from flask_marshmallow import Marshmallow, Schema
from Models_Controller import address_controller as ac, message_controller as mc, student_controller as sc, user_controller as uc, post_controller as pc
from Models_Controller import conversations_controller as cc
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://adam:''@localhost/studentska_zoznamka'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisissecretkey'
CORS(app)


db = SQLAlchemy(app)
ma = Marshmallow(app)

# Authorization-------------------------------------------------


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        print(token)
        if not token:
            return jsonify({'response': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
        except:
            return jsonify({'response': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated


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


@app.route('/user/create', methods=['POST'])
def user_create():
    return uc.create_user(Users,db,app)


@app.route('/user/login', methods=['POST'])
def user_login():
    return uc.login_user(Users, Students, Address, db, app)


@app.route('/user/get/<id>/', methods=['GET'])
@token_required
def user_get(id):
    return uc.get_user_by_id(Users, user_schema, id)


@app.route('/user/update/<id>/', methods=['PUT'])
@token_required
def user_update(id):
    return uc.update_user(Users, db, id)


@app.route('/user/delete/<id>/', methods=['DELETE'])
@token_required
def user_delete(id):
    return uc.delete_user(Users, Students, Address, Messages, Post, db, id)


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
    age = db.Column(db.Integer())
    bodytype = db.Column(db.String())
    interests = db.Column(db.String())
    file = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, fullname, phonenumber, contacts, height, weight, hobby, haircolor, age, bodytype, interests, file, user_id):
        self.fullname = fullname
        self.phonenumber = phonenumber
        self.contacts = contacts
        self.height = height
        self.weight = weight
        self.hobby = hobby
        self.haircolor = haircolor
        self.age = age
        self.bodytype = bodytype
        self.interests = interests
        self.file = file
        self.user_id = user_id


class StudentsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'fullname', 'phonenumber', 'contacts', 'height', 'weight', 'hobby', 'haircolor', 'age', 'bodytype', 'interests', 'file', 'user_id')


student_schema = StudentsSchema()


@app.route('/student/create/<user_id>/', methods=['POST'])
@token_required
def student_create(user_id):
    return sc.create_student(Students, db, user_id)


@app.route('/student/get/<user_id>/', methods=['GET'])
def student_get(user_id):
    return sc.get_student(Students, student_schema, user_id)


@app.route('/students/get/<user_id>/', methods=['GET'])
def students_get(user_id):
    return sc.get_students(Students, student_schema, user_id)


@app.route('/student/update/data/<user_id>/', methods=['PUT'])
@token_required
def student_data_update(user_id):
    return sc.update_student_data(Students, db, user_id)


@app.route('/student/update/photo/<user_id>/', methods=['PUT'])
@token_required
def student_photo_update(user_id):
    return sc.update_student_photo(Students, db, user_id)


# Addresses section------------------------------------------------
class Address(db.Model):
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


class AddressSchema(ma.Schema):
    class Meta:
        fields = ('id', 'street', 'city', 'postalcode', 'country')


address_schema = AddressSchema()


@app.route('/address/create/<user_id>/', methods=['POST'])
@token_required
def address_add(user_id):
    return ac.create_address(Address, address_schema, db, user_id)


@app.route('/address/get/<user_id>/', methods=['GET'])
def address_get(user_id):
    return ac.get_address(Address, address_schema, user_id)


@app.route('/address/update/<user_id>/', methods=['PUT'])
@token_required
def address_update(user_id):
    return ac.update_address(Address, db, address_schema, user_id)


# Conversation section------------------------------------------------
class Conversations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, user1_id, user2_id):
        self.user1_id = user1_id
        self.user2_id = user2_id


class ConversationsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user1_id', 'user2_id')


conversations_schema = ConversationsSchema()


@app.route('/conversation/create/<user1_id>/<user2_id>/', methods=['POST'])
@token_required
def conversation_create(user1_id, user2_id):
    return cc.create_conversation(Conversations, db, user1_id, user2_id)


@app.route('/conversation/get/<id>/', methods=['GET'])
@token_required
def conversation_get(id):
    return cc.get_conversation(Conversations, db, id)


@app.route('/conversation/delete/<id>/', methods=['DELETE'])
@token_required
def conversation_delete(id):
    return cc.delete_conversation(Conversations, db, id)


# Message section------------------------------------------------
class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sent_at = db.Column(db.DateTime, default=datetime.datetime.now)
    content = db.Column(db.String())
    attachment = db.Column(db.LargeBinary)
    from_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), default=None)

    def __init__(self, content, attachment, from_id, to_id):
        self.content = content
        self.attachment = attachment
        self.from_id = from_id
        self.to_id = to_id


class MessagesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'sent_at', 'content', 'attachment', 'from_id', 'to_id')


messages_schema = MessagesSchema(many=True)


@app.route('/message/create/<from_id>/<to_id>/', methods=['POST'])
@token_required
def message_create(from_id, to_id):
    return mc.create_message(Messages, db, from_id, to_id)


@app.route('/message/get/<from_id>/<to_id>/', methods=['GET'])
def message_get(from_id, to_id):
    return mc.get_message(Messages, messages_schema, from_id, to_id)


@app.route('/message/update/<id>/', methods=['PUT'])
@token_required
def message_update(id):
    return mc.update_message(Messages, db, id)


@app.route('/message/delete/<id>/', methods=['DELETE'])
@token_required
def message_delete(id):
    return mc.delete_message(Messages, db, id)


# Post section------------------------------------------------
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    attachment = db.Column(db.LargeBinary)
    likes = db.Column(db.Integer, default=0)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, attachment, owner_id):
        self.attachment = attachment
        self.owner_id = owner_id


class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'attachment', 'created_at', 'likes')


post_schema = PostSchema()


@app.route('/post/create/<user_id>/', methods=['POST'])
@token_required
def post_create(user_id):
    return pc.create_post(Post, db, user_id)


@app.route('/post/get/<id>/', methods=['GET'])
def post_get(id):
    return pc.get_post(Post, Users, post_schema, id)


@app.route('/posts/get/all', methods=['GET'])
def posts_get_all():
    return pc.get_all_posts(Post, post_schema)


@app.route('/posts/get/<owner_id>/', methods=['GET'])
def posts_get(owner_id):
    return pc.get_posts(Post, post_schema, owner_id)


@app.route('/post/like/<id>/', methods=['PUT'])
@token_required
def post_liked(id):
    return pc.like_post(Post, db, id)


@app.route('/post/update/<id>/', methods=['PUT'])
@token_required
def post_update(id):
    return pc.update_post(Post, db, id)


@app.route('/post/delete/<id>/', methods=['DELETE'])
@token_required
def delete_post(id):
    return pc.delete_post(Post, db, id)


# Main------------------------------------------------------------
if __name__ == "__main__":
    app.run(host='192.168.0.104', port=3000, debug=True)

