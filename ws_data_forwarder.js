var express = require('express')
,http = require('http');

var app = express();
var server = http.Server(app); 
var REDIS_HOST_IP = "192.168.59.103";

const io = require('socket.io')(server);
const redis = require("redis"),
 client = redis.createClient(6379, REDIS_HOST_IP);

server.listen(3000, function(){
  console.log('listening on *:3000');
});

app.all('/:dashboard_id/:metric_pattern', function (req, res, next) {
  if(req.params.metric_pattern ==  "metricA" || req.params.metric_pattern ==  "metricB"){
	  /*subscribe to corresponding channel in redis*/
	  io.sockets.on('connection', function (socket) {
		  socket.on('set nickname', function (name) {
		    socket.name = name;
		     socket.emit('ready');
			 console.log('waiting client\'s acknowledgement...');
		  });

		  socket.on("start receiving data (from redis client)...", function () {
		  	console.log("nick nickname: " + socket.name);
		  	if(socket.name == req.params.dashboard_id) {
	    	  console.log("building subscription to " + req.params.metric_pattern);
	    	  client.subscribe(req.params.metric_pattern);
	    	  client.on("message", function(channel, message){
	    		  console.log(channel + ": " + message);
	    		  if(channel == req.params.metric_pattern) 
	    		  	socket.emit(req.params.metric_pattern, message.toString());
	    	  })
	        }
	       });
	  });
	  
	  res.header("Access-Control-Allow-Origin", "*");
	  res.header("Access-Control-Allow-Headers", "X-Requested-With");
	  res.send("Subscribe to valid metric name" + req.params.metric_pattern );
  } else {
	  next(new Error('Invalid metric pattern ' + req.params.metric_pattern));
  }
  
});