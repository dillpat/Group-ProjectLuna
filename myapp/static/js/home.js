

var submit = document.querySelector('.accept');
var checkbox = document.querySelector('.checker');


disableSubmit = function(e) {
    submit.disabled = !this.checked
};

checkbox.addEventListener('change', disableSubmit);


let cancel = document.querySelector(".cancel");
cancel.addEventListener('click',function(){
    window.location = "/logout"
})