$(document).ready(function() {    
    
    //Se muestran los chosen singles, como inputs de bootstrap
    $("a.chosen-single").addClass("form-control");
    
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
    
    //Control de los mensajes de ayuda debajo del header, para que acompañen a 
    //cada pagina del formulario
    var titulos = ["su Perfil","sus Aspiraciones","sus Estudios", "su Experiencia laboral","Otras habilidades"];
    var textos = [        
        "A continuación debe completar con sus datos de cuenta, personales y de contacto en el formulario expuesto a continuación. Los campos marcados con un * son obligatorios. <br>",
        "En la presente página debe seleccionar los diferentes cargos en los que desea encontrar trabajo, además, de donde le gustaría desempeñarlos, sus pretenciones de renta"
        + "y el tipo de contrato buscado<br>",
        "Dentro del formulario expuesto a continuación debe indicar si lo desea, el estado de su enseñanza escolar media, en el caso de que haya estudiado en un colegio técnico"
        + "se le da la opción de ingresar la institución donde lo hizo y el título que obtuvo una vez finalizada estado <br>",
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
        manageSize();
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
        manageSize();
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

    function manageSize(){
    
        /*Se estiman a mano los height de cada help-block*/
        $("#session-help").css("height",$("#session").css("height"));
        $("#personal-help").css("height",$("#personal").css("height"));
        $("#contact-help").css("height",$("#contact").css("height"));
        
        $("#aspiraciones-help").css("height",$("#aspiraciones").css("height"));
        
        //alert($("#aspiraciones-help").css("height"));
        
        $("#escolar-help").css("height",$("#escolar").css("height"));
        $("#superiores-help").css("height",$("#superiores").css("height"));
        $("#habilidades-help").css("height",$("#habilidades").css("height"));
        
        $("#experiencias-help").css("height",$("#experiencias").css("height"));
        
        /*Se hara para cada uno de los textos de ayuda, por separado*/  
        //Para el fomr de datos ersonales
         var topPersonal = parseInt($("#session-help").css("top").substring(0, $("#session-help").css("top").length - 2)) 
                             + parseInt($("#session").css("height").substring(0, $("#session").css("height").length - 2))
                             + parseInt($("#session").css("margin-top").substring(0, $("#session").css("margin-top").length - 2))
                             + parseInt($("#session").css("margin-bottom").substring(0, $("#session").css("margin-bottom").length - 2));
        
         $("#personal-help").css("top",topPersonal);
         $("#personal-help").css("left","5%");
        
        //Para el form de datos de contacto
         var topContacto = parseInt($("#personal-help").css("top").substring(0, $("#personal-help").css("top").length - 2)) 
                             + parseInt($("#personal").css("height").substring(0, $("#personal").css("height").length - 2))
                             + parseInt($("#personal").css("margin-top").substring(0, $("#personal").css("margin-top").length - 2))
                             + parseInt($("#personal").css("margin-bottom").substring(0, $("#personal").css("margin-bottom").length - 2));
        
         $("#contact-help").css("top",topContacto);
         $("#contact-help").css("right","5%");
        
         //Para el fomr de datos de enseñanza superior
         var topEscolar = parseInt($("#escolar-help").css("top").substring(0, $("#escolar-help").css("top").length - 2)) 
                             + parseInt($("#escolar").css("height").substring(0, $("#escolar").css("height").length - 2))
                             + parseInt($("#escolar").css("margin-top").substring(0, $("#escolar").css("margin-top").length - 2))
                             + parseInt($("#escolar").css("margin-bottom").substring(0, $("#escolar").css("margin-bottom").length - 2));
        
         $("#superiores-help").css("top",topEscolar);
         $("#superiores-help").css("left","5%");
        
         //Para el form de datos de otras habilidades
         var topSuperiores = parseInt($("#superiores-help").css("top").substring(0, $("#superiores-help").css("top").length - 2)) 
                             + parseInt($("#superiores").css("height").substring(0, $("#superiores").css("height").length - 2))
                             + parseInt($("#superiores").css("margin-top").substring(0, $("#superiores").css("margin-top").length - 2))
                             + parseInt($("#superiores").css("margin-bottom").substring(0, $("#superiores").css("margin-bottom").length - 2));
        
         /*$("#habilidades-help").css("top",topSuperiores);
         $("#habilidades-help").css("right","5%");*/
        
         /* Se calcula la posicion de cada titulo */
         if(current==0){
             $("h1#seccion_personal").css("top", parseInt($("#personal-help").css("top").substring(0, $("#personal-help").css("top").length - 2)) - 55);
             $("h1#seccion_personal").css("left","initial");
             $("h1#seccion_personal").css("right", parseInt($("#personal").css("width").substring(0, $("#personal").css("width").length - 2)) 
                                             - parseInt($("h1#seccion_personal").css("width").substring(0, $("h1#seccion_personal").css("width").length - 2))
                                             - 20);
                                            
             $("h1#seccion_contacto").css("top", parseInt($("#contact-help").css("top").substring(0, $("#contact-help").css("top").length - 2)) - 55);
             $("h1#seccion_contacto").css("left","60px"); 
         }
         if(current==2){
            
             $("h2#seccion_superiores").css("top", parseInt($("#superiores-help").css("top").substring(0, $("#superiores-help").css("top").length - 2)) - 55);
            
             $("h2#seccion_superiores").css("left","initial");
             $("h2#seccion_superiores").css("right", parseInt($("#superiores").css("width").substring(0, $("#superiores").css("width").length - 2)) 
                                             - parseInt($("h2#seccion_superiores").css("width").substring(0, $("h2#seccion_superiores").css("width").length - 2))
                                             - 20);
             /*                                
             $("h2#seccion_habilidades").css("top", parseInt($("#habilidades-help").css("top").substring(0, $("#habilidades-help").css("top").length - 2)) - 55);
             $("h2#seccion_habilidades").css("left","60px");*/ 
         }   
    };
    
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
    $.scrollTo(".header",300);
    $("#surprise-message").parent().css("overflow","hidden");
    
    //ocultar mensaje
    $(".panel-body > a").click(function(event){

        event.preventDefault();
        $(".panel").fadeOut("slow");
        setTimeout(function(){
            $("#surprise-message").animate({
                height: "0px"            
            }, 400);
            $("#surprise-message").parent().css("overflow","visible");
        },400);
    });
    
    manageSize();
    
    $(window).resize(function(){
        manageSize();        
    });

});
