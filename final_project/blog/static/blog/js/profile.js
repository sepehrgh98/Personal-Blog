$(".card").mouseover(function(){
    x = $(this);
    y = x.attr('id');
    y = y.substring(1);
    $("#-"+y).css('display', 'flex');
  });
$(".card").mouseleave(function(){
    x = $(this);
    y = x.attr('id');
    y = y.substring(1);
    $("#-"+y).css('display', 'none');
  });

var switchStatus ;
$("#togBtn").on('change', function() {
    post_id = $('.activation').attr('id');
    console.log(post_id)
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    if ($(this).is(':checked')) {
        switchStatus = $(this).is(':checked');
        console.log(switchStatus);
        $.ajax({
         type: "POST",
         url : "http://127.0.0.1:8000/blog/ActivePostAPI/",
         data: {
             "active_state": switchStatus,
             "post_id":post_id
         },
         headers: {'X-CSRFToken': csrftoken},
         success : function (data) {
            console.log("wiiiiiiiin")
         }

    });
    }
    else {
       switchStatus = $(this).is(':checked');
       console.log(switchStatus);
       $.ajax({
         type: "POST",
         url : "http://127.0.0.1:8000/blog/ActivePostAPI/",
         data: {
             "active_state": switchStatus,
             "post_id":post_id
         },
         headers: {'X-CSRFToken': csrftoken},
         success : function (data) {
            console.log("wiiiiiiiin")
         }

    });
    }
});