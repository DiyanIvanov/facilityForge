
function togglePassword() {
    const passwordField = document.getElementById('password');
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
    } else {
        passwordField.type = 'password';
    }
}

// Spinner on form submit
document.getElementById('loginForm').addEventListener('submit', function () {
    document.getElementById('buttonText').classList.add('d-none');
    document.getElementById('spinner').classList.remove('d-none');
});
