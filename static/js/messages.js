function showAlert(message, tags) {
    const alertClass = tags.includes('success') ? 'alert-success' : 'alert-error';
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert ' + alertClass;
    alertDiv.textContent = message;
    document.body.appendChild(alertDiv);
    setTimeout(function() {
        alertDiv.parentNode.removeChild(alertDiv);
    }, 5000); // Удаляем сообщение через 5 секунд
}

