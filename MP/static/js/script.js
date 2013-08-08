/*
 * @author: Mario Muñoz Villegas    mario dot munozv at usach dot cl
 
 */

$(document).ready(function() {
    //se inicia el dropdown
    $('.dropdown-toggle').dropdown()
    
    $('.message').delay(6000).fadeOut(function() {
        $(this).remove();
    });
});


