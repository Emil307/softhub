const burger = document.getElementById('burger')
const nav = document.getElementById('nav')

function handleClick() {
    burger.classList.toggle('burger--active');
    nav.classList.toggle('nav--visible');
}

burger.onclick = handleClick;