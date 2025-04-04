function userScroll() {
    const toTopBtn = document.querySelector('#to-top');
    const navbar = document.querySelector('.navbar');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            toTopBtn.classList.add('show');
            navbar.classList.add('border-bottom');
            navbar.classList.add('border-dark-subtle');
            navbar.classList.add('navbar-sticky');
        } else {
            toTopBtn.classList.remove('show');
            navbar.classList.remove('border-bottom');
            navbar.classList.remove('border-dark-subtle');
            navbar.classList.remove('navbar-sticky');
        }
    })
}

function scrollToTop() {
    document.body.scrollTo = 0;
    document.documentElement.scrollTop = 0;
}

document.addEventListener('DOMContentLoaded', userScroll);
document.querySelector('#to-top').addEventListener('click', scrollToTop);