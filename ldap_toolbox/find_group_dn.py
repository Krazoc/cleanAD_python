#!/usr/bin/env python

import sys

from ldap_toolbox.utils import ldap_start_connection, ldap_stop_connection, load_config

group_cn = input()
print(group_cn)


def search_group_dn(conn, ldap_domain, ldap_domain_ext, group_cn):
    """ Get information for the requested group
    """
    try:
        search_base = "dc={}, dc={}".format(ldap_domain, ldap_domain_ext)
        query = "(&(objectCategory=group)(cn={}))".format(group_cn)
        attributes = ['distinguishedName']

        conn.search(search_base, query, attributes=attributes)
        group = conn.entries
        group_dn = group[0].distinguishedName
        print(group_dn)
    except Exception as e:
        raise Exception("unable to search group information :: {}".format(e))
    return group_dn


def main():
    try:
        ldap_config = load_config()

        conn = ldap_start_connection(ldap_domain_full=ldap_config['domain_full'],
                                     ldap_login=ldap_config['login'],
                                     ldap_password=ldap_config['password'])

        search_group_dn(conn, ldap_domain=ldap_config['domain'],
                        ldap_domain_ext=ldap_config['domain_ext'],
                        group_cn=group_cn)

        ldap_stop_connection(conn)

    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
