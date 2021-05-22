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
    document.getElementById('console').innerHTML += ` ${data['response']} </br>`;
})

socket.on('client_data', function(data){
    if( data['buy']){
        document.getElementById('console').innerHTML += `bought ${data['buy']['shares']} at $${data['buy']['price']} </br>`;
    }else if (data['sell']){
        document.getElementById('console').innerHTML += `sold ${data['sell']['shares']} at $${data['sell']['price']}, balance:${data['sell']['balance']} </br>`;
    }else {
        console.error('[*] Check server, client_data is not correct')
    };
    
})

function command() {
    com_send = document.getElementById('console-input').value;
    socket.emit('command', {command: com_send})
}