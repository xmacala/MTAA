from flask import Flask, jsonify, request, Response


def create_message(msg, db, from_id, to_id):
    try:
        photo = request.json['file']
        content = request.json['content']
        message = msg(content, photo.encode('utf-8'), from_id, to_id)
        db.session.add(message)
        db.session.commit()
        return jsonify({'response': 'Message successfully sent'}), 200
    except:
        return jsonify({'response': 'Invalid input'}), 400


def get_message(msg, message_schema, from_id, to_id):
    try:
        messages_1 = msg.query.filter_by(from_id=from_id, to_id=to_id).all()
        messages_2 = msg.query.filter_by(from_id=to_id, to_id=from_id).all()
        all_messages = messages_1 + messages_2
        if all_messages:
            newlist = sorted(all_messages, key=lambda x: x.sent_at)
            return message_schema.jsonify(newlist), 200
        else:
            return jsonify({'response': 'Message not found'}), 404
    except:
        return jsonify({'response': 'Something went wrong'}), 400


def update_message(msg, db, id):
    try:
        message = msg.query.get(id)
        if message:
            attachment = request.json['file']
            content = request.json['content']
            message.content = content
            message.attachment = attachment.encode('utf-8')
            db.session.commit()
            return jsonify({'response', 'Message successfully updated'}), 200
        else:
            return jsonify({'response': 'Message not found'}), 404
    except:
        return jsonify({'response': 'Something went wrong'}), 400


def delete_message(msg, db, id):
    try:
        message = msg.query.get(id)
        if message:
            db.session.delete(message)
            db.session.commit()
            return jsonify({'response': 'Message successfully deleted'}), 200
        else:
            return jsonify({'response': 'Message not found'}), 404
    except:
        return jsonify({'response': 'Something went wrong'}), 400
