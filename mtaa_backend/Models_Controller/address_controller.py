from flask import Flask, jsonify, request, Response


def create_address(addr, address_schema, db, user_id):
    try:
        street = request.json['street']
        city = request.json['city']
        postalcode = request.json['postalcode']
        country = request.json['country']
        address = addr(street, city, postalcode, country, user_id)
        db.session.add(address)
        db.session.commit()
        return jsonify({'response': 'Address successfully added'}), 200
    except:
        return jsonify({'response': 'Invalid ID supplied'}), 400


def get_address(addr, address_schema, user_id):
    try:
        address = addr.query.filter_by(user_id=user_id).first()
        if address is not None:
            return address_schema.jsonify(address), 200
        else:
            return jsonify({'response': 'Address not found'}), 404
    except:
        return jsonify({'response': 'Invalid ID supplied'}), 400


def update_address(addr, db, address_schema, user_id):
    try:
        address = addr.query.filter_by(user_id=user_id).first()
        if address is not None:
            street = request.json['street']
            city = request.json['city']
            postalcode = request.json['postalcode']
            country = request.json['country']
            address.street = street
            address.city = city
            address.postalcode = postalcode
            address.country = country
            db.session.commit()
            return jsonify({'response': 'Address successfully updated'}), 200
        else:
            return jsonify({'response': 'Address not found'}), 404
    except:
        return jsonify({'response': 'Invalid ID supplied'}), 400
