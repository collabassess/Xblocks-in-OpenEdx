"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
import logging

from xblock.core import XBlock
from xblock.fields import Integer, Scope,String, DateTime, Boolean
from xblock.fragment import Fragment
from xblockutils.studio_editable import StudioEditableXBlockMixin

log = logging.getLogger(__name__)

logging.basicConfig(level = logging.ERROR)

logging.disable(logging.CRITICAL)
logging.disable(logging.DEBUG)
logging.disable(logging.INFO)
import mysql.connector
import settings as s
from mysql.connector import errorcode

@XBlock.needs("i18n")
@XBlock.wants('user')
class ShareContentXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    count = Integer(
        default=0, scope=Scope.user_state,
        help="A simple counter, to show something happening",
    )
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

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def get_room(self,data,suffix=''):
        cnx = mysql.connector.connect(**s.database)
        cursor = cnx.cursor(buffered=True)
        curr_user = self.get_userid()
        cursor.execute("""
                    SELECT group_id,course_id from user_groups
                    WHERE user1=%s OR user2=%s
                    """,(curr_user,curr_user))
        for (group_id,course_id) in cursor:
            log.error("ye")
            self.room = str(group_id+"-"+course_id)
            return {"room": self.room}

    @XBlock.json_handler
    def increment_count(self, data, suffix=''):
        cnx = mysql.connector.connect(**s.database)
        cursor = cnx.cursor(buffered=True)
        query = ("SELECT * FROM user_groups")
        cursor.execute(query)
        curr_user = self.get_userid()
        for (group_id, course_id, user1,user2) in cursor:
            log.error(group_id+","+course_id)
            if(user1 == curr_user):
                log.error(user2)
            elif user1 is None:
                log.error("gotcha!")
                cursor.execute("""
                                UPDATE user_groups
                                SET user1=%s
                                WHERE group_id=%s && course_id=%s
                                """,(curr_user,group_id,course_id))
                cnx.commit()
            elif user2 == curr_user:
                log.error(user1)
                log.error("gotcha2")
            elif user2 is None:
                log.error("gotcha4!")
                cursor.execute("""
                                UPDATE user_groups
                                SET user2=%s
                                WHERE group_id=%s && course_id=%s
                                """, (curr_user, group_id,course_id))
                cnx.commit()
            #     continue

        cursor.close()
        cnx.close()
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}

    def get_username(self):
        """Get an attribute of the current user."""
        user_service = self.runtime.service(self, 'user')
        if user_service:
            # May be None when creating bok choy test fixtures
            return user_service.get_current_user()
        return None

    def get_userid(self):
        # user_service = self.runtime.service(self, 'user')
        # if user_service:
        #     # May be None when creating bok choy test fixtures
        #     return user_service.opt_attrs['edx-platform.user_id']
        return '2'

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
