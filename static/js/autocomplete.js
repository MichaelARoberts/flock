$('document').ready(function(){
  $.get(
    '/api/questions',
    function(data) {
      data = JSON.parse(data)
      var questions = {}

      for (let d of data){
        questions[d.question] = null
      }

      $('input.autocomplete').autocomplete({
        'data': questions
      });
    }
  )
})
