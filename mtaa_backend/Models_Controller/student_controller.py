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
        age = request.json['age']
        bodytype = request.json['bodytype']
        interests = request.json['interests']
        file = None
        student = students(fullname, phonenumber, contacts, height, weight, hobby, haircolor, age, bodytype, interests, file, user_id)
        db.session.add(student)
        db.session.commit()
        return jsonify({'response': 'Student data successfully added'}), 200
    except:
        return jsonify({'response': 'Invalid input'}), 400


def get_student(students, student_schema, user_id):
    try:
        student = students.query.filter_by(user_id=user_id).first()
        if student is not None:
            return student_schema.jsonify(student), 200
        else:
            return jsonify({'response': 'Student not found'}), 404
    except:
        return jsonify({'response': 'Invalid ID supplied'}), 400


def get_students(students, student_schema, user_id):
    try:
        data = students.query.filter(students.user_id != user_id).all()
        return student_schema.jsonify(data, many=True), 200
    except:
        return jsonify({'response': 'Invalid ID supplied'}), 400


def update_student_data(students, db, user_id):
    try:
        student = students.query.filter_by(user_id=user_id).first()
        if student is not None:
            try:
                fullname = request.json['fullname']
                phonenumber = request.json['phonenumber']
                contacts = request.json['contacts']
                height = request.json['height']
                weight = request.json['weight']
                hobby = request.json['hobby']
                haircolor = request.json['haircolor']
                age = request.json['age']
                bodytype = request.json['bodytype']
                interests = request.json['interests']
                student.fullname = fullname
                student.phonenumber = phonenumber
                student.contacts = contacts
                student.height = height
                student.weight = weight
                student.hobby = hobby
                student.haircolor = haircolor
                student.age = age
                student.bodytype = bodytype
                student.interests = interests
                db.session.commit()
                return jsonify({'response': 'Student data successfully updated'}), 200
            except:
                return jsonify({'response': 'Invalid input'}), 400
        else:
            return jsonify({'response': 'Student not found'}), 404
    except:
        return jsonify({'response': 'Invalid ID supplied'}), 400


def update_student_photo(students, db, user_id):
    try:
        student = students.query.filter_by(user_id=user_id).first()
        if student is not None:
            photo = request.json['file']
            student.file = photo.encode('utf-8')
            db.session.commit()
            return jsonify({'response': 'Photo successfully uploaded'}), 200
        else:
            return jsonify({'response': 'Student not found'}), 404
    except:
        return jsonify({'response': 'Invalid ID supplied'}), 400
