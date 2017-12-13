/* Javascript for TogetherJsXBlock. */
function TogetherJsXBlock(runtime, element, data) {

    r = "";
    function updateRoom(result) {
        console.log(result.room);
        this.r = result.room;
        $('.room', element).text(result.room);
        TogetherJSConfig_findRoom = {prefix:result.room, max: 2};
        TogetherJS.config("findRoom", function () {
          return {prefix:result.room, max: 2};
        });
        alert("room added:"+result.room)
    }

    function updateUserName(result) {
        TogetherJS.config("getUserName", function () {
          return result.s_name;
        });
        TogetherJS.config("suppressJoinConfirmation", function () {
          return true;
        });

        //alert(result.s_name+" it works");
        //TogetherJS();
    }


    $('#collaborate').click(function(){
           TogetherJS();

           //initialize chat rooms
            $.ajax({
                type: "POST",
                url: runtime.handlerUrl(element, 'initializeRoom'),
                data: JSON.stringify({"hello": "world1"})
            });

            //update room name
            var handlerUrl = runtime.handlerUrl(element, 'returnRoom');
            $.ajax({
                type: "POST",
                url: handlerUrl,
                data: JSON.stringify({"hello": "world"}),
                success: updateRoom
            });
    });

    $("#check").click(function(){
        alert(TogetherJS.running);
    });


    $(function ($) {
//        updateVotes(data)

        TogetherJS.config("disableWebRTC", function () {
              return true;
            });
        TogetherJS.config("suppressInvite", function () {
          return true;
        });
        TogetherJS.config("suppressJoinConfirmation", function () {
          return true;
        });
        TogetherJSConfig_cloneClicks = "button.submit";
        TogetherJS.config("cloneClicks", function () {
          return "button.submit";
        });

        TogetherJS.config("includeHashInUrl", function () {
          return true;
        });

        TogetherJSConfig_hubBase = "https://calm-escarpment-25279.herokuapp.com/";

        TogetherJS.config("dontShowClicks",function(){
            return true;
        });



        var handlerStudentUrl = runtime.handlerUrl(element, 'returnUserName');
        $.ajax({
            type: "POST",
            url: handlerStudentUrl,
            data: JSON.stringify({"hello": "world1"}),
            success: updateUserName,
            error: function (request, status, error) {
                alert(error);
                alert(status);
                alert(request.responseText);
            }
        });




    });



//
//    function updateVotes(votes) {
//        $('.upvote .count', element).text(votes.up);
//        $('.downvote .count', element).text(votes.down);
//    }
//
//    var handlerUrl = runtime.handlerUrl(element, 'vote');
//
//    $('.upvote', element).click(function(eventObject) {
//        $.ajax({
//            type: "POST",
//            url: handlerUrl,
//            data: JSON.stringify({voteType: 'up'}),
//            success: updateVotes
//        });
//    });
//
//    $('.downvote', element).click(function(eventObject) {
//        $.ajax({
//            type: "POST",
//            url: handlerUrl,
//            data: JSON.stringify({voteType: 'down'}),
//            success: updateVotes
//        });
//    });


}
