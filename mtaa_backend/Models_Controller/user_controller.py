from flask import Flask, jsonify, request, session, Response


def create_user(users, user_schema, db):
    try:
        id = request.json['id']
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        user = users(id, username, email, password)
        db.session.add(user)    
        db.session.commit()
        return Response("{'response':'Succesfull operation'}", status=200, mimetype='application/json')
    except:
        return Response("{'response':'Invalid input'}", status=400, mimetype='application/json') 


def login_user(users, db):
    username = request.json['username']
    password = request.json['password']
    exists_name = db.session.query(
    db.session.query(users).filter_by(username=username).exists()
    ).scalar()
    exists_pass = db.session.query(
    db.session.query(users).filter_by(password=password).exists()
    ).scalar()
    if exists_name and exists_pass:
        return Response("{'response':'Succesfull login'}", status=200, mimetype='application/json') 
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


def delete_user(users, students, adress, db, user_schema, id):
    user = users.query.get(id)
    if user is not None:
        student = students.query.filter_by(user_id=id).first()
        adr = adress.query.filter_by(user_id=id).first()
        if student is not None:
            db.session.delete(student)
        if adr is not None:
            db.session.delete(adr)
        db.session.delete(user)
        db.session.commit()
        return Response("{'response':'Succesfull operation'}", status=200, mimetype='application/json')   
    else:
        return Response("{'response':'User not found'}", status=404, mimetype='application/json')   

