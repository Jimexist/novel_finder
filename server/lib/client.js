// Generated by CoffeeScript 1.3.1
var socket;

socket = io.connect('http://192.168.1.191:18080');

socket.on('message', function(data) {
  if (data.welcome === 'ok') {
    return socket.emit('index');
  }
});

socket.on('index', function(data) {
  return jQuery.each(data.data, function(index, item) {
    return $('#index').append('<tr><td>' + item.key + '</td><td>' + item.value.count + '</td></tr>');
  });
});

socket.on('change', function(data) {
  return console.log(data);
});
