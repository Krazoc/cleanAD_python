import os
import yaml
import sys

from ldap3 import Server, Connection, ALL


def load_config():
    ldap_config = {}
    """ Read a yaml file from an environment variable to get information
    """
    stream = os.environ.get("LDAP_TOOLBOX_CONFIG_FILE")
    with open(stream) as file:
        data_loaded = yaml.load(file)
        ldap_config['login'] = data_loaded['login']
        ldap_config['password'] = data_loaded['password']
        ldap_config['domain'] = data_loaded['domain']  # The name of your domain (ex : hello)
        ldap_config['domain_ext'] = data_loaded['domain_ext']  # The extension of your domain (ex : com)
        ldap_config['domain_full'] = "{}.{}".format(ldap_config['domain'], ldap_config['domain_ext'])  # The full name of your domain (ex : hello.com)
    return ldap_config


def ldap_start_connection(ldap_domain_full, ldap_login, ldap_password):
    """ Start the connection to the Active Directory
    """
    try:
        server = Server(ldap_domain_full, use_ssl=True, get_info=ALL)
        conn = Connection(server, ldap_login, ldap_password)
        conn.bind()
        return conn
    except Exception as e:
        raise Exception("unable to init ldap connection :: {}".format(e))


def ldap_stop_connection(conn):
    """ Stop the Connection to the Active Directory
    """
    try:
        conn.unbind()
    except Exception as e:
        raise Exception("Can't unbind connection to Active Directory :: {}".format(e))


def main():
    try:
        ldap_config = load_config()

        conn = ldap_start_connection(ldap_domain_full=ldap_config['domain_full'],
                                     ldap_login=ldap_config['login'],
                                     ldap_password=ldap_config['password'])

        ldap_stop_connection(conn)
        print('ok')
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
