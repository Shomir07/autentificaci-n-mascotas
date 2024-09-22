document.querySelector('.profile-pic').addEventListener('click', function() {
    var navbar = document.querySelector('.l-navbar_movil');
    if (navbar.classList.contains('show')) {
        navbar.classList.remove('show');
    } else {
        navbar.classList.add('show');
    }
});
