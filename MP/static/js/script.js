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
    
    function manageSize(){
    
        /*Se estiman a mano los height de cada help-block*/
        $("#session-help").css("height",$("#session").css("height"));
        $("#personal-help").css("height",$("#personal").css("height"));
        $("#contact-help").css("height",$("#contact").css("height"));
        
        $("#aspiraciones-help").css("height",$("#aspiraciones").css("height"));
        
        $("#escolar-help").css("height",$("#escolar").css("height"));
        $("#superiores-help").css("height",$("#superiores").css("height"));
        $("#habilidades-help").css("height",$("#habilidades").css("height"));
        
        $("#experiencias-help").css("height",$("#experiencias").css("height"));
        
        /*Se hara para cada uno de los textos de ayuda, por separado*/  
        //Para el fomr de datos ersonales
        // var topPersonal = parseInt($("#session-help").css("top").substring(0, $("#session-help").css("top").length - 2)) 
        //                     + parseInt($("#session").css("height").substring(0, $("#session").css("height").length - 2))
        //                     + parseInt($("#session").css("margin-top").substring(0, $("#session").css("margin-top").length - 2))
        //                     + parseInt($("#session").css("margin-bottom").substring(0, $("#session").css("margin-bottom").length - 2));
        
        // $("#personal-help").css("top",topPersonal);
        // $("#personal-help").css("left","5%");
        
        // //Para el form de datos de contacto
        // var topContacto = parseInt($("#personal-help").css("top").substring(0, $("#personal-help").css("top").length - 2)) 
        //                     + parseInt($("#personal").css("height").substring(0, $("#personal").css("height").length - 2))
        //                     + parseInt($("#personal").css("margin-top").substring(0, $("#personal").css("margin-top").length - 2))
        //                     + parseInt($("#personal").css("margin-bottom").substring(0, $("#personal").css("margin-bottom").length - 2));
        
        // $("#contact-help").css("top",topContacto);
        // $("#contact-help").css("right","5%");
        
        // //Para el fomr de datos de enseñanza superior
        // var topPersonal = parseInt($("#escolar-help").css("top").substring(0, $("#escolar-help").css("top").length - 2)) 
        //                     + parseInt($("#escolar").css("height").substring(0, $("#escolar").css("height").length - 2))
        //                     + parseInt($("#escolar").css("margin-top").substring(0, $("#escolar").css("margin-top").length - 2))
        //                     + parseInt($("#escolar").css("margin-bottom").substring(0, $("#escolar").css("margin-bottom").length - 2));
        
        // $("#superiores-help").css("top",topPersonal);
        // $("#superiores-help").css("left","5%");
        
        // //Para el form de datos de otras habilidades
        // var topContacto = parseInt($("#superiores-help").css("top").substring(0, $("#superiores-help").css("top").length - 2)) 
        //                     + parseInt($("#superiores").css("height").substring(0, $("#superiores").css("height").length - 2))
        //                     + parseInt($("#superiores").css("margin-top").substring(0, $("#superiores").css("margin-top").length - 2))
        //                     + parseInt($("#superiores").css("margin-bottom").substring(0, $("#superiores").css("margin-bottom").length - 2));
        
        // /*$("#habilidades-help").css("top",topContacto);
        // $("#habilidades-help").css("right","5%");*/
        
        // /* Se calcula la posicion de cada titulo */
        // if(current==0){
        //     $("h1#seccion_personal").css("top", parseInt($("#personal-help").css("top").substring(0, $("#personal-help").css("top").length - 2)) - 55);
        //     $("h1#seccion_personal").css("left","initial");
        //     $("h1#seccion_personal").css("right", parseInt($("#personal").css("width").substring(0, $("#personal").css("width").length - 2)) 
        //                                     - parseInt($("h1#seccion_personal").css("width").substring(0, $("h1#seccion_personal").css("width").length - 2))
        //                                     - 20);
                                            
        //     $("h1#seccion_contacto").css("top", parseInt($("#contact-help").css("top").substring(0, $("#contact-help").css("top").length - 2)) - 55);
        //     $("h1#seccion_contacto").css("left","60px"); 
        // }
        // if(current==2){
            
        //     $("h2#seccion_superiores").css("top", parseInt($("#superiores-help").css("top").substring(0, $("#superiores-help").css("top").length - 2)) - 55);
            
        //     $("h2#seccion_superiores").css("left","initial");
        //     $("h2#seccion_superiores").css("right", parseInt($("#superiores").css("width").substring(0, $("#superiores").css("width").length - 2)) 
        //                                     - parseInt($("h2#seccion_superiores").css("width").substring(0, $("h2#seccion_superiores").css("width").length - 2))
        //                                     - 20);
        //     /*                                
        //     $("h2#seccion_habilidades").css("top", parseInt($("#habilidades-help").css("top").substring(0, $("#habilidades-help").css("top").length - 2)) - 55);
        //     $("h2#seccion_habilidades").css("left","60px");*/ 
        // }   
    };    
    
    $("#id_estado_civil").css({
    
        width: "72%",
        'margin-left': "8%",
        'max-width': "100%"
    });
    
    //Funcionalidad del boton plus
    $(".plus-button").click(function(event){
    
        event.preventDefault();
        var containerForm = $(this).parent();
        var alreadyRemoved = false;
        containerForm.children().each(function(){           
        
            if($(this).hasClass("hidden-form") && !alreadyRemoved){
            
                $(this).fadeIn();
                $(this).removeClass("hidden-form");
                alreadyRemoved = true;
            }
        
        });
    });
    
    //Control del formulario de registro, para que funcione por paginas
    var minVal=0;
    var maxVal=4;
    var current=0;
    
    manageSize();
    
    $(window).resize(function(){
        manageSize();        
    });
    
    //Control de los mensajes de ayuda debajo del header, para que acompañen a 
    //cada pagina del formulario
    var titulos = ["su Perfil","sus Aspiraciones","sus Estudios", "su Experiencia laboral","Otras habilidades"];
    var textos = [        
        "A continuaci&oacute;n debe completar sus datos de cuenta, datos personals y de contacto <br>",
        "En esta secci&oacute;n debe ingresar las caracteristicas del trabajo que desea encontrar <br>",
        "Ahora ingrese los datos de sus estudios escolares y superiores... esta casi listo <br>",
        "Finalmente, debe ingresar los datos referentes a su experiencia laboral y ya está! <br>",
        "Ingrese otras caracteristicas que desee que aparescan en su perfil <br>"
    ];
    
    $(".form-pane:not(.active-pane)").hide();
    $("a#prev").attr("disabled","disabled");
    $(".alert > h4").html(titulos[current]);
    $(".alert > p:first").html(textos[current]);

    $("#controls > a#next").click(function(event){        
        event.preventDefault();
        //manageSize();
        $(".form-pane:nth-of-type("+(current+1)+")").removeClass("active-pane").fadeOut();
        $(".form-pane:nth-of-type("+(current+2)+")").addClass("active-pane").fadeIn();
        current++;
        $(".alert > h4").html(titulos[current]);
        $(".alert > p:first").html(textos[current]);
        if(current > 0){
            $("a#prev").removeAttr("disabled");    
            $("#controls").css("width","105px");
        }
        if(current == 4){
            
            $("a#next").fadeOut();
            $("[value=Registrar]").fadeIn();
            $("#controls").css("width","150px");          
        }                
        
    });
    //Se manejan los botones de acceso a las paginas de registro
    $("#controls > a#prev").click(function(event){
        event.preventDefault();
        //manageSize();
        $(".form-pane:nth-of-type("+(current+1)+")").removeClass("active-pane").fadeOut();
        $(".form-pane:nth-of-type("+(current)+")").addClass("active-pane").fadeIn();
        current--;
        $(".alert > h4").html(titulos[current]);
        $(".alert > p:first").html(textos[current]);
        if(current < 5){
            
            $("a#next").fadeIn();
            $("[value=Registrar]").fadeOut();    
        }
        if(current == 0){
            $("a#prev").attr("disabled","disabled");           
        }
    });
    //Se muestra la ayuda que corresponda
    $("#hide-alert").click(function(event){
        event.preventDefault();
        $(".alert").alert('close');
        $("#content").css("position","relative");
    });

    
    //Se usan los tour de ayuda en cada pagina
    $("#help").click(function(event){
        event.preventDefault();
        
        //Para cada caso, se activa el tour definido
        //Si estoy en la pagina de sesion
        if(current == 0){
            hopscotch.startTour(tour1);   
        //Si estoy en la pagina de aspiraciones     
        }else if(current == 1){
            hopscotch.startTour(tour2);
        }else if(current == 2){
            hopscotch.startTour(tour3);
        }else if(current == 3){
            hopscotch.startTour(tour4);
        }
    });
    //mensaje guia del inicio
    $("#surprise-message").animate({
        width: "100%",
        height: "100%"
    },400, function(){
        
        $(".panel").fadeIn();
    });

    //ocultar mensaje
    $(".panel-body > a").click(function(event){

        event.preventDefault();
        $(".panel").fadeOut("slow");
        setTimeout(function(){
            $("#surprise-message").animate({
                height: "0px"            
            }, 400);
        },400);
    });        
});


