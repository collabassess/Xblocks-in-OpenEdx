## Creating new users:

### Login to the ubuntu system with openedx(ginko.1 release at this time):
<pre>
cd /edx/app/edxapp/
sudo git clone https://repo_url.git
sudo -u edxapp /edx/bin/pip.edxapp install location/of/xblock/with/setup.py/file --no-deps
</pre>

--upgrade --no-deps to upgrade
> important note: please use --no-deps, else openedx installation breaks

> e.g:
<pre>
cd /edx/app/edxapp/
sudo git clone https://github.com/collabassess/Xblocks-in-OpenEdx.git
sudo -u edxapp /edx/bin/pip.edxapp install Xblocks-in-OpenEdx/togetherjsxblock --upgrade --no-deps
</pre>

### restart lms and cms after install/upgrade
> ### (be careful this might break the openedx installation if --no-deps not used)

<pre>
sudo /edx/bin/supervisorctl restart edxapp:*

//just check status:

sudo /edx/bin/supervisorctl status edxapp:*

</pre>
