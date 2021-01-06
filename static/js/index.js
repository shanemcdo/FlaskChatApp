const socket = io();

socket.on('message', data => {
    let li = document.createElement('li');
    let sender = document.createElement('p');
    sender.className = 'message_sender'
    sender.innerText = data['sender'];
    let message = document.createElement('p');
    message.className = 'message_content'
    message.innerText = data['message'];
    li.className = 'message'
    li.appendChild(sender);
    li.appendChild(message);
    if(data['sender'] === socket.username)
        li.classList.add('sent_by_me');
    ul_messages.appendChild(li);
    ul_messages.scrollTop = ul_messages.scrollHeight;
})

socket.on('change_username', username =>{
    socket.username = username;
})

socket.on('join_event', username =>{
    let li = document.createElement('li');
    let p = document.createElement('p');
    p.className = 'message_announcement';
    p.innerHTML = username + ' joined the chat!';
    li.className = 'message'
    li.appendChild(p);
    ul_messages.appendChild(li);
})

socket.on('leave_event', username =>{
    let li = document.createElement('li');
    let p = document.createElement('p');
    p.className = 'message_announcement';
    p.innerHTML = username + ' left the chat!';
    li.className = 'message'
    li.appendChild(p);
    ul_messages.appendChild(li);
})

input_message.addEventListener('keydown', event =>{
    if(event.key === 'Enter')
        send_message()
});

function send_message(){
    if(input_message.value !== ''){
        socket.send({
            sender: socket.username,
            message: input_message.value,
        });
        input_message.value = '';
    }
}
