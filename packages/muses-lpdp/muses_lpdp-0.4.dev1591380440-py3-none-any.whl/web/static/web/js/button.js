const animateButton = function (e) {

    e.preventDefault;
    //reset animation
    e.target.classList.remove('animate');

    e.target.classList.add('animate');
    setTimeout(function () {
        e.target.classList.remove('animate');
    }, 700);
};
const selectors = "button, input[type=submit], input[type=reset], input[type=button], .muses-button";
const elements = document.querySelectorAll(selectors);

for (let i = 0; i < elements.length; i++) {
    elements[i].addEventListener('click', animateButton, false);

}