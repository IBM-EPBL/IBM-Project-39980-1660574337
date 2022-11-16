from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify
import ibm_db
from main import conn, flask_bcrypt

sprint1 = Blueprint('sprint1', __name__, template_folder='templates', static_folder='static', static_url_path='/sprint1/static')


@sprint1.route('/')
def home():
    return render_template('home.html')


# Login Verification
@sprint1.route('/login', methods=['POST', 'GET'])
def login():
    data = dict()
    if request.method == 'POST':
        loginform = request.json
        email = loginform['username']
        password = loginform['loginpassword']

        if loginform['title'] != 'Administrator Login':
            if loginform['loginAs'] == 'AsDonor':
                sql = 'SELECT PASSWORD FROM USER_TABLE WHERE email=? and STATUS=\'Donor\''
            else:
                sql = 'SELECT PASSWORD FROM USER_TABLE WHERE email=? and STATUS=\'Organisation\''
        else:
            sql = 'SELECT PASSWORD FROM USER_TABLE WHERE email=? and STATUS=\'Administrator\''

        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        userdata = ibm_db.fetch_assoc(stmt)

        if userdata:
            if flask_bcrypt.check_password_hash(userdata['PASSWORD'], password):
                session.permanent = True
                if loginform['title'] == 'Administrator Login':
                    session['ADMINISTRATOR'] = 'active'
                    data['status'] = 'logged-in'
                    data['user'] = 'ADMIN'
                else:
                    if loginform['loginAs'] == 'AsDonor':
                        pd_sql = 'SELECT FirstName FROM PERSONALDETAILS WHERE email=?'
                        stmt1 = ibm_db.prepare(conn, pd_sql)
                        ibm_db.bind_param(stmt1, 1, email)
                        ibm_db.execute(stmt1)
                        username = ibm_db.fetch_assoc(stmt1)

                        # Adding user to session
                        session['user'] = username['FIRSTNAME']
                        session['donor-email'] = email
                        data['user'] = 'Donor'
                        data['status'] = 'logged-in'
                    else:
                        session['Organisation'] = email
                        data['status'] = 'logged-in'
                        data['user'] = 'Org'
            else:
                data['status'] = 'Invalid-Password'
        else:
            data['status'] = 'Invalid-User'
        return jsonify(data)


@sprint1.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('sprint1.home'))


@sprint1.route('/admin-logout')
def admin_logout():
    session.pop('ADMINISTRATOR', None)
    return redirect(url_for('sprint2.administrator_login'))


@sprint1.route('/org-logout')
def org_logout():
    session.pop('Organisation', None)
    return redirect(url_for('sprint1.home'))