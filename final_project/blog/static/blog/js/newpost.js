
$(document).on("click", "i.del" , function() {
	$(this).parent().remove();
});
$(function() {
    $(document).on("change",".uploadFile", function()
    {
    		var uploadFile = $(this);
        var files = !!this.files ? this.files : [];
        if (!files.length || !window.FileReader) return; // no file selected, or no FileReader support

        if (/^image/.test( files[0].type)){ // only image file
            var reader = new FileReader(); // instance of the FileReader
            reader.readAsDataURL(files[0]); // read the local file

            reader.onloadend = function(){ // set image data as background of div
                //alert(uploadFile.closest(".upimage").find('.imagePreview').length);
uploadFile.closest(".imgUp").find('.imagePreview').css("background-image", "url("+this.result+")");
            }
        }

    });
});

$('#id_category option').on("click", function() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
	x = $(this).text();
	$.ajax({
            type: "POST",
             url : "http://127.0.0.1:8000/blog/CategoryAPI/",
             data: {
                "category_name": x
             },
             headers: {'X-CSRFToken': csrftoken},
             success : function (data) {
                console.log("win");
                $.ajax({
                     type: "GET",
                     url : "http://127.0.0.1:8000/blog/CategoryResultAPI/",
                     headers: {'X-CSRFToken': csrftoken},
                     success : function (data) {
                        console.log(data);
                        $.each(data, function( index, value ) {
                            $('.categoryResult').append('<div style="color:#7b2020;"> >> </div>');
                            $('.categoryResult').append('<div>'+value.name+'</div>');
                        });

                     }
                });
             },
             error: function (data) {
                 console.log("loss");
             }
    });

});

$(".addTag").on("click", function(){
    myTag = $("#id_name").val()
    $('.chosenTags').append('<div class="miniTag">'+myTag+'</div>');
    $('.chosenTags').append('<div style="color:white;"> , </div>');

});