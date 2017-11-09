/* Javascript for TogetherJsXBlock. */
function TogetherJsXBlock(runtime, element) {

    function updateRoom(result) {
        $('.room', element).text(result.room);
    }



    $('#collaborate').click(function(){
        TogetherJS();
    });


    $(function ($) {

        TogetherJSConfig_findRoom = {prefix: "together", max: 2};
        TogetherJSConfig_disableWebRTC = true;
        TogetherJSConfig_suppressInvite = true;
        TogetherJSConfig_suppressJoinConfirmation =true;
        TogetherJS.config("getUserName", function () {
              return 'Ajay';
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
