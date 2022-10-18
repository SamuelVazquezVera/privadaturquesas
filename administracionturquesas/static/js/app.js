$(document).ready(function(){
  $('.toast').toast('show');

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

