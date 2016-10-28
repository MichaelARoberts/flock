var signUp = function(){
  var fd = new FormData();
  fd.append('first_name', $('#first_name').text())
  fd.append('last_name', $('#last_name').text())
  fd.append('username', $('#username').text())
  fd.append('password', $('#password').text())

  $.ajax({
    url: '/signup',
    data: fd,
    processData: false,
    contentType: false,
    type: 'POST'
  });

  window.location.href = '/'
}
