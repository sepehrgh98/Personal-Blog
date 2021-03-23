$('.mylikes').click( function() {
    x = $(this)
    var elmId = x.closest('div').attr('id');
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    if(x.css('background-color') == 'rgb(0, 128, 0)'){
        $.ajax({
            type: "POST",
             url : "http://127.0.0.1:8000/blog/UnlikeAPI/",
             data: {
                "post_id": elmId
             },
             headers: {'X-CSRFToken': csrftoken},
             success : function (data) {
             x.css({"background-color": "inherit"});
              console.log("win1");
              $.ajax({
                            type: "GET",
                            url : "http://127.0.0.1:8000/blog/LikeAndDislikeCountAPI/",
                            headers: {'X-CSRFToken': csrftoken},
                            success : function (data) {
                                $.each(data, function( index, value ) {
                                    if (elmId == value['id']){
                                        var mylikecounter = value['like_count']
                                        var mydislikecounter = value['dislike_count']
                                        $('#'+elmId+' .likeCounter').text(mylikecounter);
                                        $('#'+elmId+' .dislikeCounter').text(mydislikecounter);
                                        return false;
                                    }
                                });
                            }

                       });
             },
             error: function (data) {
                     console.log("loss1");
                    }
                 });
    }else{

    $.ajax({
            type: "POST",
             url : "http://127.0.0.1:8000/blog/likeapi/",
             data: {
                "post_id": elmId
             },
             headers: {'X-CSRFToken': csrftoken},
             success : function (data) {
                       console.log("win");
                       x.css({"background-color": "green"});
                       $('#'+elmId+' .mydislikes').css({"background-color": "inherit"});
                       $.ajax({
                            type: "GET",
                            url : "http://127.0.0.1:8000/blog/LikeAndDislikeCountAPI/",
                            headers: {'X-CSRFToken': csrftoken},
                            success : function (data) {
                                $.each(data, function( index, value ) {
                                    if (elmId == value['id']){
                                        var mylikecounter = value['like_count']
                                        var mydislikecounter = value['dislike_count']
                                        $('#'+elmId+' .likeCounter').text(mylikecounter);
                                        $('#'+elmId+' .dislikeCounter').text(mydislikecounter);
                                        return false;
                                    }
                                });
                            }

                       });
                    },
             error: function (data) {
                       console.log("loss");
                    }
                 });
                }
             });

$('.mydislikes').click( function() {
    x = $(this)
    var elmId = x.closest('div').attr('id');
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log(x.css('background-color'))
    if(x.css('background-color') == 'rgb(255, 0, 0)'){
        $.ajax({
            type: "POST",
             url : "http://127.0.0.1:8000/blog/UndislikeAPI/",
             data: {
                "post_id": elmId
             },
             headers: {'X-CSRFToken': csrftoken},
             success : function (data) {
             x.css({"background-color": "inherit"});
              console.log("win1");
              $.ajax({
                            type: "GET",
                            url : "http://127.0.0.1:8000/blog/LikeAndDislikeCountAPI/",
                            headers: {'X-CSRFToken': csrftoken},
                            success : function (data) {
                                $.each(data, function( index, value ) {
                                    if (elmId == value['id']){
                                        var mylikecounter = value['like_count']
                                        var mydislikecounter = value['dislike_count']
                                        $('#'+elmId+' .likeCounter').text(mylikecounter);
                                        $('#'+elmId+' .dislikeCounter').text(mydislikecounter);
                                        return false;
                                    }
                                });
                            }

                       });
             },
             error: function (data) {
                     console.log("loss1");
                    }
                 });
    }else{
    $.ajax({
            type: "POST",
             url : "http://127.0.0.1:8000/blog/dislikeapi/",
             data: {
                "post_id": elmId
             },
             headers: {'X-CSRFToken': csrftoken},
             success : function (data) {
                       console.log("win");
                       x.css({"background-color": "red"});
                       $('#'+elmId+' .mylikes').css({"background-color": "inherit"});
                       $.ajax({
                            type: "GET",
                            url : "http://127.0.0.1:8000/blog/LikeAndDislikeCountAPI/",
                            headers: {'X-CSRFToken': csrftoken},
                            success : function (data) {
                                $.each(data, function( index, value ) {
                                    if (elmId == value['id']){
                                        var mylikecounter = value['like_count']
                                        var mydislikecounter = value['dislike_count']
                                        $('#'+elmId+' .likeCounter').text(mylikecounter);
                                        $('#'+elmId+' .dislikeCounter').text(mydislikecounter);
                                        return false;
                                    }
                                });
                            }

                       });
                    },
             error: function (data) {
                       console.log("loss");
                    }
                 });
                 }
             });

var y = $('.LikeOrDislike')
var elmId = y.parent();

$.each(elmId, function( index, value ) {
var state = $('#'+ value.id +' .LikeOrDislike')
if (state[0].id == 'True'){
    $('#'+value.id+' .mylikes').css({"background-color": "green"});
}else if (state[0].id == 'False'){
    $('#'+value.id+' .mydislikes').css({"background-color": "red"});
}else{
    $('#'+value.id+' .mylikes').css({"background-color": "inherit"});
    $('#'+value.id+' .mydislikes').css({"background-color": "inherit"});
}
});

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
