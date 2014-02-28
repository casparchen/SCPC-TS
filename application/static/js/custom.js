//  Author: Louis Holladay
//  Website: AdminDesigns.com
//  Last Updated: 01/01/14 
// 
//  This file is reserved for changes made by the user 
//  as it's often a good idea to seperate your work from 
//  the theme. It makes modifications, and future theme
//  updates much easier 
// 

//  Place custom styles below this line 
///////////////////////////////////////
var current_height = $(window).height();
var current_main_height = $('#main').height();
if (current_height - 53 > current_main_height) {
    //$('#main').css("min-height", current_height - 53);
    $('#content').css("height", current_height - 106);
    $('#content').css("min-height", current_height - 106);
}

var SCPC = function () {
    $.getJSON("/user/login_status", function(data){
        if(data.login_status == false){
            $('#user-area').append("<button class='btn btn-primary btn-gradient' id='btn-login-form'><i class='fa fa-keyboard-o'></i><b>Login</b></button>");
            $('#btn-login-form').click(function () {
                $.get('/user/login_form', function(data){
                    if(!$('#LoginModal').length)
                        $('body').append(data);
                    $('#LoginModal').modal();
                    $('#btn-login').click(function(){
                        $.ajax({
                            cache: true,
                            type: "POST",
                            url:"/user/login",
                            data:$('#loginForm').serialize(),
                            async: true,
                            error: function(request) {
                                alert("Connection error");
                            },
                            success: function(data) {
                                data = $.parseJSON(data);
                                
                                if(data.result == 'ok'){
                                    alert("Dear " + data.username + ", welcome back!");
                                    window.location.href=document.referrer;
                                }else{
                                    alert("Username or Password does not match!");
                                    window.location.href=document.referrer;  
                                }
                            }
                        });

                    });

                });
            });
        }
        else{
            var email_hash = data.email_hash;
            $('#user-area').append("<div class=\"btn-group user-menu\" id=\"menu_user\"><button type=\"button\" class=\"btn btn-default btn-gradient btn-sm dropdown-toggle\" data-toggle=\"dropdown\"> <span class=\"glyphicons glyphicons-user\"></span> <b id='menu-user-username'></b> </button><button type=\"button\" class=\"btn btn-default btn-gradient btn-sm dropdown-toggle padding-none\" data-toggle=\"dropdown\"> <img src=\"http://gravatar.duoshuo.com/avatar/" + email_hash +"\" alt=\"user avatar\" width=\"28\" height=\"28\"> </button><ul class=\"dropdown-menu checkbox-persist animated-short animated flipInY\" role=\"menu\"><li class=\"menu-arrow\"><div class=\"menu-arrow-up\"></div></li><li class=\"dropdown-header\">Your Account <span class=\"pull-right glyphicons glyphicons-user\"></span></li><li><ul class=\"dropdown-items\"><li><div class=\"item-icon\"><i class=\"fa fa-envelope-o\"></i> </div><a class=\"item-message\" href=\"setting\">Setting</a> </li><li><div class=\"item-icon\"><i class=\"fa fa-envelope-o\"></i> </div><a class=\"item-message\" id='btn-logout' href=\"\">Logout</a> </li></li></ul></li></ul></div>");
            $('#menu-user-username').text(data.username);
            $('#btn-logout').click(function(){
                $.getJSON("/user/logout", function(data){
                    if(data.result == "ok"){
                        alert("You are now logged out.");
                        window.location.href = '/';
                    }
                });
                return false;
            });
        }
    });
}



