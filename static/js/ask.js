$('document').ready(function(e){
  var getLocation = function(cb){
    navigator.geolocation.getCurrentPosition(function(position) {
      console.log(position)
      var lat = position.coords.latitude
      var lng = position.coords.longitude

      var url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + lat + "," + lng + "&key=AIzaSyCM8bk-wN3XZAZSBbQHZ6vgeueCZaGDmZE"
      console.log(url)
      $.get(
        url,
        function(data) {
          $('.location-display').text(data.results[0].formatted_address)
        }
      )

    });
  }
  getLocation()
});

var answer = function(data){
  data = JSON.parse(data)
  post = data['links'][0].replace('<h2>','').replace('</h2>','')


  var answer =
  `
  <div class="row answer ">
    <div class="right col s8">
      <div class="green white-text card horizontal chat-bubble-right">
        <div class="card-stacked">
          <div class="card-content">
            <p>`+ post +`</p>
          </div>
          <div class="card-action">
            <small><a href="#" class="yellow-text">Get Live Help</a></small>
          </div>
        </div>
      </div>
      <small class="grey-text lighten-2 timestamp">`+ new Date().toLocaleString(); +`</small>
    </div>
  </div>
  `
  $('.loader-swirl').remove()
  $('#chatContainer').append(answer)
}
var askQuestion = function(){
  var query = $('#query').val()
  $('#query').val("")
  var ask =
  `<div class="row question">
    <div class="col s8">
      <div class="card horizontal chat-bubble-left">
        <div class="card-stacked">
          <div class="card-content">
            <p>`+ query +`</p>
          </div>
        </div>
      </div>
      <small class="grey-text lighten-2">`+ new Date().toLocaleString(); +`</small>
    </div>
  </div>
  `
  var loader =
  `
  <div class="center-align loader-swirl">
    <div class="preloader-wrapper small active">
      <div class="spinner-layer spinner-green-only">
        <div class="circle-clipper left">
          <div class="circle"></div>
        </div><div class="gap-patch">
          <div class="circle"></div>
        </div><div class="circle-clipper right">
          <div class="circle"></div>
        </div>
      </div>
    </div>
  </div>
  `

  $('#chatContainer').append(ask).append(loader)

  var fd = new FormData();
  fd.append('query', query)
  fd.append('location', $('.location-display').text())

  $.ajax({
    url: '/api/ask',
    data: fd,
    processData: false,
    contentType: false,
    type: 'POST',
    success: function(data){
      answer(data)
    }
  });
}
