/* Javascript for TogetherJsXBlock. */
function TogetherJsXBlock(runtime, element) {

    function updateRoom(result) {
        $('.room', element).text(result.room);
        TogetherJSConfig_findRoom = {prefix:result.room, max: 2};
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
        TogetherJS.config("getUserName", function () {
              return 'Ajay';
            });

        TogetherJS.config("dontShowClicks",function(){
            return true;
        });

        var handlerUrl = runtime.handlerUrl(element, 'returnRoom');

        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"hello": "world"}),
            success: updateRoom
        });
    });
}
