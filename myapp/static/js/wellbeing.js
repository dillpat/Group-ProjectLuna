let slidesShowing;
if(window.screen.availWidth < 500){
    slidesShowing = 1
} else {
    slidesShowing = 3
}

//Glider rotates through wellbeing articles
//calls functions from glider.min.js when arrows are clicked
new Glider(document.querySelector('.glider'),{
    slidesToShow: slidesShowing,
    draggable: true,
    dots: '#dots',
    arrows:{
        prev: '.glider-prev',
        next: '.glider-next',
    }
})

const circle = document.querySelector('.progress-ring');
//const radius = circle.r.baseVal.value;
//const circumference = radius * 2 * Math.PI;
const circumference = 364;

circle.style.strokeDasharray = `${circumference} ${circumference}`;
circle.style.strokeDashoffset = circumference;

function setProgress(percent) {
    const offset = circumference - percent / 100 * circumference;
    circle.style.strokeDashoffset = offset;
}


let taskProgress = 0;
let daily_tasks = document.querySelectorAll('.step-wrapper .task-checkbox')
let i = document.getElementById("daily_task_list").getElementsByTagName("li").length

//function when a daliy task i checked to update progression circle

function checkTask(e){
    const daily_text = document.querySelector("daily_task_text")
    if(e.checked){
        taskProgress += 100/3
        setProgress(taskProgress);
    } else {
        taskProgress -= 100/3;
        setProgress(taskProgress);
    }

    if(taskProgress <= 0 ){
          document.getElementById("daily_task_text").innerHTML = " "
    }
    //updates the circle to 1/3 when 1 task is checked
    else if(taskProgress < 34){
        circle.style.stroke = "red"
        document.getElementById("daily_task_text").innerHTML = "1/3"

    } else if(taskProgress < 67){
        circle.style.stroke = "orange"
        document.getElementById("daily_task_text").innerHTML = "2/3"

    } else {
        circle.style.stroke = "green"
        document.getElementById("daily_task_text").innerHTML = "3/3"

    }
    $(function () {
        $.ajax({
            url: "/update_daily_tasks",
            type: 'get',
            data: {taskName: e.name}
        })
    })
}


function dummyData(value){
    let data = `
    <li>
    <input type="checkbox" value="34" name="{{every_task}}"  class="task-checkbox" onclick="checkUserTask('{{every_task}}')">
    ${value}
    </li>
    `
    return data
}

$(document).ready(function(){
    $('#new_personal_task').submit(function(){
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function(res){
                val = $('#new-personal-task').val();
                $('#personal-tasks').append(dummyData(val))
            },
            error: function(e){
                alert("Problem adding a task")
            }
        })
        return false;
    })
})


function checkUserTask(e){
    $(function () {
        $.ajax({
            url: "/user_set_tasks",
            type: 'get',
            data: {taskName: e,},
             success: function(){
                 alert(e+" Successful")
             },
             error: function(){
                alert(e+" error")
             },
        })
    })
}
