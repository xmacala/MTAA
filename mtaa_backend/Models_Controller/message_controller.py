from flask import Flask, jsonify, request, Response
import os


def create_message_text(msg_text, db, from_id, to_id):
    try:
        content = request.json['content']
        message = msg_text(content, from_id, to_id)
        db.session.add(message)
        db.session.commit()
        return Response("{'response':'Successfull operation'}", status=200, mimetype='application/json') 
    except:
        return Response("{'response':'Invalid input'}", status=400, mimetype='application/json') 


def get_message_text(msg_text, message_schema, from_id, to_id):
    try:
        message = msg_text.query.filter_by(
            from_id = from_id,
            to_id = to_id).all()
        if message:
            return message_schema.jsonify(message)
        else:
            return Response("{'response':'Message not found'}", status=404, mimetype='application/json') 
    except:
        return Response("{'response':'Invalid ID supplied'}", status=400, mimetype='application/json') 


def update_message_text(msg_text, db, id):
    try:
        message = msg_text.query.get(id)
        if message:
            content = request.json['content']
            message.content = content
            db.session.commit()
            return Response("{'response':'Successfull operation'}", status=200, mimetype='application/json') 
        else:
            return Response("{'response':'Message not found'}", status=404, mimetype='application/json') 
    except:
        return Response("{'response':'Invalid ID suplied'}", status=400, mimetype='application/json') 


def create_message_file(msg_file, db, from_id, to_id):
    try:
        image = request.files['file']
        photo_name = os.path.abspath(image.filename)
        message = msg_file(photo_name, image.read(), from_id, to_id)
        db.session.add(message)
        db.session.commit()
        return Response("{'response':'Successfull operation'}", status=200, mimetype='application/json') 
    except:
        return Response("{'response':'Invalid input'}", status=400, mimetype='application/json') 


def get_message_file(msg_file, message_schema, from_id, to_id):
    try:
        message = msg_file.query.filter_by(
            from_id = from_id,
            to_id=to_id).all()
        if message:
            return message_schema.jsonify(message)
        else:
            return Response("{'response':'Message not found'}", status=404, mimetype='application/json') 
    except:
        return Response("{'response':'Invalid ID supplied'}", status=400, mimetype='application/json') 


def update_message_file(msg_file, db, id):
    try:
        message = msg_file.query.get(id)
        if message:
            file = request.files['file']
            message.filename = file.filename
            message.attachment = file.read()
            db.session.commit()
            return Response("{'response':'Successfull operation'}", status=200, mimetype='application/json') 
        else:
            return Response("{'response':'Message not found'}", status=404, mimetype='application/json') 
    except:
        return Response("{'response':'Invalid ID suplied'}", status=400, mimetype='application/json') 