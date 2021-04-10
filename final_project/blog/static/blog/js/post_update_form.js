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
$(".addTag").on("click", function(){
    myTag = $("#id_name").val()
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $('.chosenTags').append('<div class="miniTag">'+myTag+'</div>');
    $('.chosenTags').append('<div style="color:white;"> , </div>');
    $.ajax({
         type: "POST",
         url : "http://127.0.0.1:8000/blog/tagAPI/",
         data: {
             "tag_name": myTag
         },
         headers: {'X-CSRFToken': csrftoken},
         success : function (data) {
            console.log("wiiiiiiiin")
         }

    });

});
$('.delete_tag').on("click", function(){
    x = $(this)
    var elmId = x.closest('div').attr('id');
    var p = x.attr('id');
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log(p);
    $('#'+elmId).remove();
    $.ajax({
         type: "POST",
         url : "http://127.0.0.1:8000/blog/delete_tagAPI/",
         data: {
             "tag_id": elmId,
             "post_id": p
         },
         headers: {'X-CSRFToken': csrftoken},
         success : function (data) {
            console.log("wiiiiiiiin")
         }

    });
});
