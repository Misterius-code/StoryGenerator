<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
<script>
var bar = document.getElementById("bar");
setInterval(function(){
    $.ajax({
      url: "/rand",
      type: "get",
      success: function(response) {
        bar.value = response;
       },
      error: function(xhr) {
          //Handel error
      }
    }); 
}, 1000);
</script>