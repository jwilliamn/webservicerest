'user strict';

const Hapi = require('hapi');


// Create a server with a host and port
const server = Hapi.server({
	host: 'localhost',
	port: 8000
});

// Add the route
server.route({
	method: 'GET',
	path: '/hello',
	handler: function (request, h){
		return 'hello world'
	}
});


server.route({
	method: 'GET',
	path: '/{name}',
	handler: function (request, reply){
		return 'Hello, ' + encodeURIComponent(request.params.name) + '!';
	}
});

server.route({
	method: 'POST',
	path: '/posttest',
	handler: function (request, reply){
		return 'Hello, ' + encodeURIComponent(request.params.name) + '!';
	}
});

// Start the server
async function start(){
	try{
		await server.start();
	}
	catch (err){
		console.log(err);
		process.exit(1);
	}

	console.log('Server running at:', server.info.uri);
};

start();