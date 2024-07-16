function updateFileName(input) {
        const fileNameElement = input.parentElement.querySelector('.file-name');
        if (input.files.length > 0) {
            fileNameElement.textContent = input.files[0].name;
        } else {
            fileNameElement.textContent = '.EXCEL';
        }
    }