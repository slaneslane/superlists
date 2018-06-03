window.Superlists = {}; 
window.Superlists.initialize = function(){ 
  $('#id_text').on('focus', function(){
    $('.has-error').hide();
  });
};

window.Superlists.filter_list = function(){
  $('#id_text').on('keyup', function(){
    var value = $(this).val().toLowerCase();
    $('#id_list_table tr').filter(function(){
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
};
