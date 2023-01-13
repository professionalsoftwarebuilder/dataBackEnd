//  Code hieronder is gebaseerd op jQuery en plaats clientside
//  validatie in lijst met id errorMessages die zicht weer bovenin
//  de pagina bevind en zichtbaar is in alle tabs, hiermee is het probleem opgelost
//  dat wanneer de gebruiker op een tab is en de pagina wil niet submitten vanwege velden op een
//  ander tab, dat de gebruiker niet weet wat er aan de hand is

    //alert('010');
    var createAllErrors = function() {
        //alert('createAllErrors');
        var form = $( this ),
            errorList = $( "ul.errorMessages", form );

        var showAllErrorMessages = function() {
            errorList.empty();
            //alert('showAllErrorMessages');

            // Find all invalid fields within the form.
            var invalidFields = form.find( ":invalid" ).each( function( index, node ) {

                // Find the field's corresponding label
                var label = $( "label[for=" + node.id + "] "),
                    // Opera incorrectly does not fill the validationMessage property.
                    message = node.validationMessage || 'Invalid value.';

                errorList
                    .show()
                    .append( "<li class='showinline ml-2' ><span><b>" + label.html() + "</b></span> " + message + "</li>" );
                    //alert('appended');
            });
            //alert('showAllErrorMessages');

        };

        $( "input[type=submit], button:not([type=button])", form )
            .on( "click", showAllErrorMessages);

        $( "input", form ).on( "keypress", function( event ) {
            //alert('Keypress');
            var type = $( this ).attr( "type" );
            if ( /date|email|month|number|search|tel|text|time|url|week/.test ( type )
              && event.keyCode == 13 ) {
                showAllErrorMessages();
            }
            //alert('Keypress');
        });
    };

    $( "form" ).each( createAllErrors );
