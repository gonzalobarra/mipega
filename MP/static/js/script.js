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

    var minVal=0;
    var maxVal=4;
    var current=0;

    $(".form-pane:not(.active-pane)").hide();
    $("a#prev").attr("disabled","disabled");

    $("#controls > a#next").click(function(event){        
        event.preventDefault();
        $(".form-pane:nth-of-type("+(current+1)+")").removeClass("active-pane").fadeOut();
        $(".form-pane:nth-of-type("+(current+2)+")").addClass("active-pane").fadeIn();
        current++;
        if(current > 0){
            $("a#prev").removeAttr("disabled");    
        }
        if(current == 3){
            //$("a#next").attr("disabled","disabled"); 
            $("a#next").fadeOut();
            $("[value=Registrar]").fadeIn();          
        }                
        
    });
    $("#controls > a#prev").click(function(event){
        event.preventDefault();
        $(".form-pane:nth-of-type("+(current+1)+")").removeClass("active-pane").fadeOut();
        $(".form-pane:nth-of-type("+(current)+")").addClass("active-pane").fadeIn();
        current--;
        if(current < 4){
            //$("a#next").removeAttr("disabled");
            $("a#next").fadeIn();
            $("[value=Registrar]").fadeOut();    
        }
        if(current == 0){
            $("a#prev").attr("disabled","disabled");           
        }
    });
});


