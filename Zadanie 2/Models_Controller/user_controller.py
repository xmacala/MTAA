from flask import Flask, jsonify, request

def create_user(Users, user_schema, db):

    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    user = Users(username, email, password)
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user)

def get_users(Users, users_schema):

    all_users = Users.query.all()
    results = users_schema.dump(all_users)
    return jsonify(results)

def get_user_by_id(Users, user_schema, id):

    user = Users.query.get(id)
    return user_schema.jsonify(user)

def update_user(Users, db, user_schema, id):

    user = Users.query.get(id)
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    user.username = username
    user.email = email
    user.password = password
    db.session.commit()
    return user_schema.jsonify(user)

def delete_user(Users, db, user_schema, id):

    user = Users.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

