var dib_id = 'YZCV85O394D5K7H26A6M';
var dib_recent_posts = 3;

const quizCards = document.querySelectorAll('.quiz-card')

quizCards.forEach(e => e.addEventListener('click', function(){
    e.setAttribute("href","#popup1")
    let modal = document.querySelector("#interactApp604391e863fd8c00174e79a3");
    modal.removeAttribute("src")
    modal.setAttribute("src",e.getAttribute('value'))
    modal.foc
}))

