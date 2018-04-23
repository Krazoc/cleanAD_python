from ldap3 import Server, Connection, ALL, MODIFY_REPLACE
from ldap3.core.exceptions import LDAPKeyError
import yaml
import os
import sys

userslogin = sys.argv[1:]
olduserdn = "OU=User,OU=Old,DC=Domain,DC=Ext"

#----------------------------------------------------------------------------------------------------------------------#
#                           Load the a file in which you can store your ID/Password and some other information         #
#                           Below we can see that the file in conf.d from my script directory                          #
#----------------------------------------------------------------------------------------------------------------------#
HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, "conf.d/credentials.yaml"), 'r') as stream:
    data_loaded = yaml.load(stream)
    USER = data_loaded['login']
    PASSWORD = data_loaded['Password']
    DOMAIN = data_loaded['Domain']            #The name of your domain (ex : hello)
    EXT = data_loaded['Ext']                  #The extension of your domain (ex : com)
    DOMAINFULL = DOMAIN + "." + EXT           #The full name of your domain, with the extension (ex : hello.com)

#----------------------------------------------------------------------------------------------------------------------#
#                           Initialize the connection to the Active Directory                                          #
#----------------------------------------------------------------------------------------------------------------------#
server = Server(DOMAINFULL, use_ssl=True, get_info=ALL)
with Connection(server, USER, PASSWORD) as conn:

#----------------------------------------------------------------------------------------------------------------------#
#                           Find user information                                                                      #
#----------------------------------------------------------------------------------------------------------------------#
    for userlogin in userslogin:
        conn.search("dc=" + str(DOMAIN) + ", dc=" + str(EXT),
                    "(&(objectclass=user)(objectCategory=person)(sAMAccountName=" + str(userlogin) + ")(userAccountControl=512))",
                    attributes=['distinguishedName', 'displayname'])
        user = conn.entries
        userdn = user[0].distinguishedName
        userdisp = user[0].displayname
        print(userdisp)
        
#----------------------------------------------------------------------------------------------------------------------#
#                           Find Groups in which the user is                                                           #
#----------------------------------------------------------------------------------------------------------------------#
        conn.search("dc=" + str(DOMAIN) + ", dc=" + str(EXT), "(&(objectCategory=group)(member=" + str(userdn) + "))",
                    attributes=['distinguishedName'])
        groups = conn.entries
        for group in groups :
            groupdn = group.distinguishedName
            print(groupdn)
#                           Use the loop to delete the user from all the group
            conn.extend.microsoft.remove_members_from_groups([str(userdn)], [str(groupdn)])

#----------------------------------------------------------------------------------------------------------------------#
#                           Moving the user in a different OU by modifying it's DN                                     #
#----------------------------------------------------------------------------------------------------------------------#
        conn.modify_dn(str(userdn), 'CN=' + str(userdisp), new_superior=str(olduserdn))

#----------------------------------------------------------------------------------------------------------------------#
#                           Disable the user by modifying the userAccountControl to 514                                #
#----------------------------------------------------------------------------------------------------------------------#
        conn.modify(str(userdn),{'userAccountControl': [(MODIFY_REPLACE, ['514'])]})

#----------------------------------------------------------------------------------------------------------------------#
#                           Disconnect from the Active Directory                                                       #
#----------------------------------------------------------------------------------------------------------------------#
conn.unbind()
