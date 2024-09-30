console.log('validaciones.js loaded');

document.addEventListener("DOMContentLoaded", function() {
    function hideErrorMessage(id) {
        var errorMessage = document.getElementById(id);
        if (errorMessage) { // Verificar que el elemento exista
            if (errorMessage.textContent.trim() !== "") { // Verificar que el mensaje no esté vacío
                setTimeout(function() {
                    errorMessage.style.opacity = 0; // Fade out the message
                    setTimeout(function() {
                        errorMessage.style.display = "none"; // Hide the message
                    }, 1000); // Fade out duration
                }, 2000); // Delay before fading out
            } else {
                errorMessage.style.display = "none"; // Hide immediately if no message
            }
        } else {
            console.warn('No se encontró el elemento con id: ' + id);
        }
    }

    // Login error messages
    hideErrorMessage("error_message");
    hideErrorMessage("error_message2");

    // Registration error messages
    hideErrorMessage("username_error");
    hideErrorMessage("email_error");
    hideErrorMessage("password1_error");
    hideErrorMessage("password2_error");
    hideErrorMessage("general_error");
});
