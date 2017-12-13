"""TO-DO: Write a description of what this XBlock is."""
# import datetime
# import pytz
# import json
# import logging
# # import io
#
# log = logging.getLogger(__name__)
#
# logging.basicConfig(level = logging.ERROR)
#
# logging.disable(logging.CRITICAL)
# logging.disable(logging.DEBUG)
# logging.disable(logging.INFO)


import pkg_resources
from xblock.core import XBlock
from xblock.fields import Integer, Scope,String, DateTime, Boolean
from xblock.fragment import Fragment
from xblockutils.studio_editable import StudioEditableXBlockMixin
import mysql.connector
import settings as s
from mysql.connector import errorcode


# @XBlock.needs('fs')
@XBlock.needs("i18n")
@XBlock.wants('user')
class TogetherJsXBlock(StudioEditableXBlockMixin,XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    room = String(
        default="room", scope=Scope.settings,
        help="A chat room number",
    )
    s_name = String(default="a", scope=Scope.settings, help="user name")

    editable_fields = ('s_name','room')
    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.



    # fs = Filesystem(help="File system", scope=Scope.user_state_summary)

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the TogetherJsXBlock, shown to students
        when viewing courses.
        """

        html = self.resource_string("static/html/togetherjsxblock.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/togetherjsxblock.css"))
        frag.add_javascript(self.resource_string("static/js/togetherjs-min.js"))
        frag.add_javascript(self.resource_string("static/js/src/togetherjsxblock.js"))
        frag.initialize_js('TogetherJsXBlock')
        # frag.initialize_js('TogetherJsXBlock', {'up': self.upvotes,
        #                                        'down': self.downvotes})
        return frag


    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def returnRoom(self, data, suffix=''):
        """
        a handler which returns the chat room name.
        """
        cnx = mysql.connector.connect(**s.database)
        cursor = cnx.cursor(buffered=True)
        curr_user = self.get_userid()

        cursor.execute("""
                        SELECT group_id,user1,user2 from user_groups
                        WHERE user1=%s OR user2=%s
                       """, (curr_user, curr_user))

        for (group_id, user1, user2) in cursor:
            log.error("in returnRoom fn")
            self.room = str(str(group_id) + user1 + user2)
            return {"room": self.room}

    @XBlock.json_handler
    def initializeRoom(self,data,suffix=''):
        """
                A handler, which intializes room for the collaboration partners and syncs with mysql backend.
        """
        cnx = mysql.connector.connect(**s.database)
        cursor = cnx.cursor(buffered=True)
        curr_user = self.get_userid()

        cursor.execute("""
                           SELECT * from user_groups
                           WHERE user1=%s OR user2=%s
                       """, (curr_user, curr_user))

        if not cursor.rowcount:
            # log.error("No results found")
            cursor.execute("""
                           SELECT * from user_groups
                           WHERE user1 IS NULL OR user2 IS NULL
                            """)
            if not cursor.rowcount:
                # log.error("New row created")
                cursor.execute("""
                                   INSERT INTO user_groups(course_id,user1) VALUES (%s,%s)
                               """,
                               ('1', curr_user))
                cnx.commit()
            else:
                # log.error("Old row updated")
                for (group_id, course_id, user1, user2) in cursor:
                    if user1 is None:
                        # log.error("User1 updated")
                        cursor.execute("""
                                        UPDATE user_groups
                                        SET user1=%s
                                        WHERE group_id=%s && course_id=%s
                                       """,
                                       (curr_user, group_id, course_id))
                        cnx.commit()
                    elif user2 is None:
                        # log.error("User2 updated")
                        cursor.execute("""
                                        UPDATE user_groups
                                        SET user2=%s
                                        WHERE group_id=%s && course_id=%s
                                       """,
                                       (curr_user, group_id, course_id))
                        cnx.commit()
        cursor.close()
        cnx.close()


    @XBlock.json_handler
    def returnUserName(self, data, suffix=''):
        """
           a handler which returns user name.
        """
        return {"s_name": self.get_username().full_name}

    def get_username(self):
        """Get an attribute of the current user."""
        user_service = self.runtime.service(self, 'user')
        if user_service:
            # May be None when creating bok choy test fixtures
            return user_service.get_current_user()
        return None

    def get_userid(self):
        user_service = self.runtime.service(self, 'user')
        if user_service:
            # May be None when creating bok choy test fixtures
            try:
                return user_service.opt_attrs['edx-platform.user_id']
            except:
                return '2'
   # def get_sql_access(self):


    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("TogetherJsXBlock",
             """<togetherjsxblock/>
             """),
            ("Multiple TogetherJsXBlock",
             """<vertical_demo>
                <togetherjsxblock/>
                <togetherjsxblock/>
                <togetherjsxblock/>
                </vertical_demo>
             """),
        ]
