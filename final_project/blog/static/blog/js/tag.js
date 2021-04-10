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