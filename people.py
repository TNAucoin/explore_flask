from flask import abort, make_response
from config import db
from models import Person, people_schema, person_schema


def read_all():
    people = Person.query.all()
    return people_schema.dump(people)


def read_one(lname):
    person = Person.query.filter(Person.lname == lname).one_or_none()
    if person is not None:
        return person_schema.dump(person)
    else:
        abort(404, f"Person with {lname} not found")


def create(person):
    lname = person.get("lname")
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()
    if existing_person is None:
        new_person = person_schema.load(person, session=db.session)
        db.session.add(new_person)
        db.session.commit()
        return person_schema.dump(new_person), 201
    else:
        abort(406, f"Person with {lname} already exists")


def update(lname, person):
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()
    if existing_person is not None:
        update_person = person_schema.load(person, session=db.session)
        existing_person.fname = update_person.fname
        db.session.merge(existing_person)
        db.session.commit()
        return people_schema.dump(existing_person), 201
    else:
        abort(404, f"Person with last name {lname} was not found")


def delete(lname):
    existing_person = Person.query(Person.lname == lname).one_or_none()
    if existing_person is not None:
        db.session.delete(existing_person)
        db.session.commit()
        return make_response(f"{lname} sucessfully deleted", 200)
    else:
        abort(404, f"Person with {lname} was not found")
