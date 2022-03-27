from flask import Flask, jsonify, request


def create_user(users, user_schema, db):
    id = request.json['id']
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    user = users(id, username, email, password)
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user)


def get_users(users, users_schema):
    all_users = users.query.all()
    results = users_schema.dump(all_users)
    return jsonify(results)


def get_user_by_id(users, user_schema, id):
    user = users.query.get(id)
    return user_schema.jsonify(user)


def update_user(users, db, user_schema, id):
    user = users.query.get(id)
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    user.username = username
    user.email = email
    user.password = password
    db.session.commit()
    return user_schema.jsonify(user)


def delete_user(users, db, user_schema, id):
    user = users.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

