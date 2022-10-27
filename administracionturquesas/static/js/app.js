$(document).ready(function(){
  $('.toast').toast('show');
  let fecha = new Date();
  let monthNames = [ "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12" ]; 
  let fechaTexto = `${fecha.getFullYear()}-${monthNames[fecha.getMonth()]}-${fecha.getDate()}`;
  jQuery('#fecha').val(fechaTexto);
});

$(document).on('change', '#privada', function() {
  var seleccion = $(this).val();

  if (seleccion === 'privada'){
    $('#vivienda').prop("disabled", true);
  }
  else{
    $('#vivienda').prop("disabled", false);
  }
  if (seleccion === '1'){
    $('#calle').prop("disabled", false);
  }
  else{
    document.getElementById("calle").selectedIndex = 0
    $('#calle').prop("disabled", true);
  }
});

