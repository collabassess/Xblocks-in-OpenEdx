sudo git clone git+https://repo_url.git
sudo -u edxapp /edx/bin/pip.edxapp install location/of/xblock/with/setup.py/file --no-deps


--upgrade --no-deps to upgrade


important note: please use --no-deps, else openedx installation breaks

e.g:
cd /edx/app/edxapp/
sudo -u edxapp /edx/bin/pip.edxapp install Xblocks-in-OpenEdx/togetherjsxblock --upgrade --no-deps


restart lms and cms after install/upgrade(be careful this might break the openedx installation if --no-deps not used)
sudo /edx/bin/supervisorctl restart edxapp:*

//just check status:

sudo /edx/bin/supervisorctl status edxapp:*
