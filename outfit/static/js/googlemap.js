
var geocoder;
var map;
function initialized() {
  geocoder = new google.maps.Geocoder();
  var latlng = new google.maps.LatLng(-1.141038, 37.288865);
  var mapOptions = {
    zoom: 8,
    center: latlng,
    mapTypeId:google.maps.MapTypeId.ROADMAP
  }
  map = new google.maps.Map(document.getElementById('googleMap'), mapOptions);
}

function codeAddress() {
  var address = document.getElementById('address').value;
  geocoder.geocode( { 'address': address}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      map.setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
          map: map,
          position: results[0].geometry.location,
          animation:google.maps.Animation.BOUNCE
      });
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}

google.maps.event.addDomListener(window, 'load',initialized);