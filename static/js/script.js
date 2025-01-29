const chat_container = document.querySelector('.chat-container')
const upload = document.querySelector('.upload')
const fileInput = document.querySelector('.file-input');
const uploadLoader = document.querySelector('.upload-loader');
const chatLoader = document.querySelector('.chat-loader');
const recordButton = document.querySelector('.record')

let mediaRecorder
let audioChunks = []
let start = false


uploadLoader.style.display = "none";
upload.style.display = "none";
chat_container.style.display = "none";

fileInput.addEventListener('change', function () {
    if (fileInput.files.length > 0) {
        upload.style.display = "block";
    } else {
        upload.style.display = "none";
    }
});


upload.addEventListener('click', async function () {
    upload.style.display = "none";
    uploadLoader.style.display = "block";

    const file = fileInput.files[0];
    const formData = new FormData();

    formData.append('file', file);

    try {
        const response = await fetch('http://127.0.0.1:8000/upload-pdf/', {
            method: 'POST',
            body: formData
        })

        const result = await response.json()
        if (result.status === 'ok') {
            chat_container.style.display = 'flex'
            document.querySelector('.error').textContent = ''
            document.querySelector('.pdf-name').innerHTML = file.name
        } else {
            chat_container.style.display = 'none'
            document.querySelector('.error').textContent = `Error: ${result.message}`
        }
    } catch (error) {
        chat_container.style.display = 'none'
        document.querySelector('.error').textContent = `Error: ${error.message}`
    }
    uploadLoader.style.display = "none";
});


const add_conversation = function (question, answer) {
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


const get_answer = async function (question) {
    const pdfName = document.querySelector('.pdf-name').innerText;
    const requestBody = JSON.stringify({
        question: question,
        pdf_name: pdfName
    });
    try {
        const response = await fetch('http://127.0.0.1:8000/generate-response/', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: requestBody
        });

        const result = await response.json();
        if (response.ok && result.status === 'ok') {
            add_conversation(question, result.response);
        } else {
            add_conversation(question, result.response || "Error processing request");
        }
    } catch (error) {
        add_conversation(question, `Error: ${error.message}`);
    }
}


document.querySelector(".send").addEventListener('click', async function () {
    const question = document.querySelector('.message-input').value;
    if (question) {
        chatLoader.style.display = "block";
        await get_answer(question);
        chatLoader.style.display = "none";
        document.querySelector('.message-input').value = '';
    }
});

document.querySelector('.message-input').addEventListener('keypress', async function (e) {
    if (e.key === 'Enter') {
        const question = document.querySelector('.message-input').value;
        if (question) {
            chatLoader.style.display = "block";
            await get_answer(question);
            chatLoader.style.display = "none";
            document.querySelector('.message-input').value = '';
        }
    }
});


recordButton.addEventListener('click', async () => {
    message_input = document.querySelector('.message-input')
    if (start == false) {
        start = true
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        mediaRecorder = new MediaRecorder(stream)
        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data)
        }

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' })
            audioChunks = []
            const reader = new FileReader()
            reader.readAsArrayBuffer(audioBlob)
            reader.onloadend = async () => {
                const audioArrayBuffer = reader.result;
                const audioBlob = new Blob([audioArrayBuffer], { type: 'audio/wav' });
                const formData = new FormData();
                formData.append('file', audioBlob, 'audio.wav');
                chatLoader.style.display = "block";
                try {
                    const response = await fetch('http://127.0.0.1:8000/transcribe-audio', {
                        method: 'POST',
                        body: formData
                    });

                    const result = await response.json();
                    if (result.status === 'ok') {
                        const question = result.transcript;
                        message_input.value = question;
                    } else {
                        document.querySelector('.error').textContent = `Error: ${result.response}`;
                    }
                } catch (error) {
                    document.querySelector('.error').textContent = `Error: ${error.message}`;
                }
                chatLoader.style.display = "none";
            }
        }
        message_input.value = 'Recording...'
        mediaRecorder.start()
    } else {
        message_input.value = ''
        mediaRecorder.stop()
        start = false
    }
})

