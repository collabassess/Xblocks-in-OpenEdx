/* Javascript for TogetherJsXBlock. */
function TogetherJsXBlock(runtime, element) {

    function updateRoom(result) {
        $('.room', element).text(result.room);
        TogetherJSConfig_findRoom = {prefix:result.room, max: 2};

    }

    function updateUserName(result) {
        TogetherJSConfig_getUserName = result.s_name;
        alert(result.s_name+" it works");
//        TogetherJS.config("suppressJoinConfirmation", function () {
//          return true;
//        });
    }


    $('#collaborate').click(function(){
        TogetherJS();
    });


    $(function ($) {
        TogetherJS.config("disableWebRTC", function () {
              return true;
            });
        TogetherJS.config("suppressInvite", function () {
          return true;
        });
        TogetherJS.config("suppressJoinConfirmation", function () {
          return true;
        });
        TogetherJSConfig_hubBase = "https://calm-escarpment-25279.herokuapp.com/";

        TogetherJS.config("dontShowClicks",function(){
            return true;
        });

        var handlerUrl = runtime.handlerUrl(element, 'returnRoom');
        //var handlerStudentUrl = runtime.handlerUrl(element, 'returnUserName');

        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"hello": "world"}),
            success: updateRoom
        });

//        $.ajax({
//            type: "POST",
//            url: handlerUrl,
//            data: JSON.stringify({"hello": "world1"}),
//            success: updateUserName
//        });

    });
}
