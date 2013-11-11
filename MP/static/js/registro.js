$(document).ready(function() {

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
         var topPersonal = parseInt($("#escolar-help").css("top").substring(0, $("#escolar-help").css("top").length - 2)) 
                             + parseInt($("#escolar").css("height").substring(0, $("#escolar").css("height").length - 2))
                             + parseInt($("#escolar").css("margin-top").substring(0, $("#escolar").css("margin-top").length - 2))
                             + parseInt($("#escolar").css("margin-bottom").substring(0, $("#escolar").css("margin-bottom").length - 2));
        
         $("#superiores-help").css("top",topPersonal);
         $("#superiores-help").css("left","5%");
        
         //Para el form de datos de otras habilidades
         var topContacto = parseInt($("#superiores-help").css("top").substring(0, $("#superiores-help").css("top").length - 2)) 
                             + parseInt($("#superiores").css("height").substring(0, $("#superiores").css("height").length - 2))
                             + parseInt($("#superiores").css("margin-top").substring(0, $("#superiores").css("margin-top").length - 2))
                             + parseInt($("#superiores").css("margin-bottom").substring(0, $("#superiores").css("margin-bottom").length - 2));
        
         /*$("#habilidades-help").css("top",topContacto);
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
    
    manageSize();
    
    $(window).resize(function(){
        manageSize();        
    });

});
