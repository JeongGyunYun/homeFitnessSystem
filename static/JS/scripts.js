$(function (){
  console.log("##########");

  var count = $("#count");
  var num;
  var goal = $("#goal").text();
  var bars = $(".bar");

  console.log(count);
  console.log(goal);
  
  bars.each(function(i,el){
    $(this).css({
      height : 0 + "%"
    });
  });
  
  var clear = setInterval(function(){
    bars.each(function(){
      num = count.text()
      if(num <= goal){
        // count.text(num)
        $(this).css({
          height : num / goal * 100 + "%"
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
