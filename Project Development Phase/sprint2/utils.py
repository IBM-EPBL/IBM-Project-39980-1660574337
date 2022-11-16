from datetime import datetime, timedelta
from main import app, conn
import jwt
import ibm_db
import random
import array


# Token Generator To Reset Password
def token_generator(user):
    token = jwt.encode({'user': user, 'exp': datetime.utcnow() + timedelta(minutes=15)},
                       app.config['SECRET_KEY'])

    sql = 'UPDATE USER_TABLE SET RESET_LINK=? WHERE EMAIL=?'
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, token)
    ibm_db.bind_param(stmt, 2, user)
    ibm_db.execute(stmt)
    return token


# Token Verification
def verify_token(token):
    verify = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    email = verify['user']

    sql = 'SELECT EMAIL FROM USER_TABLE WHERE email=?'
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, email)
    ibm_db.execute(stmt)
    return ibm_db.fetch_assoc(stmt)


def generate_random_password():
    max_len = 8
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    lower_case = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    upper_case = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    symbols = ['@', '#', '$', '%', '?', '.', '/', '*']
    combined_list = digits + upper_case + lower_case + symbols

    rand_digit = random.choice(digits)
    rand_upper = random.choice(upper_case)
    rand_lower = random.choice(lower_case)
    rand_symbol = random.choice(symbols)

    temp_pwd = rand_digit + rand_upper + rand_lower + rand_symbol
    temp_pass_list = []
    for x in range(max_len - 4):
        temp_pwd = temp_pwd + random.choice(combined_list)
        temp_pass_list = array.array('u', temp_pwd)
        random.shuffle(temp_pass_list)

    password = ""
    for x in temp_pass_list:
        password = password + x

    return password