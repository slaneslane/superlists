window.Superlists = {}; 
window.Superlists.initialize = function () { 
  $('input[name="text"]').on('focus', function () {
    $('.has-error').hide();
  });
};
