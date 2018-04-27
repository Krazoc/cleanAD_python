#!/usr/bin/env python

import sys

from datetime import date, timedelta

from ldap_toolbox.utils import ldap_start_connection, ldap_stop_connection, load_config


def search_user_information(conn, ldap_domain, ldap_domain_ext):
    """ Get information for the requested user
    """
    try:
        search_base = "dc={}, dc={}".format(ldap_domain, ldap_domain_ext)
        query = "(&(objectclass=user)(objectCategory=person)(userAccountControl=512))"
        attributes = ['displayname', 'lastLogon', 'lastLogonTimestamp']

        conn.search(search_base, query, attributes=attributes)
        users = conn.entries
    except Exception as e:
        raise Exception("unable to search user information :: {}".format(e))
    return users


def find_last_date(users):
    """ Grab user if their connection date is older than 2 month
    """
    try:
        for user in users:
            userdisp = user.displayname
            if user.lastLogon:
                userll = date(user.lastLogon[0].year,
                              user.lastLogon[0].month,
                              user.lastLogon[0].day)
            else:
                userll = 'No date'

            if user.lastLogonTimestamp:
                userllts = date(user.lastLogonTimestamp[0].year,
                                user.lastLogonTimestamp[0].month,
                                user.lastLogonTimestamp[0].day)
            else:
                userllts = 'No timestamp date'

            compare_date = date(date.today().year,
                            date.today().month,
                            date.today().day) + timedelta(weeks=-8)

            if (userllts != 'No timestamp date')&(userll != 'No date'):
                if userll > userllts:
                    if userll < compare_date:
                        print(userdisp, userll)
                if userllts > userll:
                    if userllts < compare_date:
                        print(userdisp, userllts)

            if (userll == 'No date')&(userllts != 'No timestamp date'):
                if userllts < compare_date:
                    print(userdisp, userllts)

            if (userllts == 'No timestamp date')&(userll != 'No date'):
                if userll < compare_date:
                    print(userdisp, userll)

            if (userllts == 'No timestamp date')&(userll == 'No date'):
                print(userdisp, userll, userllts)
    except Exception as e:
        raise Exception("A problem occured during the process of the date :: {}".format(e))


def main():
    try:
        ldap_config = load_config()

        conn = ldap_start_connection(ldap_domain_full=ldap_config['domain_full'],
                                     ldap_login=ldap_config['login'],
                                     ldap_password=ldap_config['password'])

        users = search_user_information(conn, ldap_domain=ldap_config['domain'],
                                        ldap_domain_ext=ldap_config['domain_ext'])

        find_last_date(users=users)

        ldap_stop_connection(conn)
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
