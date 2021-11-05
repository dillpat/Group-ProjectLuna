// JS for the sidebar which appears on most pages

$('.side-nav').click(function(){
    
})

//function to open the sidebar menu when clicked
function openNav() {
    document.querySelector(".side-nav").style.width = "60vw";
    $(".side-nav-shader").fadeIn("slow")
}
//function to close the sidebar menu when clicked
function closeNav() {
    document.querySelector(".side-nav").style.width = "0";
    $(".side-nav-shader").fadeOut("slow")
}

//function to toggle the length of the wellbeing tasks when the arrow is clicked
$('.step-goals .expand').click(function(){
    $(this).parent().find('.more-user-goals').toggle();
});

$('.step-goals .expand').click(function(){
    $(this).parent().find('.more-step-goals').toggle();
});