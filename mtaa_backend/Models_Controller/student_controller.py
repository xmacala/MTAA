from os import abort
from fastapi import Response
from flask import Flask, jsonify, request, Response
import os


def create_student(students, db, user_id):
    try:
        fullname = request.json['fullname']
        phonenumber = request.json['phonenumber']
        contacts = request.json['contacts']
        height = request.json['height']
        weight = request.json['weight']
        hobby = request.json['hobby']
        haircolor = request.json['haircolor']
        bodytype = request.json['bodytype']
        filename = None
        student = students(fullname, phonenumber, contacts, height, weight, hobby, haircolor, bodytype, filename , user_id)
        db.session.add(student)
        db.session.commit()
        return Response("{'response':'Successfull operation'}", status=200, mimetype='application/json') 
    except:
        return Response("{'response':'Invalid input'}", status=400, mimetype='application/json') 


def get_student(students, student_schema, user_id):
    try:
        student = students.query.filter_by(user_id = user_id).first()
        if student is not None:
            return student_schema.jsonify(student)
        else:
            return Response("{'response':'Student not found'}", status=404, mimetype='application/json') 
    except:
        return Response("{'response':'Invalid ID supplied'}", status=400, mimetype='application/json') 


def update_data_student(students, db, user_id):
    try:
        student = students.query.filter_by(user_id = user_id).first()
        if student is not None:
            try:
                fullname = request.json['fullname']
                phonenumber = request.json['phonenumber']
                contacts = request.json['contacts']
                height = request.json['height']
                weight = request.json['weight']
                hobby = request.json['hobby']
                haircolor = request.json['haircolor']
                bodytype = request.json['bodytype']
                student.fullname = fullname
                student.phonenumber = phonenumber
                student.contacts = contacts
                student.height = height
                student.weight = weight
                student.hobby = hobby
                student.haircolor = haircolor
                student.bodytype = bodytype
                db.session.commit()
                return Response("{'response':'Successfull operation'}", status=200, mimetype='application/json')
            except:
                return Response("{'response':'Invalid input'}", status=400, mimetype='application/json')
        else:
            return Response("{'response':'Student not found'}", status=404, mimetype='application/json')
    except:
        return Response("{'response':'Invalid ID supplied'}", status=400, mimetype='application/json') 


def update_photo_student(students, db, user_id):
    try:
        student = students.query.filter_by(user_id = user_id).first()
        if student is not None:
            photo = request.files['file']
            student.filename = os.path.abspath(photo.filename)
            #student.file = photo.read()
            db.session.commit()
            return Response("{'message':'Photo successfully uploaded'}", status=200, mimetype='application/json')
        else:
            return Response("{'message':'Student not found'}", status=404, mimetype='application/json')
    except:
        return Response("{'response':'Invalid ID supplied'}", status=400, mimetype='application/json') 