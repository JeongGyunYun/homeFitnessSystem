$(document).ready(function (){
  var count = $("#count");
  var num;
  var goal = $("#goal").text();
  var bars = $(".bar");
  bars.each(function(i,el){
    $(this).css({
      height : 0 + "%"
    });
  });
  setInterval(function(){
    bars.each(function(){
      num = count.text()
      num = parseInt(num) + 1
      if(num <= goal){
        count.text(num)
        $(this).css({
          height : num / goal * 100 + "%"
        })
      }
    })
  }, 300);

}())