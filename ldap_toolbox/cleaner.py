#!/usr/bin/env python

import sys

from ldap3 import MODIFY_REPLACE

from ldap_toolbox.utils import ldap_start_connection, ldap_stop_connection, load_config

users_login = sys.argv[1:]
memberOf_id = "id"
old_user_group_dn = "CN=old_user,OU=old_user,DC=hello,DC=com"
old_user_ou_dn = "OU=old_user,DC=hello,DC=com"

def search_user_information(conn, ldap_domain, ldap_domain_ext, user_login):
    """ Get information for the requested user
    """
    try:
        search_base = "dc={}, dc={}".format(ldap_domain, ldap_domain_ext)
        query = "(&(objectclass=user)(objectCategory=person)" \
                "(sAMAccountName={})(userAccountControl=512))".format(user_login)
        attributes = ['distinguishedName', 'displayname']

        conn.search(search_base, query, attributes=attributes)
        user = conn.entries

        if not user:
            raise Exception("users not found")
    except Exception as e:
        raise Exception("unable to search user information :: {}".format(e))
    return user


def add_user_to_group(conn, user_dn, old_user_group_dn):
    """ Add the user to a group
    """
    try:
        conn.extend.microsoft.add_members_to_groups([str(user_dn)], [str(old_user_group_dn)])
    except Exception as e:
        raise Exception("Can't add user to this group :: {}".format(e))


def modify_primary_group(conn, user_dn, memberOf_id):
    """ Change the primary group of the user
    """
    try:
        conn.modify(str(user_dn), {'primaryGroupID': [(MODIFY_REPLACE, [memberOf_id])]})
    except Exception as e:
        raise Exception("Can't set this group as Primary Group :: {}".format(e))


def find_user_groups(conn, ldap_domain, ldap_domain_ext, user_dn):
    """ Find the memberOf of the user
    """
    try:
        search_base = "dc={}, dc={}".format(ldap_domain, ldap_domain_ext)
        query = "(&(objectCategory=group)(member={}))".format(user_dn)
        attributes = ['distinguishedName']

        conn.search(search_base, query, attributes=attributes)
        groups = conn.entries
    except Exception as e:
        raise Exception("No groups found :: {}".format(e))
    return groups


def remove_user_from_groups(conn, user_dn, group_dn):
    """ Delete the memberOf of the user
    """
    try:
        conn.extend.microsoft.remove_members_from_groups([str(user_dn)], [str(group_dn)])
    except Exception as e:
        raise Exception("Can't remove user from groups :: {}".format(e))


def disable_user(conn, user_dn):
    """ Disable the user in the Active Directory
    """
    try:
        conn.modify(str(user_dn), {'userAccountControl': [(MODIFY_REPLACE, ['514'])]})
    except Exception as e:
        raise Exception("Can't disable the user :: {}".format(e))


def move_user(conn, user_dn, user_disp, old_user_ou_dn):
    """ Move the user to another directory
    """
    try:
        conn.modify_dn(str(user_dn), 'CN={}'.format(user_disp), new_superior=str(old_user_ou_dn))
    except Exception as e:
        raise Exception("Can't move the user :: {}".format(e))


def main():
    try:
        ldap_config = load_config()

        conn = ldap_start_connection(ldap_domain_full=ldap_config['domain_full'],
                                     ldap_login=ldap_config['login'],
                                     ldap_password=ldap_config['password'])

        for user_login in users_login:

            user = search_user_information(conn, ldap_domain=ldap_config['domain'],
                                           ldap_domain_ext=ldap_config['domain_ext'],
                                           user_login=user_login)

            user_dn = user[0].distinguishedName
            user_disp = user[0].displayname
            print(user_disp)

            #add_user_to_group(conn, user_dn=user_dn)

            #modify_primary_group(conn, user_dn=user_dn)

            groups = find_user_groups(conn, ldap_domain=ldap_config['domain'],
                                      ldap_domain_ext=ldap_config['domain_ext'],
                                      user_dn=user_dn)

            for group in groups:
                group_dn = group.distinguishedName
                print(group_dn)

                #remove_user_from_groups(conn, user_dn=user_dn, group_dn=group_dn)

            #disable_user(conn, user_dn=user_dn)

            #move_user(conn, user_dn=user_dn, user_disp=user_disp)

        ldap_stop_connection(conn)
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
