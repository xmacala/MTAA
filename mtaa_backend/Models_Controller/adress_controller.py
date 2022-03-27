from flask import Flask, jsonify, request


def create_address(addr, address_schema, db):

    street = request.json['street']
    city = request.json['city']
    postalcode = request.json['postalcode']
    country = request.json['country']
    address = addr(street, city, postalcode, country)
    db.session.add(address)
    db.session.commit()
    return address_schema.jsonify(address)


def get_address(addr, address_schema, address_id):

    address = addr.query.get(address_id)
    return address_schema.jsonify(address)


def update_address(addr, db, address_schema, id):

    address = addr.query.get(id)
    street = request.json['street']
    city = request.json['city']
    postalcode = request.json['postalcode']
    country = request.json['country']
    address.street = street
    address.city = city
    address.postalcode = postalcode
    address.country = country
    db.session.commit()
    return address_schema.jsonify(address)
