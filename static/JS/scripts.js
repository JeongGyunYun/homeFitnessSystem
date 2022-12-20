$(function (){
  var count = $("#count");
  var goal = $("#goal").text();
  var bars = $(".bar");
  var cnum, gnum = parseInt(goal);

  var clear = setInterval(function(){
    fetch("{{ url_for('data_feed') }}")
            .then(response => {
                response.text().then(data => {
                  count.innerText = data
                });
            })
    cnum = parseInt(count.text())
    bars.each(function(){
      if(cnum <= gnum){
        // count.text(num)
        $(this).css({
          height : cnum / gnum * 100 + "%"
        })
      }
      else{
        clearInterval(clear);
        $("#clear").css('visibility', 'visible');
        $('.sample_video').trigger('pause');
      }
    })
  }, 500);

  $("#clear").click(function(){
    //Some code
    $(location).attr("href", "/home");
  });
});
