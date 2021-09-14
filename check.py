

def check_empty(variable):
    if len(variable) == 0:
        return True
    else:
        return False


import re
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
def check(email):
    if (re.search(regex, email)):
        return True
    else:
        return False


def check_pass(variable):
    if len(variable) < 8:
        return 'Password sMUST be more than eight characters'
    elif not re.search("[a-z]", variable):
        return 'Must have at least a small letter'

    elif not re.search("[A-Z]", variable):
        return 'Must have at least a capital letter'

    elif not re.search("[0-9]", variable):
        return 'Must have at least a small letter'

    elif not re.search("[_@$]", variable):
        return 'Must have at least a symbol'

    else:
        return True