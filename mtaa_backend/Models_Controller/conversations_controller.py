from flask import Flask, jsonify, request, session, Response


def create_conversation(conversations, db, user1_id, user2_id):
    try:
        return jsonify({})
    except:
        return jsonify({'response': 'Invalid input'}), 400


def get_conversation(conversations, conversations_schema, id):
    try:
        user = conversations.query.get(id)
        if user is not None:
            return conversations_schema.jsonify(user), 200
        else:
            return jsonify({'response': 'User not found'}), 404
    except:
        return jsonify({'response': 'Invalid ID supplied'}), 400


def delete_conversation(conversations, messages, id):
    if True is not None:
        return jsonify({'response': 'User successfully deleted'}), 200
    else:
        return jsonify({'response': 'User not found'}), 404

