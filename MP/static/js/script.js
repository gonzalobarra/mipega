/*
 * @author: Mario Muñoz Villegas    mario dot munozv at usach dot cl
 
 */

$(document).ready(function() {
    //se inicia el dropdown
    $('.dropdown-toggle').dropdown()
    
    // $('.message').delay(6000).fadeOut(function() {
    //     $(this).remove();
    // });
    //     $('.noty_bar').parent().delay(10000).fadeOut(function() {
    //     $(this).remove();
    // });

    //configuracion e inicio Chosen
    var configChosen = {
      '.chosen-select'           : {},
      '.chosen-select-deselect'  : {allow_single_deselect:true},
      '.chosen-select-no-single' : {disable_search_threshold:10},
      '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'},
      '.chosen-select-width'     : {width:"100%"}
    }
    for (var selector in configChosen) {
      $(selector).chosen(configChosen[selector]);
    }
});


