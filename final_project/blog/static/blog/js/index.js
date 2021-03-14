//function mylikes(x) {
//    x.style.backgroundColor = "green";
//}
//function mydislikes(x) {
//    x.style.backgroundColor = "red";
//
//}
$('#mylikes').click( function() {
    x = $(this)
    var elmId = x.closest('div').attr('id');
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
            type: "POST",
             url : "http://127.0.0.1:8000/blog/likeapi/",
             dataType: "json",
             data: {
                "post_id": elmId
             },
             headers: {'X-CSRFToken': csrftoken},
             success : function (data) {
                       console.log("win");
                    },
             error: function (data) {
                       console.log("loss");
                    }
                 });
             });