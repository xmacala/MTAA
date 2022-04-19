from flask import Flask, jsonify, request, session, Response
import jwt
import datetime


def create_user(users, db, app):
    try:
        app.config['SECRET_KEY'] = 'thisissecretkey'
        id = request.json['id']
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        exists_name = db.session.query(
            db.session.query(users).filter_by(username=username).exists()
        ).scalar()
        exists_id = db.session.query(
            db.session.query(users).filter_by(id=id).exists()
        ).scalar()
        exists_email = db.session.query(
            db.session.query(users).filter_by(email=email).exists()
        ).scalar()
        if not exists_name and not exists_id and not exists_email:
            token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
                               app.config['SECRET_KEY'])
            user = users(id, username, email, password)
            db.session.add(user)
            db.session.commit()
            return jsonify({'response': 'User successfully created', 'token': token}), 200
        else:
            return jsonify({'response': 'User is already registered'}), 409
    except:
        return jsonify({'response': 'Invalid input'}), 400


def login_user(users, students, address, db, app):
    app.config['SECRET_KEY'] = 'thisissecretkey'
    username = request.json['username']
    password = request.json['password']
    exists_name = db.session.query(
    db.session.query(users).filter_by(username=username).exists()
    ).scalar()
    exists_pass = db.session.query(
    db.session.query(users).filter_by(password=password).exists()
    ).scalar()
    user = users.query.filter_by(username=username).first()
    if exists_name and exists_pass:
        student = students.query.filter_by(user_id=user.id).first()
        adr = address.query.filter_by(user_id=user.id).first()
        if student is not None:
            is_student = True
        else:
            is_student = False
        if adr is not None:
            has_address = True
        else:
            has_address = False
        token = jwt.encode({ 'user' : username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
        return jsonify({'response': 'Login successful', 'token': token, 'id': user.id, 'isStudent': is_student, 'hasAddress': has_address}), 200
    elif exists_name:
        return jsonify({'response': 'Invalid password'}), 400
    else:
        return jsonify({'response': 'User not found'}), 404


def get_user_by_id(users, user_schema, id):
    try:
        user = users.query.get(id)
        if user is not None:
            return user_schema.jsonify(user), 200
        else:
            return jsonify({'response': 'User not found'}), 404
    except:
        return jsonify({'response': 'Invalid ID supplied'}), 400


def update_user(users, db, id):
    user = users.query.get(id)
    if user is not None:
        try:
            username = request.json['username']
            email = request.json['email']
            password = request.json['password']
            user.username = username
            user.email = email
            user.password = password
            db.session.commit()
            return jsonify({'response': 'User data successfully updated'}), 200
        except:
            return jsonify({'response': 'Invalid input'}), 400
    else:
        return jsonify({'response': 'User not found'}), 404


def delete_user(users, students, adress, msg, post, db, id):
    user = users.query.get(id)
    if user is not None:
        student = students.query.filter_by(user_id=id).first()
        adr = adress.query.filter_by(user_id=id).first()
        msg.query.filter(msg.from_id == id).delete()
        post.query.filter(post.owner_id == id).delete()
        if student is not None:
            db.session.delete(student)
        if adr is not None:
            db.session.delete(adr)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'response': 'User successfully deleted'}), 200
    else:
        return jsonify({'response': 'User not found'}), 404

