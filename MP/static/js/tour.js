// Define the tour!
    var tour1 = {
      id: "hopscotch1",
      steps: [
        {
          title: "Datos de cuenta",
          content: "Estos datos son obligatorios y solo se usaran para acceder a su cuenta de mipega",
          target: "seccion_cuenta",
          placement: "right"
        },
        {
          title: "Datos de contacto",
          content: "Estos datos seran utilizados por los posibles empleadores para ubicarlo",
          target: "seccion_contacto",
          placement: "right"
        },
        {
          title: "Datos personales",
          content: "Estos datos seran visibles para el usuario si usted lo desea. No son obligatorios",
          target: "seccion_personal",
          placement: "right"
        },
        {
          title: "Siguiente...",
          content: "Acontinuación viene el panel 'Aspiraciones'",
          target: "next",
          placement: "right"
        }
      ]
    };
    
    var tour2 = {
      id: "hopscotch2",
      steps: [
        {
          title: "Localidad",
          content: "Dónde desea trabajar? Seleccione la opción que más se auste a sus necesidades",
          target: "id_localidad",
          placement: "right"
        },
        {
          title: "Pretención de renta",
          content: "Cuánto dinero desea ganar? Seleccion el rango que desee",
          target: "id_pretencion_renta",
          placement: "right"
        },
        {
          title: "Tipo de contrato",
          content: "Qué tipo de cntrato necesita? Seleccione la opción que desee",
          target: "id_tipo_contrato",
          placement: "right"
        },
        {
          title: "Siguiente...",
          content: "Acontinuación viene el panel 'Estudios'",
          target: "next",
          placement: "right"
        }
      ]
    };
    
    var tour3 = {
      id: "hopscotch3",
      steps: [
        {
          title: "Enseñanza escolar",
          content: "Ingrese los datos necesarios de sus estudios escolares",
          target: "seccion_escolar",
          placement: "right"
        },
        {
          title: "Estudios superiores",
          content: "Ingrese sus datos de estudios superiores",
          target: "seccion_superiores",
          placement: "right"
        },        
        {
          title: "Siguiente...",
          content: "Acontinuación viene el panel 'Experiencia laboral'",
          target: "next",
          placement: "right"
        }
      ]
    };
    
    var tour4 = {
      id: "hopscotch4",
      steps: [
        {
          title: "Experiencia laboral",
          content: "Ingrese los datos de sus trabajos anteriores",
          target: "seccion_laboral",
          placement: "right"
        },
        {
          title: "Otras habilidades",
          content: "Ingrese los datos de habilidades como cursos extras",
          target: "seccion_habilidades",
          placement: "right"
        },        
        {
          title: "Finalizar!",
          content: "Ahora quedara registrado!",
          target: "final",
          placement: "right"
        }
      ]
    };

    
