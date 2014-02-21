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
    if (true) {
        $('#user-area').append("<button class='btn btn-primary btn-gradient' data-toggle='modal' data-target='#LoginModal'><i class='fa fa-keyboard-o'></i><b>Login</b></button>");
        $('body').append("<!-- Modals --><div class=\"modal fade in\" id=\"LoginModal\" tabindex=\"-1\" role=\"dialog\" aria-hidden=\"false\" style=\"display: none;\"><div class=\"modal-dialog\"><div class=\"modal-content\"><div class=\"modal-header\"><button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-hidden=\"true\">×</button><h4 class=\"modal-title\">Login</h4></div><div class=\"modal-body\"><form class=\"cmxform\" id=\"altForm\" method=\"get\"><div class=\"form-group\"><div class=\"input-group\"><span class=\"input-group-addon\"><i class=\"fa fa-user\"></i></span><input type=\"text\" class=\"form-control phone\" maxlength=\"10\" autocomplete=\"off\" placeholder=\"User Name\"></div></div><div class=\"form-group\"><div class=\"input-group\"><span class=\"input-group-addon\"><i class=\"fa fa-key\"></i></span><input type=\"text\" class=\"form-control product\" maxlength=\"10\" autocomplete=\"off\" placeholder=\"Password\"></div></div></form></div><div class=\"modal-footer\"><span class=\"panel-title-sm pull-left\" style=\"padding-top: 7px;\"><a>Forgotten Password?</a></span><button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">Close</button><button type=\"button\" class=\"btn btn-primary\" data-dismiss=\"modal\" id=\"btn-login\">Login</button></div></div></div></div>");
        $('#btn-login').click(function () {
            alert("Login!");
        });
    }
}