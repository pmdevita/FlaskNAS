$(function() {
    var sm = "576";

    function TooltipDirection() {
      if ($(window).width() <= sm) {
        return "bottom";
      } else {
        return "right";
      }
    }

    function FormCheck() {
      form = $("form").serializeArray();
      status = 1;
      for (i in form) {
        if (form[i]["value"] == "") {
          status = 0;
        }
      }
      if (form[4]["value"] != form[5]["value"]) {
          status = 0;
          if ((form[4]["value"] != "") && (form[5]["value"] != "")) {
            $("[name=password]").tooltip("show");
          }
      } else {
        $("[name=password]").tooltip("hide");
      }


      if (status == 1) {
        $("button").removeClass('disabled');
        $("button").prop("disabled", false);
      } else {
        $("button").addClass('disabled');
        $("button").prop("disabled", true);
      }

    }

    $("[name='password']").tooltip({"placement": TooltipDirection, "trigger": "manual"});
    $("[data-toggle='tooltip'][name!='password']").tooltip({"placement": TooltipDirection, "trigger": "focus hover"});

    $("input").change(FormCheck);
    FormCheck();


    $("form").submit(function( event ){
      event.preventDefault();

      $(".spinner").addClass("spinner-on")

      form = $("form").serializeArray();
      form.push({"name":"point", "value": "first_login"});


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
