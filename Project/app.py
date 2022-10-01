from flask import Flask, render_template, request
import ibm_db

app = Flask(__name__)

conn = ibm_db.connect(
    "DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT"
    "=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=kzg03731;PWD=f4Jb4Y6d8YHaha5F",
    '', '')
autocommitstatus = ibm_db.autocommit(conn)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password1 = request.form['password']

        select_sql = 'SELECT fname FROM USER_DETAILS WHERE email=? AND password1=?'
        stmt = ibm_db.prepare(conn, select_sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.bind_param(stmt, 2, password1)
        ibm_db.execute(stmt)
        d = ibm_db.fetch_assoc(stmt)

        if d:
            return render_template('sample.html', message="Welcome" + " " + d['FNAME'])
        else:
            return render_template('sample.html', message="Invalid Username or Password")


@app.route('/register')
def register_form():
    return render_template('registrations/user_registration.html')


@app.route('/formreg', methods=['POST', 'GET'])
def addform():
    if request.method == "POST":
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        phonenumber = request.form['phonenumber']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if password2 != password1:
            flag2 = True

        sql = 'SELECT * FROM USER_DETAILS WHERE email=?'
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        flag = ibm_db.fetch_assoc(stmt)

        if flag:
            return render_template('sample.html', message='User already exist')
        else:
            insert_sql = "INSERT INTO USER_DETAILS VALUES (?, ?, ?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, fname)
            ibm_db.bind_param(prep_stmt, 2, lname)
            ibm_db.bind_param(prep_stmt, 3, email)
            ibm_db.bind_param(prep_stmt, 4, phonenumber)
            ibm_db.bind_param(prep_stmt, 5, password1)
            ibm_db.execute(prep_stmt)

            return render_template('sample.html', message='New User Created')
