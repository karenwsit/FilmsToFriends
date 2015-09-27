
//HOMEPAGE
$(document).ready(function() {
    $(this).load(function(){
        $.ajax("/homepage").done(function(result) {
            $('#contents').html(result);
        });
    });
});


//LOGIN
//Make login modal appear
$(document).ready(function() {
    $("#login").click(function(){
    //show login form
        $.get("/login", "login-form.html").done(function(results) {
            var contents = results;
            $("#login-form").html(contents);
            $("#login-form").css("display","block");

        });
    });
}); 


//REGISTER
//Makde register modal appear
$(document).ready(function() {
    $("#register").click(function(){
    //show registration form
        $.get("/register", "registration-form.html").done(function(results) {
            var contents = results;
            $("#login-form").html(contents);
            $("#login-form").css("display","block");
            $(".modal-login").css("height","100%");
        });
    });
});    

