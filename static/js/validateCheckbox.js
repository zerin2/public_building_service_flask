function validateCheckbox() {
    var checkbox = document.getElementById('formCheck-1');
    if (!checkbox.checked) {
        alert('Пожалуйста, ' +
            'отметьте согласие на обработку персональных данных для продолжения.');
        return false;
    }
    return true;
}
