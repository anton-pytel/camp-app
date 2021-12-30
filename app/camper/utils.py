import string
import random

# characters to generate password from
characters = list(string.ascii_letters + string.digits + "!")


def generate_random_password(length):
    # shuffling the characters
    random.shuffle(characters)

    # picking random characters from the list
    password = []
    for i in range(length):
        password.append(random.choice(characters))

    # shuffling the resultant password
    random.shuffle(password)

    # converting the list to string
    return "".join(password)


def get_username(p_name, l_name, sfx):
    return f"{p_name.lower()}.{l_name.lower()}-{sfx}"
