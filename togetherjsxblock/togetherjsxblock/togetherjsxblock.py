"""TO-DO: Write a description of what this XBlock is."""
import datetime
import pytz
import json
# import logging
import io

import pkg_resources
from xblock.core import XBlock
from xblock.fields import Integer, Scope,String, DateTime, Boolean
from xblock.fragment import Fragment
from xblockutils.studio_editable import StudioEditableXBlockMixin
# from xblock.reference.plugins import Filesystem

# log = logging.getLogger(__name__);


@XBlock.needs("i18n")
@XBlock.needs('user')
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

    # TO-DO: delete count, and define your own fields.
    # upvotes = 0
    # downvotes = 0

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
        # log.warning('The system may break down')
        # if not self.fs.exists(u"custom.json"):
        #     with self.fs.open(u'custom.json', 'wb') as file_output:
        #         json.dump({
        #             "up": 0,
        #             "down": 0
        #         }, file_output)
        #         file_output.close()
        #
        # votes = json.load(self.fs.open(u"custom.json"))
        # self.upvotes = votes['up']
        # self.downvotes = votes['down']
        user_service = self.runtime.service(self, 'user')
        xb_user = user_service.get_current_user()
        self.s_name = xb_user.full_name

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
        # user_service = self.runtime.service(self, 'user')
        # xb_user = user_service.get_current_user()
        # self.s_name = xb_user.full_name
        # Just to show data coming in...
        if(data['hello'] == 'world'):
            return {"room": self.room}

    @XBlock.json_handler
    def returnUserName(self, data, suffix=''):
        """
           a handler which returns user name.
        """
        return {"s_name": self.s_name}

    # @XBlock.json_handler
    # def vote(self, data, suffix=''):  # pylint: disable=unused-argument
    #     """
    #     Update the vote count in response to a user action.
    #     """
    #     # Here is where we would prevent a student from voting twice, but then
    #     # we couldn't click more than once in the demo!
    #     #
    #     #     if self.voted:
    #     #         log.error("cheater!")
    #     #         return
    #
    #     votes = json.load(self.fs.open(u"custom.json"))
    #     self.upvotes = votes['up']
    #     self.downvotes = votes['down']
    #     if data['voteType'] not in ('up', 'down'):
    #         log.error('error!')
    #         return
    #
    #     if data['voteType'] == 'up':
    #         self.upvotes += 1
    #     else:
    #         self.downvotes += 1
    #
    #     with self.fs.open(u'custom.json', 'wb') as file_output:
    #         json.dump({'up': self.upvotes, 'down': self.downvotes}, file_output)
    #
    #     self.voted = True
    #
    #     return {'up': self.upvotes, 'down': self.downvotes}

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
