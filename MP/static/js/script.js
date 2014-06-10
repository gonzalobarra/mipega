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

    $("#selected-option").before("<div class='rectangle2'></div>").after("<div class='arrow-right2'></div>");
    var i = $(".profile-nav li").index($("#selected-option"));
    $(".arrow-right2").css("top",(205 + (i*37))+"");
    $(".rectangle2").css("top",(205 + (i*37))+"");
    
    $(".profile-nav li a.btn-primary").hover(function(){
        $(this).after("<div class='arrow-right'></div>");
        $(this).before("<div class='rectangle'></div>");
        
        i = $(".profile-nav li").index($(this));
        $(".arrow-right").css("top",(205 + (i*37))+"");
        $(".rectangle").css("top",(205 + (i*37))+"");
    }, function(){
    
        $(".arrow-right").remove();
        $(".rectangle").remove();
        
    });
    
    /*       DETALLE.HTML        */
    
    var sexo = $("li#sex").text();
    
    $("li#sex").remove();
    	
    if(sexo=="m"){    
        $("#user_name").after("<img class='sex_image' src='../../../static/img/man.png' />");        
    }else{    
        $("#user_name").after("<img class='sex_image' src='../../../static/img/female.png' />");        
    }    
    
    var nacionalidad = $("li#nacionalidad").text();
    
    if(nacionalidad=="chile"){
        $("li#nacionalidad").html("<img class='nac_image' src='../../../static/img/chile.png' />");
    }
    
    $("#id_usuario").css("margin-left","23%");
    
        
    
    
    
    /*      index.html      */
    /*
    var busquedaH = $(".busqueda").css("height");    
    busquedaH = parseInt(busquedaH.substring(0, busquedaH.length - 2));
    
    var jumbotronH = $(".jumbotron").css("height");
    jumbotronH = parseInt(jumbotronH.substring(0, jumbotronH.length - 2));
    
    var jumbotronM = $(".jumbotron").css("margin-bottom");
    jumbotronM = parseInt(jumbotronM.substring(0, jumbotronM.length - 2));
    
    var busquedaRapidaH = busquedaH - (jumbotronH + jumbotronM);
    
    $(".fast-search-container").css("height", busquedaRapidaH);*/
});


