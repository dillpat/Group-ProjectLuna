//JS functions for the login page

var set_x = document.getElementById("stu")
var set_y = document.getElementById("sta")
var set_login = document.getElementById("btn")

let stuText = document.querySelector('#stu-text');
let staText = document.querySelector('#sta-text');


//Function change to the staff login page when staff button is clicked

function sta(){
    set_x.style.left = "-400px";
    set_y.style.left = "0px";
    set_login.style.left = "110px";
    staText.style.color = "#fff";
    stuText.style.color = "#000"

  }


//Function change to the student login page when student button in clicked
  function stu(){
    set_x.style.left = "0px";
    set_y.style.left = "400";
    set_login.style.left = "0px";
    staText.style.color = "#000";
    stuText.style.color = "#fff"
  }

  //Animation when the login page is opened
  var tl = gsap.timeline()
  tl.set('#luna-logo', {y:300,scale:5})
  tl.set('.form-win',{opacity:0})
  tl.to('#luna-logo',{duration:1,rotation:360})
  tl.to("#luna-logo",{duration:1,y:1})
  tl.to('#luna-logo',{duration:0.5,scale:1})
  tl.to('#luna-logo', {repeat:-1, yoyo:true,y:5})
  tl.to('.form-win',{duration:0.75,opacity:1})

  

  //Animation for comets in the background
  
  var cometTimeline = gsap.timeline({repeat: -1, repeatDelay:5 ,defaults: {ease: Power4.easeIn}})

cometTimeline.fromTo('#comet1', 4, {rotation: 30, scaleY: 0, opacity:0}, {rotation: 30, scaleY: 1, x: -1300, y: 1500, opacity:1})
cometTimeline.fromTo('#comet2', 2.5, { rotation: 30, scaleY: 0, opacity:0}, {rotation: 30, scaleY: 1, x: -500, y: 1500, opacity:1})
cometTimeline.fromTo('#comet3', 3, { rotation: 30, scaleY: 0, opacity:0}, {rotation: 30, scaleY: 1, x: -500, y: 1500, opacity:1})
cometTimeline.fromTo('#comet4', 3, { rotation: 30, scaleY: 0, opacity:0}, {rotation: 30, scaleY: 1, x: -500, y: 1500, opacity:1})
cometTimeline.fromTo('#comet5', 4, { rotation: 30, scaleY: 0, opacity:0}, {rotation: 30, scaleY: 1, x: -500, y: 1500, opacity:1})
cometTimeline.fromTo('#comet6', 3, { rotation: 30, scaleY: 0, opacity:0}, {rotation: 30, scaleY: 1, x: -500, y: 1500, opacity:1})
  /*
  var tl2 = gsap.timeline({delay:5,repeat: -1})
  tl2.to('#comet1',{duration:8, x:500, y:1500, delay:3})
  tl2.to('#comet2')
  */
