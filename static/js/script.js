const add_conversation = function(question, answer){
    const chatBox = document.querySelector('.chat-box');

    const userMessage = document.createElement('div');
    userMessage.classList.add('message', 'user');
    const userContent = document.createElement('div');
    userContent.classList.add('content');
    userContent.textContent = question;
    userMessage.appendChild(userContent);

    const aiMessage = document.createElement('div');
    aiMessage.classList.add('message', 'ai');
    const aiContent = document.createElement('div');
    aiContent.classList.add('content');
    aiContent.textContent = answer;
    aiMessage.appendChild(aiContent);

    chatBox.appendChild(userMessage);
    chatBox.appendChild(aiMessage);
};



