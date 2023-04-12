import connect

from models import Authors, Qoutes


def search_by_name(author_name):
    author_object = Authors.objects(fullname__istartswith=author_name)[0]
    result = Qoutes.objects(author=author_object.id)
    print(f"\nQuotes by {author_object.fullname}:")
    for el in result:
        print("    ", el.quote)


def search_by_teg(value):
    result = Qoutes.objects(tags__istartswith=value)
    if not result:
        raise IndexError
    print(f"\nQuotes by tag '{value}':")
    for el in result:
        print(f"    {el.quote} (author: {el.author.fullname})")


def search_by_tegs(value):
    tags = value.split(",")
    result = Qoutes.objects(tags__in=tags)
    if not result:
        raise IndexError
    print(f"\nQuotes by tags {tags}:")
    for el in result:
        print(f"    {el.quote} (author: {el.author.fullname})")


def Invalid_command(value):
    raise ValueError


handler = {
    "name": search_by_name,
    "tag": search_by_teg,
    "tags": search_by_tegs
}


def main():
    while True:
        try:
            user_input = input(
                "\nTo search for quotes, enter the command in the following format 'command:value':\n")
            if user_input.split()[0].lower() == "exit":
                break
            command, value = user_input.split(":")
            handler.get(command, Invalid_command)(value)
        except IndexError:
            print("Nothing found for your request!")
        except ValueError:
            print("Invalid command entered!")


if __name__ == "__main__":
    main()
