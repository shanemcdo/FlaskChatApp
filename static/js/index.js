const socket = io();

socket.on('message', data => {
    let li = document.createElement('li');
    let sender = document.createElement('p');
    sender.className = 'message_sender'
    sender.innerText = data['sender'];
    let message = document.createElement('p');
    sender.className = 'message_content'
    message.innerText = data['message'];
    li.appendChild(sender);
    li.appendChild(message);
    ul_messages.appendChild(li);
})

input_message.addEventListener('keydown', event =>{
    if(event.key === 'Enter')
        send_message()
});

function send_message(){
    if(input_message.value !== ''){
        socket.emit('message', {
            sender: 'noone',
            message: input_message.value,
        });
        input_message.value = '';
    }
}
