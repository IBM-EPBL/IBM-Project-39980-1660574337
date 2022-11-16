import ibm_db
from main import conn
import datetime


def donor_req_count(donor_email):
    sql = 'select count(DONOR_EMAIL) from DONATE_REQUESTS where DONOR_EMAIL=?'
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, donor_email)
    ibm_db.execute(stmt)
    return ibm_db.fetch_assoc(stmt)


def donate_req(donor_email, org_email, org_name, b_group, donor_name, donor_contact):
    date_format = "%Y-%m-%d %H:%M:%S"

    sql = 'insert into DONATE_REQUESTS values (?, ?, ?, ?, ?, ?, ?, ?)'
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, donor_email)
    ibm_db.bind_param(stmt, 2, org_email)
    ibm_db.bind_param(stmt, 3, 'PENDING')
    ibm_db.bind_param(stmt, 4, datetime.datetime.strftime(datetime.datetime.now(), date_format))
    ibm_db.bind_param(stmt, 5, org_name)
    ibm_db.bind_param(stmt, 6, b_group)
    ibm_db.bind_param(stmt, 7, donor_name)
    ibm_db.bind_param(stmt, 8, donor_contact)
    ibm_db.execute(stmt)


def donors_info(email):
    sql = 'select * from PERSONALDETAILS where EMAIL=?'
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, email)
    ibm_db.execute(stmt)
    fetch = ibm_db.fetch_assoc(stmt)
    d = {'B_group': fetch['BLOODGROUP'], 'Name': fetch['FIRSTNAME']+' '+fetch['LASTNAME'], 'Contact': fetch['PHONENUMBER']}
    return d