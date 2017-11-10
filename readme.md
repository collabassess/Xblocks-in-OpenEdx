## Xblocks 
ref: http://edx.readthedocs.io/projects/xblock-tutorial/en/latest/overview/introduction.html
<p>The XBlock specification is a component architecture designed to make it easier to create new online educational experiences. XBlock was developed by edX, which has a focus in education, but the technology can be used in web applications that need to use multiple independent components and display those components on a single web page.

An XBlock developer does not need to download and run the entire edx-platform developer stack or to know anything about the technologies that edX uses to provide the XBlock runtime. Instead, XBlock developers writing with edX in mind can work from the xblock-sdk and deploy their work on any platform that is compatible with XBlocks.

In educational applications, XBlocks can be used to represent individual problems, web-formatted text and videos, interactive simulations and labs, or collaborative learning experiences. Furthermore, XBlocks are composable, allowing an XBlock developer to control the display of other XBlocks to compose lessons, sections, and entire courses.


## Step by step commandline instructions

<pre>
cd working-directory/ </li>
sudo mkdir xblock_development
cd xblock_development/
sudo virtualenv venv
source venv/bin/activate
sudo git clone https://github.com/edx/xblock-sdk.git
cd xblock-sdk/
sudo pip install -r requirements/base.txt
cd -
sudo xblock-sdk/bin/workbench-make-xblock
sudo pip install -e myxblock
sudo mkdir var/
sudo touch var/workbench.log
sudo python xblock-sdk/manage.py migrate
sudo mkdir xblock-sdk/workbench/migrations
sudo vi xblock-sdk/workbench/migrations/initial.py (Note: content of initial.py is attached)
sudo python xblock-sdk/manage.py makemigrations workbench
sudo python xblock-sdk/manage.py migrate
sudo python xblock-sdk/manage.py runserver
</pre>

## code for initial.py:
<pre>
from django.db import migrations, models
class Migration(migrations.Migration):
    operations = [
        migrations.CreateModel(
            name = 'XBlockState',
            fields = [
                ('id', models.AutoField(verbose_name = 'ID', serialize = False, auto_created = True, primary_key = True)),
                ('scope', models.CharField(max_length = 50, blank = True, db_index = True, null = True, choices = [(b' block', 'block'), (b' parent', 'parent'), (b' children', 'children')])),
                ('scope_id', models.CharField(max_length = 255, blank = True, db_index = True, null = True, verbose_name = 'Scope ID')),
                ('user_id', models.CharField(max_length = 255, blank = True, db_index = True, null = True, verbose_name = 'User ID')),
                ('scenario', models.CharField(max_length = 255, blank = True, db_index = True, null = True)),
                ('tag', models.CharField(max_length = 50, blank = True, db_index = True, null = True)),
                ('created', models.DateTimeField(db_index = True, auto_now_add = True)),
                ('state', models.TextField(
                        default = b'{}')),
                    ],
                ),
            ]
</pre>
