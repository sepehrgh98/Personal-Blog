function searchOpen() {
    var search = $('#txtSearch').val();
    const csrftoken = $('[name=csrfmiddlewaretoken]').val();
    var data = {
        search: search
    };
    $.ajax({
        url: 'http://127.0.0.1:8000/blog/TagAPI/',
        headers : { 'X-CSRFToken': csrftoken },
        data: data,
        method: 'POST',
//        dataType: 'jsonp',

        success : function searchResult(data)
        {
            console.log(99999999999999999999999999)
            $( "#txtSearch" ).autocomplete ({
                source: data
            });
        },
        error: function(xhr, error)
        {
        console.log(xhr.status); console.debug(error);
        }
//        jsonp: 'callback',
//        jsonpCallback: 'searchResult'
    });
}



