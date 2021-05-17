var socket = io('http://127.0.0.1:5000');

socket.on('connect', function() {
    socket.emit('message', {data: 'I\'m connected!'});
    socket.emit('join', {client: 'weiner', room: 'client'})
});

socket.on('message', function(data){
    document.getElementById('BTC-USDT').innerHTML = data['Close'];
    document.title = data['Close']
});

socket.on('return_command', function(data){
    alert(data['response'])
})

function command() {
    com_send = document.getElementById('console-input').value;
    socket.emit('command', {command: com_send})
}