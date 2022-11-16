from flask import Blueprint, render_template, session, jsonify, request, redirect, url_for
import ibm_db
from main import conn, mail, flask_bcrypt
from flask_mail import Message
from sprint2.utils import token_generator, verify_token, generate_random_password
import jwt

sprint2 = Blueprint('sprint2', __name__, template_folder='templates', static_folder='static', static_url_path='/sprint2/static')


# Registration-Form Template Render
@sprint2.route('/register-as-donor')
def register():
    return render_template('registrations/user_registration.html')


# User Exist Validation
@sprint2.route('/user-exist', methods=['POST'])
def userexist():
    if request.method == 'POST':
        d = dict()
        form = request.json
        email = form['email']

        sql = 'SELECT * FROM USER_TABLE WHERE email=?'
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        flag = ibm_db.fetch_assoc(stmt)

        if flag:
            d['status'] = 'Exist'
        else:
            d['status'] = 'New User'
        return jsonify(d)


# SignUp-Form Submission
@sprint2.route('/form-submission', methods=['GET', 'POST'])
def formsubmission():
    if request.method == 'POST':
        d = request.json
        # Form-1 Data
        email = d['email']
        pwd = d['password']
        # Password Hashing
        password = flask_bcrypt.generate_password_hash(pwd, rounds=12)

        # Form-2 Data
        fname = d['fname']
        lname = d['lname']
        phonenumber = d['phonenumber']
        dob = d['dateofbirth']
        age = int(d['age'])
        bloodgroup = d['bloodgroup']
        address = d['address']
        pincode = d['pincode']
        city = d['city']
        state = d['state']

        # Form-1 Submission
        insert_sql1 = 'INSERT INTO USER_TABLE VALUES (?, ?, NULL, ?)'
        stmt1 = ibm_db.prepare(conn, insert_sql1)
        ibm_db.bind_param(stmt1, 1, email)
        ibm_db.bind_param(stmt1, 2, password)
        ibm_db.bind_param(stmt1, 3, 'Donor')
        ibm_db.execute(stmt1)

        # Form-2 Submission
        insert_sql2 = 'INSERT INTO PERSONALDETAILS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        stmt2 = ibm_db.prepare(conn, insert_sql2)
        ibm_db.bind_param(stmt2, 1, fname)
        ibm_db.bind_param(stmt2, 2, lname)
        ibm_db.bind_param(stmt2, 3, email)
        ibm_db.bind_param(stmt2, 4, dob)
        ibm_db.bind_param(stmt2, 5, age)
        ibm_db.bind_param(stmt2, 6, phonenumber)
        ibm_db.bind_param(stmt2, 7, bloodgroup)
        ibm_db.bind_param(stmt2, 8, address)
        ibm_db.bind_param(stmt2, 9, pincode)
        ibm_db.bind_param(stmt2, 10, city)
        ibm_db.bind_param(stmt2, 11, state)
        ibm_db.execute(stmt2)

        data = dict()
        data['status'] = 'success'
        return jsonify(data)


# Request Reset Form
@sprint2.route('/request-reset', methods=['GET', 'POST'])
def request_reset_form():
    if request.method == 'POST':
        d = dict()
        data = request.json
        email = data['email']

        sql = 'SELECT EMAIL FROM USER_TABLE WHERE email=?'
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        user = ibm_db.fetch_assoc(stmt)

        if user:
            d['status'] = 'Exist'
            token = token_generator(user['EMAIL'])
            msg = Message('Password Reset Link', sender='noreplyplasmadonor@gmail.com', recipients=[user['EMAIL']])
            msg.body = f'''Password reset link 
{url_for('sprint2.password_reset', token=token, _external=True)}'''
            mail.send(msg)
        else:
            d['status'] = 'Invalid'
        return jsonify(d)
    else:
        return render_template('registrations/request_reset_form.html')


@sprint2.route('/reset-password/<token>', methods=['GET', 'POST'])
def password_reset(token):
    d = dict()
    if request.method == 'POST':
        data = request.json
        new_pwd = data['new_password']
        email = session['email']

        if email:
            new_password = flask_bcrypt.generate_password_hash(new_pwd, rounds=12)

            update_sql = 'UPDATE USER_TABLE SET PASSWORD=? WHERE email=?'
            stmt2 = ibm_db.prepare(conn, update_sql)
            ibm_db.bind_param(stmt2, 1, new_password)
            ibm_db.bind_param(stmt2, 2, email)
            ibm_db.execute(stmt2)

            # Deleting link to make token invalid
            delete_link = 'UPDATE USER_TABLE SET RESET_LINK=NULL WHERE  EMAIL=?'
            stmt3 = ibm_db.prepare(conn, delete_link)
            ibm_db.bind_param(stmt3, 1, email)
            ibm_db.execute(stmt3)

            d['status'] = 'PasswordUpdated'
            return jsonify(d)
    else:
        try:
            user = verify_token(token)
            if user:
                email = user["EMAIL"]

                sql = 'SELECT RESET_LINK, STATUS FROM USER_TABLE WHERE EMAIL=?'
                stmt1 = ibm_db.prepare(conn, sql)
                ibm_db.bind_param(stmt1, 1, email)
                ibm_db.execute(stmt1)
                reset_link = ibm_db.fetch_assoc(stmt1)

                if reset_link['RESET_LINK'] == token:
                    session['email'] = email
                    return render_template('registrations/password_reset.html', BtnTyp=reset_link['STATUS'])
                else:
                    return redirect(url_for('sprint2.request_reset_form'))

        except jwt.exceptions.ExpiredSignatureError:
            return redirect(url_for('sprint2.request_reset_form'))


@sprint2.route('/register-as-org', methods=['GET', 'POST'])
def sign_up_as_org():
    if request.method == 'POST':
        response = dict()
        data = request.json

        sql = 'select * from USER_TABLE where EMAIL=?'
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, data['org_email'])
        ibm_db.execute(stmt)
        user = ibm_db.fetch_assoc(stmt)

        if user:
            response['status'] = 'Org-Exist'
        else:
            sql = 'select * from ORGANISATION_DETAILS where EMAIL=?'
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, data['org_email'])
            ibm_db.execute(stmt)
            user = ibm_db.fetch_assoc(stmt)

            if user:
                response['status'] = 'PENDING'
                return jsonify(response)

            sql2 = 'insert into ORGANISATION_DETAILS values (?, ?, ?, ?, ?, ?, ?, ?, NULL)'
            stmt2 = ibm_db.prepare(conn, sql2)
            ibm_db.bind_param(stmt2, 1, data['org_name'])
            ibm_db.bind_param(stmt2, 2, data['org_email'])
            ibm_db.bind_param(stmt2, 3, data['org_contact'])
            ibm_db.bind_param(stmt2, 4, data['org_address'])
            ibm_db.bind_param(stmt2, 5, data['org_locality'])
            ibm_db.bind_param(stmt2, 6, data['org_city'])
            ibm_db.bind_param(stmt2, 7, data['org_state'])
            ibm_db.bind_param(stmt2, 8, int(data['org_pincode']))
            ibm_db.execute(stmt2)

            response['status'] = 'New-user'
        return jsonify(response)
    else:
        return render_template('registrations/organisation_registration.html')


@sprint2.route('/Administrator', methods=['GET', 'POST'])
def administrator():
    if 'ADMINISTRATOR' in session:
        if request.method == 'POST':
            data = request.json
            if 'email' in data and 'action' in data:
                response = dict()
                if data['action'] == 'approve':
                    pwd = generate_random_password()

                    sql = 'insert into USER_TABLE values (?, ?, NULL, ?)'
                    stmt = ibm_db.prepare(conn, sql)
                    ibm_db.bind_param(stmt, 1, data['email'])
                    ibm_db.bind_param(stmt, 2, (flask_bcrypt.generate_password_hash(pwd, rounds=12)))
                    ibm_db.bind_param(stmt, 3, 'Organisation')
                    ibm_db.execute(stmt)

                    sql2 = 'update ORGANISATION_DETAILS set APPROVED=? where EMAIL=?'
                    stmt2 = ibm_db.prepare(conn, sql2)
                    ibm_db.bind_param(stmt2, 1, 'YES')
                    ibm_db.bind_param(stmt2, 2, data['email'])
                    ibm_db.execute(stmt2)

                    msg = Message('Verification Status', sender='noreplyplasmadonor@gmail.com', recipients=[data['email']])
                    msg.body = f'''We have approved your organisation. Find your login credentials below,
Username: { data['email'] }
Password: { pwd }'''
                    mail.send(msg)
                    response['action'] = 'Approved'
                else:
                    sql2 = 'update ORGANISATION_DETAILS set APPROVED=? where EMAIL=?'
                    stmt2 = ibm_db.prepare(conn, sql2)
                    ibm_db.bind_param(stmt2, 1, 'NO')
                    ibm_db.bind_param(stmt2, 2, data['email'])
                    ibm_db.execute(stmt2)
                    response['action'] = 'Declined'
                return response
        else:
            sql = 'select * from ORGANISATION_DETAILS'
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.execute(stmt)
            fetch = ibm_db.fetch_assoc(stmt)

            res = []
            res1 = []
            res2 = []
            while fetch:
                if fetch['APPROVED'] is None:
                    res.append(fetch)
                elif fetch['APPROVED'] == 'YES':
                    res1.append(fetch)
                else:
                    res2.append(fetch)
                fetch = ibm_db.fetch_assoc(stmt)

            return render_template('administrator.html', res=res, approved=res1, declined=res2)
    else:
        return redirect(url_for('sprint2.administrator_login'))


@sprint2.route('/administrator-login')
def administrator_login():
    return render_template('registrations/administrator_login.html')