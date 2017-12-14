"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
#import logging

from xblock.core import XBlock
from xblock.fields import Integer, Scope,String, DateTime, Boolean
from xblock.fragment import Fragment
from xblockutils.studio_editable import StudioEditableXBlockMixin

# log = logging.getLogger(__name__)
#
# logging.basicConfig(level = logging.ERROR)
#
# logging.disable(logging.CRITICAL)
# logging.disable(logging.DEBUG)
# logging.disable(logging.INFO)
import MySQLdb

@XBlock.needs("i18n")
@XBlock.wants('user')
class ShareContentXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    room = String(
        default="room", scope=Scope.settings,
        help="A chat room number",
    )
    s_name = String(default="a", scope=Scope.settings, help="user name")

    editable_fields = ('s_name', 'room')

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the ShareContentXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/shareable_content_xblock.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/shareable_content_xblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/shareable_content_xblock.js"))

        frag.initialize_js('ShareContentXBlock')
        return frag


    @XBlock.json_handler
    def submit_ans(self, data, suffix=''):
        #log.error(data['user1'])
        sol = data['user1']
        cnx = self.conn_db()
        cursor = cnx.cursor()
        curr_user = self.get_userid()
        cursor.execute("""SELECT * FROM user_hint_solutions where user_id=%s""",str(curr_user))
        if not cursor.rowcount:
            #log.error("New row created"+","+curr_user+","+sol)
            cursor.execute("""
                               INSERT INTO user_hint_solutions
                                VALUES(%s,%s,%s)
                           """, ('1',sol,str(curr_user)))
            cnx.commit()
        else:
            #log.error("update")
            for (Question_id, ans, user_id) in cursor:
                #log.error(Question_id+","+user_id+","+sol)
                #log.error('1,'+curr_user)
                cursor.execute("""
                                UPDATE user_hint_solutions
                                SET ans=%s
                                WHERE Question_id=%s AND user_id=%s
                                """, (sol,'1',curr_user))

                cnx.commit()
                break
        cursor.close()
        cnx.close()
        return "done"

    @XBlock.json_handler
    def get_ans_self(self,data,suffix=''):
        cnx = self.conn_db()
        cursor = cnx.cursor()
        curr_user = self.get_userid()
        cursor.execute("""SELECT ans FROM user_hint_solutions where user_id=%s""", str(curr_user))
        if not cursor.rowcount:
            cursor.close()
            cnx.close()
            return "Not answered yet"
        else:
           # log.error("else")
            for ans in cursor:
               # log.error(ans)
                cursor.close()
                cnx.close()
                return ans
        return "failed"


    @XBlock.json_handler
    def get_ans_ptnr(self,data,suffix=''):
        cnx = self.conn_db()
        cursor = cnx.cursor()
        curr_user = self.get_userid()
        cursor.execute("""SELECT user1,user2 FROM user_groups where user1=%s OR user2=%s""", (curr_user,curr_user))
        if not cursor.rowcount:
            cursor.close()
            cnx.close()
            return "user has no partner"
        else:
           # log.error("else")
            for (user1,user2) in cursor:
             #   log.error(user1+","+user2+":"+curr_user)
                if user1 == curr_user:
                    partner = user2
                else:
                    partner = user1
              #  log.error("partner:"+partner)
                cursor.execute("""
                                SELECT ans FROM user_hint_solutions where user_id=%s AND Question_id='1'
                                """,(partner))
                if not cursor.rowcount:
                    cursor.close()
                    cnx.close()
                    return "partner has not answered yet"
                else:
                    for ans in cursor:
                  #      log.error(ans)
                        cursor.close()
                        cnx.close()
                        return ans
        cursor.close()
        cnx.close()
        return "failed"

    @XBlock.json_handler
    def returnUserName(self, data, suffix=''):
        """
           a handler which returns user name.
        """
        return {"s_name": self.get_user().full_name}

    def conn_db(self):
        return MySQLdb.connect(host='54.156.197.224',user= 'edxapp001',passwd= 'password',db= 'collab_assess')
    def get_user(self):
        """Get an attribute of the current user."""
        user_service = self.runtime.service(self, 'user')
        if user_service:
            # May be None when creating bok choy test fixtures
            return user_service.get_current_user()
        return None

    def get_userid(self):
        try:
            return self.get_user().opt_attrs['edx-platform.user_id']
        except:
            return '4'

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("ShareContentXBlock",
             """<shareable_content_xblock/>
             """),
            ("Multiple ShareContentXBlock",
             """<vertical_demo>
                <shareable_content_xblock/>
                <shareable_content_xblock/>
                <shareable_content_xblock/>
                </vertical_demo>
             """),
        ]
