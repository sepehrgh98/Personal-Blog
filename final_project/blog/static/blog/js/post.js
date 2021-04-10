$(".comment_btn").on("click", function(){
    x = $(this);
    var elmId = x.closest('div').attr('class');
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    n = elmId.search("_");
    elmId = elmId.substring(n+1, elmId.length);
//    elmId = elmId[elmId.length -1];
    console.log(elmId);
    y = $('.textarea_'+elmId);

    var txt = y.val();
    var btn = $('.'+elmId+' .comment_btn')
    $.ajax({
            type: "POST",
             url : "http://127.0.0.1:8000/blog/CommentAPI/",
             headers: {'X-CSRFToken': csrftoken},
             data: {
                "post_id": elmId,
                "text": txt
             },
             success :function (data) {
             console.log('wiiin');
             y.val('');
             btn.attr('disabled', true);
             },
             error : function (data){
             console.log('looos');
             }
    });
});

$("#comtext").on("keyup", function(){
    var myID = $(this).attr('class');
    console.log(myID)
    n = myID.search("_");
    myID = myID.substring(n+1, myID.length);
    console.log(myID)
    var z = $('.'+myID+' button');
    z.attr('disabled', true);
    if($(this).val() != ''){
         z.attr('disabled', false);

    } else {
         z.attr('disabled', true);
    }
});