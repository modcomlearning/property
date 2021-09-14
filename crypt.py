import hashlib, binascii, os
# This function receives a password as a parameter
# its hashes and salts using sha512 encoding
def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

# below provide a plain password and see its hashed/salted output
# hashedpassword = hash_password("modcom20200")
# print(hashedpassword)


# this function checks if hashed password is the same as
# provided password
def verify_password(hashed_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = hashed_password[:64]
    hashed_password = hashed_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == hashed_password
# run it , provide the hashed and the real password
# SHOULD GIVE YOU TRUE/FALSE
#status = verify_password("bdd2bd409c72840a4ce1f565d00bb5ae01d8e84183815b55ca11236b467558b3574d5788bbccc5d0300ba885c593a8c30139aa6cba68c072952ed9b7f57191a3f4609fc7531ae273daa993377ecd46a05c1065811aada4fdd47f62968cbb018c", "modcom20200")
#print(status)