from flask import Flask, jsonify, request


def create_message(msg, message_schema, db, from_id, to_id):

    content = request.json['content']
    attachment = request.json['attachment']
    message = msg(content, attachment, from_id, to_id)
    db.session.add(message)
    db.session.commit()
    return message_schema.jsonify(message)


def get_message(msg, message_schema, id):

    message = msg.query.get(id)
    return message_schema.jsonify(message)


def update_message(msg, db, message_schema, id):

    message = msg.query.get(id)
    content = request.json['content']
    attachment = request.json['attachment']
    message.content = content
    message.attachment = attachment
    db.session.commit()
    return message_schema.jsonify(message)
