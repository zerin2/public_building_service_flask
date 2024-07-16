window.onscroll = function() {scrollFunction()};
        function scrollFunction() {
          if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            document.getElementById("js_btn_to_top").style.display = "block";
          } else {
            document.getElementById("js_btn_to_top").style.display = "none";
          }
        }
        function topFunction() {
          document.body.scrollTop = 0; // Для Safari
          document.documentElement.scrollTop = 0; // Для Chrome, Firefox, IE и Opera
        }