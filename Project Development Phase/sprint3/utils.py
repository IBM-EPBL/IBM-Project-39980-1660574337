import ibm_db
from main import conn


def display_donors(sql):
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.execute(stmt)
    res = []
    dictionary = ibm_db.fetch_assoc(stmt)
    while dictionary:
        for x in dictionary:
            dictionary[x] = str(dictionary[x]).strip()
        res.append(dictionary)
        dictionary = ibm_db.fetch_assoc(stmt)
    return res


def filter_by_one_param(sql, filter_by):
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, filter_by)
    ibm_db.execute(stmt)
    filters = ibm_db.fetch_assoc(stmt)

    res = []
    while filters:
        res.append(filters)
        filters = ibm_db.fetch_assoc(stmt)
    return res


def city_filter(state):
    res = []
    if state is not None:
        sql = 'select distinct CITY from PERSONALDETAILS where STATE=?'
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, state)
    else:
        sql = 'select distinct CITY from PERSONALDETAILS'
        stmt = ibm_db.prepare(conn, sql)
    ibm_db.execute(stmt)
    filters = ibm_db.fetch_assoc(stmt)

    while filters:
        if filters['CITY'] not in res:
            res.append(filters['CITY'])
        filters = ibm_db.fetch_assoc(stmt)
    res.sort()
    return res


def filter_by_two_params(sql, param1, param2):
    res = []
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, param1)
    ibm_db.bind_param(stmt, 2, param2)
    ibm_db.execute(stmt)
    filters = ibm_db.fetch_assoc(stmt)
    while filters:
        res.append(filters)
        filters = ibm_db.fetch_assoc(stmt)
    return res


def filter_by_one(state, city, locality):
    sql = ""
    param1 = ""
    param2 = ""
    param3 = ""
    if city is None and locality is None:
        sql = 'select distinct CITY, LOCALITY from ORGANISATION_DETAILS where APPROVED=\'YES\' and STATE=?'
        param1 = state
        param2 = 'CITY'
        param3 = 'LOCALITY'
    elif state is None and locality is None:
        sql = 'select distinct STATE, LOCALITY from ORGANISATION_DETAILS where APPROVED=\'YES\' and CITY=?'
        param1 = city
        param2 = 'STATE'
        param3 = 'LOCALITY'
    elif state is None and city is None:
        sql = 'select distinct STATE, CITY from ORGANISATION_DETAILS where APPROVED=\'YES\' and LOCALITY=?'
        param1 = locality
        param2 = 'STATE'
        param3 = 'CITY'
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, param1)
    ibm_db.execute(stmt)
    fetch = ibm_db.fetch_assoc(stmt)

    res1, res2 = [], []
    while fetch:
        if fetch[param2] not in res1:
            res1.append(fetch[param2])
        if fetch[param3] not in res2:
            res2.append(fetch[param3])
        fetch = ibm_db.fetch_assoc(stmt)
    d = {'res1': res1, 'res2': res2}
    return d


def filter_by_two(state, city, locality):
    sql = ""
    param1 = ""
    param2 = ""
    param3 = ""
    if locality is None:
        sql = 'select distinct LOCALITY from ORGANISATION_DETAILS where APPROVED=\'YES\' and STATE=? and CITY=?'
        param1 = state
        param2 = city
        param3 = 'LOCALITY'
    elif city is None:
        sql = 'select distinct CITY from ORGANISATION_DETAILS where APPROVED=\'YES\' and STATE=? and LOCALITY=?'
        param1 = state
        param2 = locality
        param3 = 'CITY'
    elif state is None:
        sql = 'select distinct STATE from ORGANISATION_DETAILS where APPROVED=\'YES\' and CITY=? and LOCALITY=?'
        param1 = city
        param2 = locality
        param3 = 'STATE'
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, param1)
    ibm_db.bind_param(stmt, 2, param2)
    ibm_db.execute(stmt)
    fetch = ibm_db.fetch_assoc(stmt)

    res = []
    while fetch:
        if fetch[param3] not in res:
            res.append(fetch[param3])
        fetch = ibm_db.fetch_assoc(stmt)
    return res


def display_all_option(sql):
    res1, res2, res3 = [], [], []
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.execute(stmt)
    fetch = ibm_db.fetch_assoc(stmt)

    while fetch:
        if fetch['STATE'] not in res1:
            res1.append(fetch['STATE'])
        if fetch['CITY'] not in res2:
            res2.append(fetch['CITY'])
        if fetch['LOCALITY'] not in res3:
            res3.append(fetch['LOCALITY'])
        fetch = ibm_db.fetch_assoc(stmt)

    d = {'res1': res1, 'res2': res2, 'res3': res3}
    return d