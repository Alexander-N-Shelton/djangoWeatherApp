function userScroll() {
    const toTopBtn = document.querySelector('#to-top');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            toTopBtn.classList.add('show');
        } else {
            toTopBtn.classList.remove('show');
        }
    })
}

function scrollToTop() {
    document.body.scrollTo = 0;
    document.documentElement.scrollTop = 0;
}

document.addEventListener('DOMContentLoaded', userScroll);
document.querySelector('#to-top').addEventListener('click', scrollToTop);