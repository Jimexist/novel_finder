// Generated by CoffeeScript 1.3.1
var app, book_feed, db, io, server;

app = require('express')();

server = require('http').createServer(app);

io = require('socket.io').listen(server);

db = require('nano')('http://192.168.1.188:5984/novel');

server.listen(18080);

book_feed = db.follow({
  since: 'now'
});

book_feed.on('change', function(change) {
  console.log(change);
  return db.view('index', 'books', {
    group: true,
    keys: [change.id]
  }, function(err, body) {
    return io.sockets.emit('change', body);
  });
});

book_feed.follow();

app.get('/', function(req, res) {
  return res.sendfile(__dirname + '/index.html');
});

app.get('/client.js', function(req, res) {
  return res.sendfile(__dirname + '/client.js');
});

io.sockets.on('connection', function(socket) {
  socket.emit('message', {
    welcome: "ok"
  });
  socket.on('index', function(data) {
    return db.view('index', 'books', {
      group: true
    }, function(err, body) {
      return socket.emit('index', {
        'type': 'books',
        'data': body.rows
      });
    });
  });
  return socket.on('book', function(data) {
    return db.view('index', 'chapters', {
      group: true,
      keys: [data.id]
    }, function(err, body) {
      return socket.emit('book', {
        'type': 'chapters',
        'data': body.rows
      });
    });
  });
});
