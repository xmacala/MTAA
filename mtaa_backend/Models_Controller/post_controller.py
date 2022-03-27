from flask import Flask, jsonify, request


def create_post(post, post_schema, db):

    content = request.json['content']
    attachment = request.json['attachment']
    message = post(content, attachment)
    db.session.add(message)
    db.session.commit()
    return post_schema.jsonify(message)


def get_post(post, post_schema, id):

    post = post.query.get(id)
    return post_schema.jsonify(post)


def get_posts(post, posts_schema, owner_id):

    posts = post.query.all(owner_id)
    return posts_schema.jsonify(posts)


def post_update(post, db, post_schema, id):

    post = post.query.get(id)
    content = request.json['content']
    attachment = request.json['attachment']
    post.content = content
    post.attachment = attachment
    db.session.commit()
    return post_schema.jsonify(post)
