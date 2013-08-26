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

    //Control del formulario de registro, para que funcione por paginas
    var minVal=0;
    var maxVal=4;
    var current=0;

    //Control de los mensajes de ayuda debajo del header, para que acompañen a 
    //cada pagina del formulario
    var titulos = ["su Perfil","sus Aspiraciones","sus Estudios", "su Experiencia laboral"];
    var textos = [        
        "A continuaci&oacute;n debe completar sus datos de cuenta, datos personals y de contacto <br>",
        "En esta secci&oacute;n debe ingresar las caracteristicas del trabajo que desea encontrar <br>",
        "Ahora ingrese los datos de sus estudios escolares y superiores... esta casi listo <br>",
        "Finalmente, debe ingresar los datos referentes a su experiencia laboral y ya está! <br>"
    ];
    /*
    var offset = $(".alert").offset().top;
    var winOffset = $('html').offset().top;    
    //OJO! SE USA EN TODOS LOS DOCUMENTOS ASI QUE CUIDADO!
    $(window).scroll(function(){
        alert($(window).position());
        //si la posicion vertical de la laerta y la ventana son las mismas
        if($(window).offset().top - $(".alert").offset().top < 0){
            
            $(".alert").css("position","fixed");
            $(".alert").css("top","0px");   
                 
        }else if (($(window).offset().top - offset) < 0){
            $(".alert").css("position","relative");
        }
    });
*/
    $(".form-pane:not(.active-pane)").hide();
    $("a#prev").attr("disabled","disabled");
    $(".alert > h4").html(titulos[current]);
    $(".alert > p:first").html(textos[current]);

    $("#controls > a#next").click(function(event){        
        event.preventDefault();
        $(".form-pane:nth-of-type("+(current+1)+")").removeClass("active-pane").fadeOut();
        $(".form-pane:nth-of-type("+(current+2)+")").addClass("active-pane").fadeIn();
        current++;
        $(".alert > h4").html(titulos[current]);
        $(".alert > p:first").html(textos[current]);
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
        $(".alert > h4").html(titulos[current]);
        $(".alert > p:first").html(textos[current]);
        if(current < 4){
            //$("a#next").removeAttr("disabled");
            $("a#next").fadeIn();
            $("[value=Registrar]").fadeOut();    
        }
        if(current == 0){
            $("a#prev").attr("disabled","disabled");           
        }
    });
    
    $("#hide-alert").click(function(event){
        event.preventDefault();
        $(".alert").alert('close');
        $("#content").css("position","relative");
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


