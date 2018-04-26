# ldap-toolbox
Preview of the different files :

- utils.py :

This file contain all the commons functions of the project (ldap_start_connection, ldap_stop_connection, load_config).

- find_inactive.py :

This file search into your Active Directory if you have user for which the last connection is older than 2 month. 
Its an output file, no input are required.

- cleaner.py

This file is a huge process file about cleaning old user from the Active Directory. 
Multiple actions can be done with it : search user in AD
                                       add group(memberOf) to a user 
                                       set new Primary Group to a user 
                                       search all the groups(memberOf) of a user 
                                       delete a user from all his groups 
                                       disable the user 
                                       move the user in a different OU 

For some function you will need to modify the following value : add_user_to_group(DN of your memberOf)
                                                                modify_primary_group(ID of the memberOf) 
                                                                move_user(Path of the new OU) 

It will depend on you Active Directory configuration
This file take an input which is the login of the user you want to disable.

- find_group_dn.py 

This file find the DN(DistinguishedName) of a group by searching his CN(Common Name).
This file take an input which is the CN of the required group.
