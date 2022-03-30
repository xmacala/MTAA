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
        return Response("{'response':'Successfull operation'}", status=400, mimetype='application/json') 
    except:
        return Response("{'response':'Invalid ID supplied'}", status=400, mimetype='application/json') 


def get_address(addr, address_schema, user_id):
    try:
        address = addr.query.filter_by(user_id=user_id).first()
        if address is not None:
            return address_schema.jsonify(address)
        else:
            return Response("{'response':'Address not found'}", status=404, mimetype='application/json') 
    except:
        return Response("{'response':'Invalid ID supplied'}", status=400, mimetype='application/json') 
        


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
            return Response("{'response':'Successfull operation'}", status=200, mimetype='application/json') 
        else:
            return Response("{'response':'Address not found'}", status=404, mimetype='application/json') 
    except:
        return Response("{'response':'Invalid ID supplied'}", status=400, mimetype='application/json') 
