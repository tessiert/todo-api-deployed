jQuery(function($) {
  $('.toggle').on('change', function(evt){
    $(this).parents('form.js-toggle-form').submit()
  });
  $('.js-todo-title').on('click', function(evt){
    $(this).parents('.view').find('form.js-toggle-form').submit()
  });
});
