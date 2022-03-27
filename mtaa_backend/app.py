import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy, Model
from flask_marshmallow import Marshmallow, Schema
from Models_Controller import adress_controller as ac, message_controller as mc, student_controller as sc, user_controller as uc, post_controller as pc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/studentska_zoznamka'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


# Users section------------------------------------------------
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(), unique = True)
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


@app.route('/user_login', methods=['GET'])        #toto fixnut
def user_login():
    return uc.get_users(Users, users_schema)


@app.route('/user_get/<id>/', methods=['GET'])
def user_get(id):
    return uc.get_user_by_id(Users, users_schema, id)


@app.route('/user_update/<id>/', methods=['PUT'])
def users_update(id):
    return uc.update_user(Users, db, user_schema, id)


@app.route('/user_delete/<id>/', methods=['DELETE'])
def users_delete(id):
    return uc.delete_user(Users, db, user_schema, id)


# Students section------------------------------------------------
class Students(db.Model):
    id = db.Column(db.Integer)
    fullname = db.Column(db.String())
    phonenumber = db.Column(db.String())
    contacts = db.Column(db.String())
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    hobby = db.Column(db.String())
    haircolor = db.Column(db.String())
    bodytype = db.Column(db.String())
    photo = db.Column(db.String())
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True )

    def __init__(self, fullname, phonenumber, contacts, height, weight, hobby, haircolor, bodytype, photo, student_id):
        self.fullname = fullname
        self.phonenumber = phonenumber
        self.contacts = contacts
        self.height = height
        self.weight = weight
        self.hobby = hobby
        self.haircolor = haircolor
        self.bodytype = bodytype
        self.photo = photo
        self.student_id = student_id


class StudentsSchema(ma.Schema):
    class Meta:
        fields = ('id','fullname', 'phonenumber', 'contacts', 'height', 'weight', 'hobby', 'haircolor', 'bodytype', 'photo')


student_schema = StudentsSchema()


@app.route('/student_create/<student_id>/', methods = ['POST'])
def student_add(student_id):
    return sc.create_student(Students ,student_schema,db,student_id)


@app.route('/student_get/<student_id>/', methods = ['GET'])
def student_get(student_id):
    return sc.get_student(Students, student_schema, student_id)


@app.route('/student_update/<id>/', methods = ['PUT'])
def student_update(id):
    return sc.update_student(Students, db, student_schema, id)


# Adresses section------------------------------------------------
class Adress(db.Model):
    id = db.Column(db.Integer)
    street = db.Column(db.String())
    city = db.Column(db.String())
    postalcode = db.Column(db.String())
    country = db.Column(db.String())
    adress_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    def __init__(self, street, city, postalcode, country):
        self.street = street
        self.city = city
        self.postalcode = postalcode
        self.country = country


class AdressSchema(ma.Schema):
    class Meta:
        fields = ('id', 'street', 'city', 'postalcode', 'country')


adress_schema = AdressSchema()


@app.route('/address_create', methods=['POST'])
def address_add():
    return ac.create_adress(Adress, adress_schema, db)


@app.route('/address_get/<address_id>/', methods=['GET'])
def address_get(address_id):
    return ac.get_adress(Adress, adress_schema, address_id)


@app.route('/address_update/<id>/', methods=['PUT'])
def address_update(id):
    return ac.update_adress(Adress, db, adress_schema, id)


# Message section------------------------------------------------
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sent_at = db.Column(db.DateTime, default=datetime.datetime.now)
    # delivered_at = db.Column(db.DateTime)
    content = db.Column(db.String(), default="")
    attachment = db.Column(db.String(), default="")
    from_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, content, attachment, from_id, to_id):
        self.content = content
        self.attachment = attachment
        self.from_id = from_id
        self.to_id = to_id


class MessageSchema(ma.Schema):
    class Meta:
        fields = ('id', 'content', 'attachment', 'from_id', 'to_id')


message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)


@app.route('/message_create/<from_id>/<to_id>/', methods = ['POST'])
def message_add(from_id, to_id):
    return mc.create_message(Message, message_schema, db, from_id, to_id)


@app.route('/message_get/<id>/', methods=['GET'])
def message_get(id):
    return mc.get_message(Message, message_schema, id)


@app.route('/message_update/<id>/', methods=['PUT'])
def message_update(id):
    return mc.update_message(Message, db, message_schema, id)


# Post section------------------------------------------------
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    # delivered_at = db.Column(db.DateTime)                                  #toto je asi blbost
    content = db.Column(db.String(), default="")
    attachment = db.Column(db.String(), default="")
    likes = db.Column(db.Integer, default=0)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, content, attachment):
        self.content = content
        self.attachment = attachment


class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'content', 'attachment', 'likes', 'owner_id')


post_schema = PostSchema()
posts_schema = PostSchema(many=True)


@app.route('/post_create', methods=['POST'])
def post_add():
    return pc.create_post(Post, post_schema, db)


@app.route('/post_get/<id>/', methods=['GET'])
def post_get(id):
    return pc.get_post(Post, post_schema, id)


@app.route('/post_get_all/<owner_id>/', methods=['GET'])              # zmenit querry
def posts_get(owner_id):
    return pc.get_posts(Post, posts_schema, id)


@app.route('/post_update/<id>/', methods=['PUT'])
def post_update(id):
    return pc.post_update(Post, db, post_schema, id)


# Main------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)

