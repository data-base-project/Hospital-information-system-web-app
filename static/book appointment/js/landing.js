let menu = document.querySelector(".header .menu");
menu.addEventListener("click", (e) => {
    menu.classList.toggle("open");
})
document.body.addEventListener("click", (e) => {
    if(!e.target.classList.contains("menu")){
        menu.classList.remove("open");
    }
})
