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
console.log(state[0].id)
if (state[0].id == 'True'){
    $('#'+value.id+' .mylikes').css({"background-color": "green"});
}else if (state[0].id == 'False'){
    $('#'+value.id+' .mydislikes').css({"background-color": "red"});
}else{
    $('#'+value.id+' .mylikes').css({"background-color": "inherit"});
    $('#'+value.id+' .mydislikes').css({"background-color": "inherit"});
}
});

