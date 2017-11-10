"""TO-DO: Write a description of what this XBlock is."""
import datetime
import pytz
import pkg_resources
from xblock.core import XBlock
from xblock.fields import Integer, Scope,String, DateTime
from xblock.fragment import Fragment
from xblockutils.studio_editable import StudioEditableXBlockMixin

@XBlock.needs("i18n")
@XBlock.wants('user')
class TogetherJsXBlock(StudioEditableXBlockMixin,XBlock):
    """
    TO-DO: document what your XBlock does.
    """


    room = String(
        default="roomdefault", scope=Scope.settings,
        help="A chat room number",
    )
    s_name = String(default="a", scope=Scope.settings, help="user name")

    editable_fields = ('s_name','room')
    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.


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
        return frag


    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def returnRoom(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # user_service = self.runtime.service(self, 'user')
        # xb_user = user_service.get_current_user()
        # self.s_name = xb_user.full_name
        # Just to show data coming in...
        if(data['hello'] == 'world'):
            return {"room": self.room}
        else:
            return {"s_name": self.s_name}

    # @XBlock.json_handler
    # def returnUserName(self, data, suffix=''):
    #     """
    #     return current user data
    #     """
    #     user_service = self.runtime.service(self, 'user')
    #     xb_user = user_service.get_current_user()
    #     self.s_name = xb_user.full_name
    #     if(self.s_name == "a"):
    #         self.s_name = "b"
    #     return {"s_name":self.s_name}


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
