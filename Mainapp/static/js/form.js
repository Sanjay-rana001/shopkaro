const wrapper = document.querySelector('.wrapper');
const login_link = document.querySelector('.login_link');
const register_link = document.querySelector('.register_link');
const login_popup = document.querySelector('.login_popup');
const icon_close = document.querySelector('.icon-close');


register_link.addEventListener('click', ()=> {
    wrapper.classList.add('active');
});
login_link.addEventListener('click', ()=> {
    wrapper.classList.remove('active');
});


login_popup.addEventListener('click', ()=> {
    wrapper.classList.add('active-popup');
});

icon_close.addEventListener('click', ()=> {
    wrapper.classList.remove('active-popup');
});


// kizumonogatari