from flask import Flask, jsonify, request, Response
from sqlalchemy import desc


def create_post(post, db, user_id):
    try:
        if request.json['file']:
            photo = request.json['file'].encode('utf-8')
            photo = post(photo, user_id)
            db.session.add(photo)
            db.session.commit()
            return jsonify({'response': 'Post successfully created'}), 200
        else:
            return jsonify({'response': 'Invalid input'}), 400
    except:
        return jsonify({'response': 'Something went wrong'}), 404


def get_post(posts, users, post_schema, id):
    try:
        post = posts.query.filter(id=id).first()
        user = users.query.join(posts).filter(posts.owner_id == id).first()
        if post:
            return jsonify({'id': post.id, 'created_at': post.created_at, 'filename': post.filename, 'likes': post.likes, 'username': user.username}), 200
        else:
            return jsonify({'response': 'Post not found'}), 404
    except:
        return jsonify({'response': 'Something went wrong'}), 400


def get_posts(post, post_schema, owner_id):
    try:
        posts = post.query.filter_by(owner_id=owner_id).order_by(desc(post.created_at)).all()
        if posts:
            return post_schema.jsonify(posts, many=True), 200
        else:
            return jsonify({'response': 'No posts found'}), 404
    except:
        return jsonify({'response': 'Something went wrong'}), 400


def get_all_posts(post, post_schema):
    try:
        posts = post.query.order_by(desc(post.created_at)).all()
        if posts:
            return post_schema.jsonify(posts, many=True), 200
        else:
            return jsonify({'response': 'No posts found'}), 404
    except:
        return jsonify({'response': 'Something went wrong'}), 400


def like_post(posts, db, id):
    try:
        post = posts.query.get(id)
        if post is not None:
            post.likes = post.likes + 1
            db.session.commit()
            return jsonify({'response': 'Post liked'}), 200
        else:
            return jsonify({'response': 'Post not found'}), 404
    except:
        return jsonify({'response': 'Something went wrong'}), 400


def update_post(post, db, id):
    try:
        poster = post.query.get(id)
        if poster is not None:
            photo = request.json['file'].encode('utf-8')
            poster.attachment = photo
            db.session.commit()
            return jsonify({'response': 'Post successfully updated'}), 200
        else:
            return jsonify({'response': 'Post not found'}), 404
    except:
        return jsonify({'response': 'Something went wrong'}), 400


def delete_post(post, db, id):
    try:
        poster = post.query.get(id)
        if poster is not None:
            db.session.delete(poster)
            db.session.commit()
            return jsonify({'response': 'Post successfully deleted'}), 200
        else:
            return jsonify({'response': 'Post not found'}), 404
    except:
        return jsonify({'response': 'Something went wrong'}), 400