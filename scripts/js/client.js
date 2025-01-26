console.log('Client side script loaded')

async function uploadFile() {
    const fileInput = document.getElementById('fileInput')
    if (fileInput.files.length > 0) {
        document.querySelector('.container-upload-loader .loader').style.display = 'block'
        document.getElementById('uploadButton').disabled = true

        document.querySelector('.error').textContent = ''
        document.querySelector('.chatbox').innerHTML = ''
        document.querySelector('.chat-section').style.display = 'none'

        const formData = new FormData()
        formData.append('file', fileInput.files[0])

        try {
            const response = await fetch('http://127.0.0.1:8000/upload-pdf/', {
                method: 'POST',
                body: formData
            })

            const result = await response.json()
            if (result.status === 'ok') {
                document.querySelector('.container-upload-loader .loader').style.display = 'none'
                document.getElementById('uploadButton').disabled = false
                document.querySelector('.chat-section').style.display = 'block'
                document.querySelector('.current-pdf').innerHTML = fileInput.files[0].name
            } else {
                document.querySelector('.error').textContent = `${result.response}`
                document.querySelector('.chat-section').style.display = 'none'
            }
        } catch (error) {
            document.querySelector('.error').textContent = `Error: ${error.message}`
            document.querySelector('.chat-section').style.display = 'none'
        }
    }
}

function add_chat(question, answer) {
    const chatbox = document.querySelector('.chatbox')
    const questionDiv = document.createElement('div')
    const qnaDivQuestion = document.createElement('div')
    const imgQuestion = document.createElement('img')
    const pQuestion = document.createElement('p')

    const qnaDivAnswer = document.createElement('div')
    const imgAnswer = document.createElement('img')
    const pAnswer = document.createElement('p')

    questionDiv.classList.add('question')
    qnaDivQuestion.classList.add('qna')
    imgQuestion.src = 'static/images/user.png'
    imgQuestion.alt = ''
    imgQuestion.style.maxWidth = '50px'
    qnaDivQuestion.appendChild(imgQuestion)
    qnaDivQuestion.appendChild(pQuestion)

    qnaDivAnswer.classList.add('qna')
    imgAnswer.src = 'static/images/ai_photo.png'
    imgAnswer.alt = ''
    imgQuestion.style.maxWidth = '50px'

    qnaDivAnswer.appendChild(imgAnswer)
    qnaDivAnswer.appendChild(pAnswer)

    pQuestion.textContent = question
    pAnswer.textContent = answer

    questionDiv.appendChild(qnaDivQuestion)
    questionDiv.appendChild(qnaDivAnswer)

    chatbox.appendChild(questionDiv)

    document.querySelector('input[name="question"]').value = ''
}

document.querySelector('#messageInput').addEventListener('click', async function () {
    const question = document.querySelector('input[name="question"]').value
    const header = {
        question: question,
        pdf_name: document.querySelector('.current-pdf').textContent
    }
    document.querySelector('.loader').style.display = 'block'
    try {
        const response = await fetch('http://127.0.0.1:8000/generate-response/', {
            method: 'POST',
            body: header
        })

        const result = await response.json()
        if (result.status === 'ok') {
            const answer = result.response
            document.querySelector('.loader').style.display = 'none'
            add_chat(question, answer)
        } else {
            document.querySelector('.error').textContent = `${result.status}`
        }
    } catch (error) {
        document.querySelector('.error').textContent = `Error: ${error.message}`
    }
})