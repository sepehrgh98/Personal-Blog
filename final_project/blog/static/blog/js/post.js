$(".comment_btn").on("click", function(){
    x = $(this);
    var elmId = x.closest('div').attr('class');
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    elmId = elmId[elmId.length -1];
    y = $('.textarea-'+elmId)
    var txt = y.val();
    var btn = $('.'+elmId+' .comment_btn')
    console.log(btn)
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

$("#com_box textarea").on("keyup", function(){
    var myID = $(this).attr('class');
    myID = myID[myID.length -1];
    var z = $('.'+myID+' button');
    z.attr('disabled', true);
    if($(this).val() != ''){
         z.attr('disabled', false);

    } else {
         z.attr('disabled', true);
    }
});