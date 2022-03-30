from django.shortcuts import redirect
from flask import Flask, jsonify, request, Response
import os


def create_post(post, db, user_id):
    try:
        if request.files:
            #app.config["IMAGE_UPLOADS"] = "C:/Users/42191/Documents/mtaa_mobile_app/mtaa_mobile_app/backend/images"
            image = request.files['image']
            #image.save(os.path("C:/Users/42191/Documents/mtaa_mobile_app/mtaa_mobile_app/backend/images", image.filename))
            photo_name = os.path.abspath(image.filename)
            exists_photo = db.session.query(
            db.session.query(post).filter_by(filename=photo_name).exists()
            ).scalar()
            if exists_photo:
                return Response("{'response':'Photo already used'}", status=403, mimetype='application/json')
            photo = post(photo_name, image.read(), user_id)
            db.session.add(photo)
            db.session.commit()
            return Response("{'response':'Successfull operation'}", status=200, mimetype='application/json') 
        else:
            return Response("{'response':'Invalid input'}", status=400, mimetype='application/json') 
    except:
        return Response("{'response':'Invalid ID supplied'}", status=404, mimetype='application/json') 


def get_post(post, post_schema, id):
    try:
        poster = post.query.filter(id=id).first()
        if post:
            return post_schema.jsonify(poster)
        else:
            return Response("{'response':'Post not found'}", status=404, mimetype='application/json') 
    except:
        return Response("{'response':'Invalid ID supplied'}", status=400, mimetype='application/json') 


def get_posts(post, posts_schema, owner_id):
    try:
        posts = post.query.filter_by(owner_id=owner_id).all()
        if posts:
            return posts_schema.jsonify(posts)
        else:
            return Response("{'response':'Posts not found'}", status=404, mimetype='application/json') 
    except:
        return Response("{'response':'Invalid ID supplied'}", status=400, mimetype='application/json') 


def post_liked(posts, db, id):
    try:
        post = posts.query.get(id)
        if post is not None:
            post.likes = post.likes + 1
            db.session.commit()
            return Response("{'response':'Like added'}", status=200, mimetype='application/json') 
        else:
            return Response("{'response':'Post not found'}", status=404, mimetype='application/json') 
    except:
        return Response("{'response':'Invalid ID supplied'}", status=400, mimetype='application/json') 

def post_update(post, db, id):
    try:
        post = post.query.get(id)
        if post is not None:
            file = request.files['image']
            post.filename = file.filename
            post.attachment = file.read()
            db.session.commit()
            return Response("{'response':'Successfull operation'}", status=200, mimetype='application/json')
        else:
            return Response("{'response':'Post not found'}", status=404, mimetype='application/json')
    except:
        return Response("{'response':'Invalid ID supplied'}", status=400, mimetype='application/json')

def delete_post(post, db, id):
    try:
        poster = post.query.get(id)
        if poster is not None:
            db.session.delete(poster)
            db.session.commit()
            return Response("{'response':'Successfull operation'}", status=200, mimetype='application/json')
        else:
            return Response("{'response':'Post not found'}", status=404, mimetype='application/json')
    except:
        return Response("{'response':'Invalid ID supplied'}", status=400, mimetype='application/json')