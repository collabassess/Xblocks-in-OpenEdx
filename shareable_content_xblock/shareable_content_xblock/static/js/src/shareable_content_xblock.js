/* Javascript for ShareContentXBlock. */
function ShareContentXBlock(runtime, element) {

    function updateCount(result) {
        $('.count', element).text(result.count);
    }

    function updateRoom(result) {
        $('.room', element).text(result.room);
    }
    var handlerUrl = runtime.handlerUrl(element, 'increment_count');

    $('p', element).click(function(eventObject) {
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"hello": "world"}),
            success: updateCount
        });
    });

    var handlerUrl1 = runtime.handlerUrl(element, 'get_room');

    $('p', element).click(function(eventObject) {
        $.ajax({
            type: "POST",
            url: handlerUrl1,
            data: JSON.stringify({"hello": "world"}),
            success: updateRoom
        });
    });

    $(function ($) {
        /* Here's where you'd do things on page load. */
    });
}
