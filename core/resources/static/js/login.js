$(function(){

  $("form").submit(function( event ){
    event.preventDefault();

    $(".spinner").addClass("spinner-on")

    form = $("form").serializeArray();
    form.push({"name":"point", "value": "login"});

    $.post("api", form, function(data, status){
      response = data;

      if (response["Response"] == "Error") {
        $("#login-error").slideDown();
        $(".spinner").removeClass("spinner-on")
        setTimeout(function(){
          $("#login-error").slideUp();
        }, 3000);
      }
      else if (response["Response"] == "Success") {
        if (response["Action"] == "Redirect") {
          window.location.replace("/");
        }
      }
    });
  });
});
