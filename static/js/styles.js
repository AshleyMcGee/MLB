    $(document).ready(function(){
        var scroll_start = 0
        var startchange = $('.jumbotron')
        var offset = startchange.offset()
         if (startchange.length){
            $(document).scroll(function() {
              scroll_start = $(this).scrollTop()
                if(scroll_start > offset.top) {
                  $("#navbar-style").css('background-color', 'rgba(9,38,105)')
                } else {
                  $('#navbar-style').css('background-color', 'rgba(0,0,0,0)')
                }
              })
            }

      })
