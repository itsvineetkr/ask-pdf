function uploadFile() {
    const fileInput = document.getElementById('fileInput')
    const uploadForm = document.getElementById('uploadForm')

    if (fileInput.files.length > 0) {
        document.querySelector('.loader').style.display = 'block'
        document.getElementById('uploadButton').disabled = true
        uploadForm.submit()
    }
}

/*

Isi page me add kar do qna wala section aur jab pdf upload ho jaye to ek dom ke andar ka text change kar ke us pdf ka name add kar do
kyunki ham name se khel rhe to name should be unique so name me time stamp add kar do
ab jab api call hogi to pdf name ham uss dom se fetch kr lenge


*/