import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
import jwt
from flask_mail import Mail, Message
from datetime import timedelta, datetime
import ibm_db
import ibm_boto3
from ibm_botocore.client import Config, ClientError

app = Flask(__name__)
app.secret_key = '6cb31e331b9133af9c318ae612505678a9ec367bb724df143993d330303f6709'
flask_bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
COS_API_KEY_ID = "mUV7uy3DpwlEmh25c-Tzr__zBd-LEx2MRx09MM6v2OgT"
COS_INSTANCE_CRN = "crn:v1:bluemix:public:iam-identity::a/e27ad57ec8f0419b8c4af4074d921bd2::serviceid:ServiceId-460841d6-8656-4d5f-8c7b-084659085116"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('E-MAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL-PASSWORD')
mail = Mail(app)
app.permanent_session_lifetime = timedelta(minutes=5)

conn = ibm_db.connect('DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT'
                      '=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=kzg03731;PWD=f4Jb4Y6d8YHaha5F', '', '')
autocommitstatus = ibm_db.autocommit(conn)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


@app.route('/')
def home():
    if 'user' in session:
        username = session['user']
        return render_template('home.html', message=username)
    else:
        return render_template('home.html')


# Login Verification
@app.route('/login', methods=['POST', 'GET'])
def login():
    data = dict()
    if request.method == 'POST':
        loginform = request.json
        email = loginform['username']
        password = loginform['loginpassword']

        sql = 'SELECT PASSWORD FROM USER_TABLE WHERE email=?'
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        userdata = ibm_db.fetch_assoc(stmt)

        if userdata:
            if flask_bcrypt.check_password_hash(userdata['PASSWORD'], password):
                pd_sql = 'SELECT FirstName FROM PERSONALDETAILS WHERE email=?'
                stmt1 = ibm_db.prepare(conn, pd_sql)
                ibm_db.bind_param(stmt1, 1, email)
                ibm_db.execute(stmt1)
                username = ibm_db.fetch_assoc(stmt1)
                session.permanent = True
                session['user'] = username['FIRSTNAME']
                data['status'] = 'logged-in'
            else:
                data['status'] = 'Invalid-Password'
        else:
            data['status'] = 'Invalid-User'
        return jsonify(data)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


# Registration-Form Template Render
@app.route('/register')
def register():
    return render_template('registrations/user_registration.html')


# User Exist Validation
@app.route('/user-exist', methods=['POST'])
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


# Form-1 and Form-2 Submission
@app.route('/form-submission', methods=['GET', 'POST'])
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
        insert_sql1 = 'INSERT INTO USER_TABLE VALUES (?, ?, DEFAULT)'
        stmt1 = ibm_db.prepare(conn, insert_sql1)
        ibm_db.bind_param(stmt1, 1, email)
        ibm_db.bind_param(stmt1, 2, password)
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


@app.route('/request-reset', methods=['GET', 'POST'])
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
{url_for('password_reset', token=token, _external=True)}'''
            mail.send(msg)
        else:
            d['status'] = 'Invalid'
        return jsonify(d)
    else:
        return render_template('registrations/request_reset_form.html')


# Token Generator To Reset Password
def token_generator(user):
    token = jwt.encode({'user': user, 'exp': datetime.utcnow() + timedelta(minutes=15)},
                       app.config['SECRET_KEY'])
    user = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    email = user['user']

    sql = 'UPDATE USER_TABLE SET RESETLINK=? WHERE EMAIL=?'
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, token)
    ibm_db.bind_param(stmt, 2, email)
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


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
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
            delete_link = 'UPDATE USER_TABLE SET RESETLINK=NULL WHERE  EMAIL=?'
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

                sql = 'SELECT RESETLINK FROM USER_TABLE WHERE EMAIL=?'
                stmt1 = ibm_db.prepare(conn, sql)
                ibm_db.bind_param(stmt1, 1, email)
                ibm_db.execute(stmt1)
                reset_link = ibm_db.fetch_assoc(stmt1)

                if reset_link == token:
                    session['email'] = email
                    return render_template('registrations/password_reset.html')
                else:
                    return redirect(url_for('request_reset_form'))

        except jwt.exceptions.ExpiredSignatureError:
            return redirect(url_for('request_reset_form'))


@app.route('/assignment')
def assignment():
    return render_template('assignment.html')


cos = ibm_boto3.resource("s3",
                         ibm_api_key_id=COS_API_KEY_ID,
                         ibm_service_instance_id=COS_INSTANCE_CRN,
                         config=Config(signature_version="oauth"),
                         endpoint_url=COS_ENDPOINT
                         )


def get_item(bucket_name, item_name):
    print("Retrieving item from bucket: {0}, key: {1}".format(bucket_name, item_name))
    try:
        file = cos.Object(bucket_name, item_name).get()

        print("File Contents: {0}".format(file["Body"].read()))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve file contents: {0}".format(e))


def get_bucket_contents(bucket_name):
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    try:
        files = cos.Bucket(bucket_name).objects.all()
        files_names = []
        for file in files:
            files_names.append(file.key)
            print("Item: {0} ({1} bytes).".format(file.key, file.size))
        return files_names
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))


@app.route('/resume', methods=['GET', 'POST'])
def resume():
    if request.method == 'POST':
        pass
    else:
        return render_template('resume.html')