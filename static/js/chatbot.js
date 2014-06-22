$(document).ready(function() {
  $('.suggest_response_inside').hide();
  $('.suggest_alternate').hide();
  $('.suggest_response').click(function() {
    $(this).children().fadeIn('slow');
  }); 
});