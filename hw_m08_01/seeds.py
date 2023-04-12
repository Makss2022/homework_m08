import json

import connect
from models import Authors, Qoutes


def read_file(file):
    with open(file, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    return data


def load_to_db_authors():
    file_authors = "authors.json"
    data = read_file(file_authors)
    for el in data:
        author = Authors(fullname=el["fullname"])
        author.born_date = el["born_date"]
        author.born_location = el["born_location"]
        author.description = el["description"]
        author.save()


def load_to_db_qoutes():
    file_qoutes = "qoutes.json"
    data = read_file(file_qoutes)
    for el in data:
        qoute = Qoutes(quote=el["quote"])
        qoute.tags = el["tags"]
        qoute.author = Authors.objects(fullname=el["author"])[0].id
        qoute.save()


if __name__ == "__main__":
    load_to_db_authors()
    load_to_db_qoutes()
