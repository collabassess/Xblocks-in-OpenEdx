user1 : staff@example.com
user2: aat@example.com

pw: edx


## create new user(super user with access to lms, cms and django administration):

<ul>

<li>cd /edx/app/edxapp/edx-platform
<li>sudo su -s /bin/bash edxapp
<li>cd
<li>/edx/bin/python.edxapp /edx/bin/manage.edxapp lms manage_user <i>[__Username__]</i> <i>[__user email__]</i> --staff --superuser --settings=aws
<li>exit
<li>cd /edx/app/edxapp/edx-platform
<li>sudo -u www-data /edx/bin/python.edxapp ./manage.py lms --settings aws changepassword <i>[__Username__]</i>
<li><i> ---- enter new password ----
<li><i> ---- re-enter new password -----
