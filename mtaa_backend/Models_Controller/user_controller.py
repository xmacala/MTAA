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
        if exists_name and exists_id and exists_email:
            token = jwt.encode({ 'user' : username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'], algorithms="HS256")
            user = users(id, username, email, password)
            db.session.add(user)    
            db.session.commit()
            return jsonify({'token' : token}), 200
        else:
            return Response("{'response':'User is already registered'}", status=400, mimetype='application/json')
    except:
        return Response("{'response':'Invalid input'}", status=400, mimetype='application/json') 


def login_user(users, db, app):
    app.config['SECRET_KEY'] = 'thisissecretkey'
    username = request.json['username']
    password = request.json['password']
    exists_name = db.session.query(
    db.session.query(users).filter_by(username=username).exists()
    ).scalar()
    exists_pass = db.session.query(
    db.session.query(users).filter_by(password=password).exists()
    ).scalar()
    if exists_name and exists_pass:
        token = jwt.encode({ 'user' : username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token}), 200
    elif exists_name:
        return Response("{'response':'Invalid password'}", status=400, mimetype='application/json')
    else:
        return Response("{'response':'User not found'}", status=404, mimetype='application/json') 
    

def get_user_by_id(users, user_schema, id):
    try:
        user = users.query.get(id)
        if user is not None:
            return user_schema.jsonify(user)
        else:
            return Response("{'response':'User not found'}", status=404, mimetype='application/json') 
    except:
        return Response("{'response':'Invalid ID supplied'}", status=400, mimetype='application/json') 


def update_user(users, db, user_schema, id):
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
            return Response("{'response':'Succesfull operation'}", status=200, mimetype='application/json') 
        except:
            return Response("{'response':'Invalid input'}", status=400, mimetype='application/json') 
    else:
        return Response("{'response':'User not found'}", status=404, mimetype='application/json') 


def delete_user(users, students, adress, msg_file, msg_text, post, db, user_schema, id):
    user = users.query.get(id)
    if user is not None:
        student = students.query.filter_by(user_id=id).first()
        adr = adress.query.filter_by(user_id=id).first()
        file = msg_file.query.filter_by(from_id=id).all()
        text = msg_text.query.filter_by(from_id=id).all()
        post = post.query.filter_by(owner_id=id).all()
        if student is not None:
            db.session.delete(student)
        if adr is not None:
            db.session.delete(adr)
        if file is not None:
            db.session.delete(file)
        if text is not None:
            db.session.delete(text)
        if post is not None:
            db.session.delete(post)
        db.session.delete(user)
        db.session.commit()
        return Response("{'response':'Succesfull operation'}", status=200, mimetype='application/json')   
    else:
        return Response("{'response':'User not found'}", status=404, mimetype='application/json')   

