/* Javascript for ShareContentXBlock. */
function ShareContentXBlock(runtime, element) {


    $("#stu_sol").click(function(){
        var dataString = $('#stu_form').serializeArray().reduce(function(obj, item) {
                        obj[item.name] = item.value;
                        return obj;
                    }, {});
        $(".solution").text("hint is: "+dataString.user1);
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'submit_ans'),
            data: JSON.stringify(dataString),
            success: function(result){
                console.log(result);
            }
        });



    });

    function get_ans_ptnr(){
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'get_ans_ptnr'),
            data:JSON.stringify({"hello": "world"}),
            success: function(result){
                SelectRadioButton("user2",result[0]);
                $(".solution2").text("hint is: "+result[0]);
            }
        });
    }

    function check_ans_self(){
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'get_ans_self'),
            data:JSON.stringify({"hello": "world"}),
            success: function(result){
                SelectRadioButton("user1",result[0]);
                $(".solution").text("hint is: "+result[0]);
            }
        });
    }

    function SelectRadioButton(name, value) {

      $("input[name='"+name+"'][value='"+value+"']").prop('checked', true);

      return false; // Returning false would not submit the form

    }

    function get_partner(){
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'get_ptnr_id'),
            data:JSON.stringify({"hello": "world"}),
            success: function(result){
            console.log("partner is "+result[0]);
            }
        });
    }



    $(function ($) {


         get_partner();

         check_ans_self();

         get_ans_ptnr();

         //setInterval(get_ans_ptnr, 1000);


    });
}
