
import subprocess
import uuid
import requests
from werkzeug.utils import secure_filename
import os
import ffmpeg

from flask import request, jsonify
from config import app, db
from models import Contact


# Add default contacts to the database, hard coded database
with app.app_context():
    default_contacts = [
        {"id": 59, "firstName": "John", "lastName": "Doe", "email": "john@example.com"}
        # {"firstName": "Jane", "lastName": "Smith", "email": "jane@example.com"},
        # {"firstName": "Alice", "lastName": "Johnson", "email": "alice@example.com"}
    ]
    for contact_data in default_contacts:
        # checking if the same email exist
        existing_contact = Contact.query.filter_by(email=contact_data['email']).first()
        if existing_contact is None:
            # contact = Contact(**contact_data)
            contact = Contact(
                # id is primary key, we are not allow to modified it
                        # id=contact["id"],
                        first_name=contact_data["firstName"],
                        last_name=contact_data["lastName"],
                        email=contact_data["email"])
            db.session.add(contact)
    db.session.commit()

# read the data from database 
@app.route("/contacts", methods=["GET"])
def get_contacts():
    # get everything from the database, should be a list of Contact object
    contacts = Contact.query.all()
    # map each Contact object into json
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    # we create a json object {contacts: [{}, {}, {}]}
    return jsonify({"contacts": json_contacts})

# a test functino to test can we call logic functin in backend 
def generate(name, state="human"):
    c = 1 + 4
    c_word = 'five' if str(c) == '5' else None
    return name + state + str(c_word)

@app.route("/create_contact", methods=["POST"])
def create_contact():
    # the the data user enter to the firstName
    first_name = request.json.get("firstName")  # datatype = type of data stored in the JSON object for the key "firstName" (String)
    # first_name = generate(first_name)
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    if not first_name or not last_name or not email:
        return (
            jsonify({"message": "You must include a first name, last name and email"}),
            400,
        )

    new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "User created!"}), 201


@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404

    data = request.json
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)

    db.session.commit()

    return jsonify({"message": "Usr updated."}), 200


@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "User deleted!"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)