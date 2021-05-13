var socket = io('http://127.0.0.1:5000');

socket.on('connect', function() {
    socket.emit('message', {data: 'I\'m connected!'});
    socket.emit('join', {client: 'weiner', room: 'client'})
});

socket.on('message', function(data){
    document.getElementById('BTC-USDT').innerHTML = data['Close'];
});