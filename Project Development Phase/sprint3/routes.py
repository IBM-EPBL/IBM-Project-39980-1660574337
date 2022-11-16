from flask import Blueprint, render_template, session, request, jsonify, redirect, url_for
from main import csrf, mail
from flask_mail import Message
from sprint3.utils import *

sprint3 = Blueprint('sprint3', __name__, template_folder='templates', static_folder='static', static_url_path='/sprint3/static')


@csrf.exempt
@sprint3.route('/donor-request', methods=['GET', 'POST'])
def donor_request():
    if 'Organisation' in session:
        if request.method == 'POST':    # Filtering Table
            response = dict()
            opt = request.json
            if 'state' in opt and 'city' in opt and 'blood_group' in opt:  # filter by both CITY and STATE
                b_group = ""

                if opt['blood_group'] != 'all':
                    for i in range(len(opt['blood_group'])):
                        if i == 0:
                            b_group += "\'" + opt['blood_group'][i] + "\'"
                        else:
                            b_group += " OR BLOODGROUP=\'" + opt['blood_group'][i] + "\'"

                if opt['state'] != 'all' and opt['city'] == 'all' and opt['blood_group'] == 'all':
                    sql = 'select * from PERSONALDETAILS where STATE=?'
                    response['filters'] = filter_by_one_param(sql, opt['state'])
                    response['filter_by'] = 'State'
                    response['filter1_city'] = city_filter(opt['state'])
                    return jsonify(response)

                elif opt['state'] != 'all' and opt['city'] == 'all' and opt['blood_group'] != 'all':
                    sql = 'select * from PERSONALDETAILS where STATE=? and BLOODGROUP=' + b_group
                    response['filters'] = filter_by_one_param(sql, opt['state'])
                    return jsonify(response)

                elif opt['state'] != 'all' and opt['city'] != 'all' and opt['blood_group'] == 'all':
                    sql = 'select * from PERSONALDETAILS where STATE=? and CITY=?'
                    response['filters'] = filter_by_two_params(sql, opt['state'], opt['city'])
                    return jsonify(response)

                elif opt['state'] == 'all' and opt['city'] != 'all' and opt['blood_group'] == 'all':
                    sql = 'select * from PERSONALDETAILS where CITY=?'
                    response['filters'] = filter_by_one_param(sql, opt['city'])
                    response['filter_by'] = 'State'
                    response['filter1_city'] = city_filter(None)
                    return jsonify(response)

                elif opt['state'] == 'all' and opt['city'] != 'all' and opt['blood_group'] != 'all':
                    sql = 'select * from PERSONALDETAILS where CITY=? and BLOODGROUP=' + b_group
                    response['filters'] = filter_by_one_param(sql, opt['city'])
                    return jsonify(response)

                elif opt['state'] == 'all' and opt['city'] == 'all' and opt['blood_group'] != 'all':
                    print(b_group)
                    sql = 'select * from PERSONALDETAILS where BLOODGROUP=' + b_group
                    response['filters'] = display_donors(sql)
                    return jsonify(response)

                elif opt['state'] == 'all' and opt['city'] == 'all' and opt['blood_group'] == 'all':
                    response['filters'] = display_donors('select * from PERSONALDETAILS')
                    response['filter_by'] = 'State'
                    response['filter1_city'] = city_filter(None)
                    return response

                sql = 'select * from PERSONALDETAILS where STATE=? and CITY=? and BLOODGROUP=' + b_group
                response['filters'] = filter_by_two_params(sql, opt['state'], opt['city'])
                return response

            elif 'emails' in opt:
                for user in opt['emails']:
                    msg = Message('Request For Plasma', sender='noreplyplasmadonor@gmail.com', recipients=[user])
                    msg.body = 'Would you like to make a plasma donation?'
                    try:
                        mail.send(msg)
                        response['mail_sent'] = 'Sent'
                    except Exception:
                        response['mail_sent'] = 'Not Sent'
                        break
            return jsonify(response)

        else:
            b_groups = ['A+ve', 'A-ve', 'B+ve', 'B-ve', 'O+ve', 'O-ve', 'AB+ve', 'AB-ve']

            sql = 'select distinct STATE, CITY from PERSONALDETAILS'
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.execute(stmt)
            states, cities = [], []

            dictionary = ibm_db.fetch_assoc(stmt)
            while dictionary:
                for x in dictionary:
                    dictionary[x] = dictionary[x].strip()
                cities.append(dictionary['CITY'.strip()])
                states.append(dictionary['STATE'].strip())
                dictionary = ibm_db.fetch_assoc(stmt)
            states = list(set(states))
            cities = list(set(cities))
            states.sort()
            cities.sort()
            return render_template('request_page.html', res=display_donors('select * from PERSONALDETAILS'), b_groups=b_groups, states=states, cities=cities)
    else:
        return redirect(url_for('sprint3.login_as', redirect_to='Org'))


@sprint3.route('/org-profile', methods=['GET', 'POST'])
def admin():
    if 'Organisation' in session:
        if request.method == 'POST':
            response = dict()
            data = request.json
            if 'Email' in data:
                sql2 = 'select NAME from ORGANISATION_DETAILS where EMAIL=?'
                stmt2 = ibm_db.prepare(conn, sql2)
                ibm_db.bind_param(stmt2, 1, session['Organisation'])
                ibm_db.execute(stmt2)
                fetch = ibm_db.fetch_assoc(stmt2)
                if data['BtnType'] == 'AccpBtn' or data['BtnType'] == 'declineBtn':
                    msg = Message('Plasma Donation Request Status', sender='noreplyplasmadono', recipients=[data['Email']])
                    if data['BtnType'] == 'AccpBtn':
                        msg.body = f'''Hello! This is {fetch['NAME']}. Your request for plasma donation have been approved.
A mail will be sent shortly for appointment. Thank you'''
                        mail.send(msg)

                        sql = 'update DONATE_REQUESTS set REQUEST_STATUS=\'ACCEPTED\' where DONOR_EMAIL=? and ORG_EMAIL=?'
                        stmt = ibm_db.prepare(conn, sql)
                        ibm_db.bind_param(stmt, 1, data['Email'])
                        ibm_db.bind_param(stmt, 2, session['Organisation'])
                        ibm_db.execute(stmt)
                        response['sent-status'] = 'success'
                    else:
                        msg.body = f'''Hello! This is {fetch['NAME']}. Thank you for your interest of plasma donation.
Sorry to decline this request. Thank you'''
                        mail.send(msg)

                        sql = 'update DONATE_REQUESTS set REQUEST_STATUS=\'DECLINED\' where DONOR_EMAIL=? and ORG_EMAIL=?'
                        stmt = ibm_db.prepare(conn, sql)
                        ibm_db.bind_param(stmt, 1, data['Email'])
                        ibm_db.bind_param(stmt, 2, session['Organisation'])
                        ibm_db.execute(stmt)
                        response['sent-status'] = 'success'
                elif data['BtnType'] == 'ReqBtn':
                    msg = Message('Plasma Donation Request Status', sender='noreplyplasmadono', recipients=[data['Email']])
                    msg.body = f'''Hello! This is {fetch['NAME']}. We're in need of plasma.
If you're interested to donate. Please send your reply to this mail.'''
                    mail.send(msg)
                    response['sent-status'] = 'success'
                return response
            else:
                sql1 = 'select * from ORG_DONOR_REGISTER_TABLE where EMAIL=?'
                stmt1 = ibm_db.prepare(conn, sql1)
                ibm_db.bind_param(stmt1, 1, data['email'])
                ibm_db.execute(stmt1)
                fetch = ibm_db.fetch_assoc(stmt1)
                if fetch:
                    response['status'] = 'Exist'
                    return response

                sql = 'insert into ORG_DONOR_REGISTER_TABLE values (?, ?, ?, ?, ?, ?)'
                stmt = ibm_db.prepare(conn, sql)
                ibm_db.bind_param(stmt, 1, data['fname'])
                ibm_db.bind_param(stmt, 2, data['lname'])
                ibm_db.bind_param(stmt, 3, data['b_group'])
                ibm_db.bind_param(stmt, 4, data['email'])
                ibm_db.bind_param(stmt, 5, data['contact'])
                ibm_db.bind_param(stmt, 6, session['Organisation'])
                ibm_db.execute(stmt)
                response['status'] = 'Done'
                return response
        else:
            sql = 'select NAME from ORGANISATION_DETAILS where EMAIL=?'
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, session['Organisation'])
            ibm_db.execute(stmt)
            fetch = ibm_db.fetch_assoc(stmt)

            details = fetch['NAME']

            sql = 'select * from DONATE_REQUESTS where ORG_EMAIL=? and REQUEST_STATUS=\'PENDING\''
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, session['Organisation'])
            ibm_db.execute(stmt)
            fetch = ibm_db.fetch_assoc(stmt)

            res = []
            while fetch:
                res.append(fetch)
                fetch = ibm_db.fetch_assoc(stmt)

            sql = 'select * from ORG_DONOR_REGISTER_TABLE where "ORG_EMAIl"=?'
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, session['Organisation'])
            ibm_db.execute(stmt)
            fetch = ibm_db.fetch_assoc(stmt)
            res2 = []
            while fetch:
                res2.append(fetch)
                fetch = ibm_db.fetch_assoc(stmt)

            return render_template('org_profile.html', res=res, donors=res2, details=details)
    else:
        return redirect(url_for('sprint3.login_as', redirect_to='Org'))


@sprint3.route('/login-as/<redirect_to>')
def login_as(redirect_to):
    if redirect_to:
        return render_template('login.html')