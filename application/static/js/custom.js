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
    $.getJSON("user/login_status", function(data){
        if(data.login_status == false){
            $('#user-area').append("<button class='btn btn-primary btn-gradient' data-toggle='modal' data-target='#LoginModal'><i class='fa fa-keyboard-o'></i><b>Login</b></button>");
            $('#btn-login').click(function () {
                $.get('user/login_form', function(data){
                    $('body').append(data);
                    alert("Login!");
                });
            });
        }
        else{
            alert("yes");
        }
    });

}