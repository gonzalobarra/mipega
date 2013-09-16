// Define the tour!
    var tour1 = {
      id: "hello-hopscotch",
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

    // Start the tour!
    //hopscotch.startTour(tour);
