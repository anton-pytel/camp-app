let menutoggle = document.querySelector('.toggle');
let hammenu = document.querySelector('.hammenu');
menutoggle.onclick = function () {
    menutoggle.classList.toggle('active')
    hammenu.classList.toggle('active');
};