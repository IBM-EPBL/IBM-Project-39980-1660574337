from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from sprint3.utils import *
from sprint4.utils import donor_req_count, donate_req, donors_info
import datetime

sprint4 = Blueprint('sprint4', __name__, template_folder='templates', static_folder='static', static_url_path='/sprint4/static')


@sprint4.route('/donate-plasma', methods=['POST', 'GET'])
def donate():
    if 'user' in session:
        if request.method == 'POST':
            response = dict()
            select = request.json
            if 'state' in select and 'city' in select and 'locality' in select:
                if select['state'] != 'all' and select['city'] == 'all' and select['locality'] == 'all':
                    sql = 'select * from ORGANISATION_DETAILS where APPROVED=\'YES\' and STATE=? order by NAME'
                    response['filter'] = filter_by_one_param(sql, select['state'])
                    temp = filter_by_one(select['state'], None, None)
                    response['filterCity'] = temp['res1']
                    response['filterLocality'] = temp['res2']
                    response['filter_city_select'] = 'YES'
                    response['filter_locality_select'] = 'YES'
                    return jsonify(response)

                elif select['state'] != 'all' and select['city'] != 'all' and select['locality'] == 'all':
                    sql = 'select * from ORGANISATION_DETAILS where APPROVED=\'YES\' and STATE=? and CITY=? order by NAME'
                    response['filter'] = filter_by_two_params(sql, select['state'], select['city'])
                    response['filter_locality_select'] = 'YES'
                    response['filterLocality'] = filter_by_two(select['state'], select['city'], None)
                    return jsonify(response)

                elif select['state'] != 'all' and select['city'] == 'all' and select['locality'] != 'all':
                    sql = 'select * from ORGANISATION_DETAILS where APPROVED=\'YES\' and STATE=? and LOCALITY=? order by NAME'
                    response['filter'] = filter_by_two_params(sql, select['state'], select['locality'])
                    response['filter_city_select'] = 'YES'
                    response['filterLocality'] = filter_by_two(select['state'], None, select['locality'])
                    return jsonify(response)

                elif select['state'] == 'all' and select['city'] != 'all' and select['locality'] == 'all':
                    sql = 'select * from ORGANISATION_DETAILS where APPROVED=\'YES\' and CITY=? order by NAME'
                    response['filter'] = filter_by_one_param(sql, select['city'])
                    temp = filter_by_one(None, select['city'], None)
                    response['filter_locality_select'] = 'YES'
                    response['filter_state_select'] = 'YES'
                    response['filterState'] = temp['res1']
                    response['filterLocality'] = temp['res2']
                    return jsonify(response)

                elif select['state'] == 'all' and select['city'] != 'all' and select['locality'] != 'all':
                    sql = 'select * from ORGANISATION_DETAILS where APPROVED=\'YES\' and CITY=? and LOCALITY=? order by NAME'
                    response['filter'] = filter_by_two_params(sql, select['city'], select['locality'])
                    response['filter_state_select'] = 'YES'
                    response['filterState'] = filter_by_two(None, select['city'], select['locality'])
                    return jsonify(response)

                elif select['state'] == 'all' and select['city'] == 'all' and select['locality'] != 'all':
                    sql = 'select * from ORGANISATION_DETAILS where APPROVED=\'YES\' and LOCALITY=? order by NAME'
                    response['filter'] = filter_by_one_param(sql, select['locality'])
                    temp = filter_by_one(None, None, select['locality'])
                    response['filter_state_select'] = 'YES'
                    response['filter_city_select'] = 'YES'
                    response['filterState'] = temp['res1']
                    response['filterCity'] = temp['res2']
                    return jsonify(response)

                elif select['state'] == 'all' and select['city'] == 'all' and select['locality'] == 'all':
                    sql = 'select * from ORGANISATION_DETAILS where APPROVED=\'YES\' order by NAME'
                    response['filter'] = display_donors(sql)
                    response['filter_state_select'] = 'YES'
                    response['filter_city_select'] = 'YES'
                    response['filter_locality_select'] = 'YES'
                    temp = display_all_option(sql)
                    response['filterState'] = temp['res1']
                    response['filterCity'] = temp['res2']
                    response['filterCity'] = temp['res3']
                    return jsonify(response)

                sql = 'select * from ORGANISATION_DETAILS where APPROVED=\'YES\' and STATE=? and CITY=? and LOCALITY=? order by NAME'
                stmt = ibm_db.prepare(conn, sql)
                ibm_db.bind_param(stmt, 1, select['state'])
                ibm_db.bind_param(stmt, 2, select['city'])
                ibm_db.bind_param(stmt, 3, select['locality'])
                ibm_db.execute(stmt)
                fetch = ibm_db.fetch_assoc(stmt)

                res = []
                while fetch:
                    res.append(fetch)
                    fetch = ibm_db.fetch_assoc(stmt)
                response['filter'] = res
                return jsonify(response)
            elif 'email' in select:
                counter = donor_req_count(session['donor-email'])

                date_format = "%Y-%m-%d %H:%M:%S"
                if counter['1'] < 5:
                    temp = donors_info(session['donor-email'])
                    if counter['1'] == 0:
                        donate_req(session['donor-email'], select['email'], select['name'], temp['B_group'], temp['Name'], temp['Contact'])
                        response['donate_req_status'] = 'Success'
                    else:
                        sql = 'select ORG_EMAIL from DONATE_REQUESTS where DONOR_EMAIL=? and ORG_EMAIL=?'
                        stmt = ibm_db.prepare(conn, sql)
                        ibm_db.bind_param(stmt, 1, session['donor-email'])
                        ibm_db.bind_param(stmt, 2, select['email'])
                        ibm_db.execute(stmt)
                        fetch = ibm_db.fetch_assoc(stmt)

                        if fetch:
                            response['donate_req_status'] = 'Already'
                        else:
                            donate_req(session['donor-email'], select['email'], select['name'], temp['B_group'], temp['Name'], temp['Contact'])
                            response['donate_req_status'] = 'Success'
                elif counter['1'] >= 5:
                    sql = 'select * from DONATE_REQUESTS where DONOR_EMAIL=?'
                    stmt = ibm_db.prepare(conn, sql)
                    ibm_db.bind_param(stmt, 1, session['donor-email'])
                    ibm_db.execute(stmt)
                    fetch = ibm_db.fetch_assoc(stmt)

                    while fetch:
                        no_of_days = (datetime.datetime.now() - datetime.datetime.strptime(fetch['REQUEST_MADE_TIME'], date_format)).days
                        if fetch['ORG_EMAIL'] == 'email' and no_of_days >= 2:
                            sql2 = 'delete from DONATE_REQUESTS where DONOR_EMAIL=? and ORG_EMAIL=?'
                            stmt2 = ibm_db.prepare(conn, sql2)
                            ibm_db.bind_param(stmt2, 1, session['donor-email'])
                            ibm_db.bind_param(stmt2, 2, fetch['ORG_EMAIL'])
                            ibm_db.execcute(stmt2)
                        fetch = ibm_db.fetch_assoc(stmt)

                    if donor_req_count(session['donor-email'])['1'] < 5:
                        temp = donors_info(session['donor-email'])
                        donate_req(session['donor-email'], select['email'], select['name'], temp['B_group'], temp['Name'], temp['Contact'])
                        response['donate_req_status'] = 'Success'
                    else:
                        response['donate_req_status'] = 'After'
                return response
        else:
            sql = 'select * from ORGANISATION_DETAILS where APPROVED=\'YES\' order by NAME'
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.execute(stmt)
            fetch = ibm_db.fetch_assoc(stmt)

            res, cities, states, locality = [], [], [], []
            while fetch:
                if fetch['CITY'] not in cities:
                    cities.append(fetch['CITY'])
                if fetch['STATE'] not in states:
                    states.append(fetch['STATE'])
                if fetch['LOCALITY'] not in locality:
                    locality.append(fetch['LOCALITY'])
                res.append(fetch)
                fetch = ibm_db.fetch_assoc(stmt)

            states.sort()
            cities.sort()
            locality.sort()
            return render_template('donate.html', res=res, cities=cities, states=states, locality=locality)
    else:
        return redirect(url_for('sprint3.login_as', redirect_to='donor'))


@sprint4.route('/donor-profile', methods=['GET', 'POST'])
def donor_profile():
    if 'user' in session:
        if request.method == 'POST':
            response = dict()
            org_email = request.json
            sql = 'delete from DONATE_REQUESTS where DONOR_EMAIL=? and ORG_EMAIL=?'
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, session['donor-email'])
            ibm_db.bind_param(stmt, 2, org_email['org-email'])
            ibm_db.execute(stmt)

            response['CancelStatus'] = 'True'
            return response
        else:
            sql = 'select * from DONATE_REQUESTS where DONOR_EMAIL=?'
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, session['donor-email'])
            ibm_db.execute(stmt)
            fetch = ibm_db.fetch_assoc(stmt)

            res = []
            while fetch:
                res.append(fetch)
                fetch = ibm_db.fetch_assoc(stmt)
            return render_template('donor_profile.html', res=res)
    else:
        return redirect(url_for('sprint3.login_as', redirect_to='donor'))