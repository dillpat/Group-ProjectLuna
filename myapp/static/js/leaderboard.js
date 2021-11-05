// assigning html elements to JS variables
var alltime_btn = document.getElementById("a")
var week_btn = document.getElementById("w")
var y = document.getElementById("weekly")
var z = document.getElementById("alltime")
var b = document.getElementById("btn")
var t = document.getElementById("table")

//function to change the leaderborder view to weekly
function weekly(){
  y.style.visibility = "visible";
  z.style.visibility = "hidden";
  b.style.left = "120px";
  t.innerHTML = "Weekly";
  alltime_btn.style.color = "black";
  week_btn.style.color = "white"
    }

//function to change the leaderborder view to weekly
function alltime(){
  y.style.visibility = "hidden";
  z.style.visibility = "visible";
  b.style.left = "0px";
  t.innerHTML = "All-time";
  alltime_btn.style.color = "white";
  week_btn.style.color = "black"
    }