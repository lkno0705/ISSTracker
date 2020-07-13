// function to toggle width of menues, function needs to be adjusted for responsive use
var clickedBoth = false;
var clickedL = false;
var clickedR = false;
var bContextMenu = false;

// left menu
function toggleNavL(show) {
  var x = document.getElementById("mySidebarLeft").style.left;
  if (!show){
    if (document.getElementById("mySidebarLeft").style.left == "0px" || document.getElementById("mySidebarLeft").style.left == "")
    {
      document.getElementById("mySidebarLeft").style.left = "-250px";
      document.getElementById("mainLeft").style.marginLeft = "-250px";
      document.getElementById("arrowleft").style.transform = "rotate(180deg)";
      clickedL = false;
    }
    else
    {
      document.getElementById("mySidebarLeft").style.left = "0px";
      document.getElementById("mainLeft").style.marginLeft = "0px";
      document.getElementById("arrowleft").style.transform = "rotate(0deg)";
      clickedL = true; 
    }
  }
  else
  {
    document.getElementById("mySidebarLeft").style.left = "0px";
    document.getElementById("mainLeft").style.marginLeft = "0px";
    document.getElementById("arrowleft").style.transform = "rotate(0deg)";
    clickedL = true; 
  }
}  

//  right menu
  function toggleNav() {
    var x = document.getElementById("mySidebar").style.right;
    var controls = document.getElementsByClassName("leaflet-control-zoom");
      if (document.getElementById("mySidebar").style.right == "-800px" || document.getElementById("mySidebar").style.right == "" )
      {
        document.getElementById("mySidebar").style.right = "0";
        document.getElementById("main").style.marginRight = "800px";
        document.getElementById("arrowright").style.transform = "rotate(180deg)";

         controls[0].style.right = "800px";
         clickedR = true;
      }
      else
      {
        document.getElementById("mySidebar").style.right = "-800px";
        document.getElementById("main").style.marginRight = "0px";
        document.getElementById("arrowright").style.transform = "rotate(0deg)";

          controls[0].style.right = "0";
          clickedR = false;
      }
  }     

  function toggleClose(event) {
    if (!bContextMenu)
    {
    // removePopUps();
    var mouseClickWidth = event.clientX;
    var controls = document.getElementsByClassName("leaflet-control-zoom");

    if (clickedL && clickedR) clickedBoth = true;

    // close left & right
    if (clickedBoth && mouseClickWidth<=800 && mouseClickWidth>=250) {
      document.getElementById("mySidebar").style.right = "-800px";
      document.getElementById("main").style.marginRight = "0px";
      document.getElementById("arrowright").style.transform = "rotate(0deg)";
      controls[0].style.right = "0";

      document.getElementById("mySidebarLeft").style.left = "-250px";
      document.getElementById("mainLeft").style.marginLeft = "-250px";
      document.getElementById("arrowleft").style.transform = "rotate(180deg)";

      clickedL = false;
      clickedR = false;
      clickedBoth = false;

      // close only right -> implemented because of side-effects from start() function
    } else if (clickedR && !clickedL && mouseClickWidth<=755 && window.getComputedStyle(document.getElementById("mySidebarLeft")).getPropertyValue('left') === "-250px") {
      document.getElementById("mySidebar").style.right = "-800px";
      document.getElementById("main").style.marginRight = "0px";
      document.getElementById("arrowright").style.transform = "rotate(0deg)";
      controls[0].style.right = "0";
      
      clickedR = false;
    } else if (clickedL && !clickedR && mouseClickWidth>=295 && window.getComputedStyle(document.getElementById("mySidebar")).getPropertyValue('right') === "-800px") {
      document.getElementById("mySidebarLeft").style.left = "-250px";
      document.getElementById("mainLeft").style.marginLeft = "-250px";
      document.getElementById("arrowleft").style.transform = "rotate(180deg)";

      clickedL = false;
    }
  }
  else
   bContextMenu=false;
  }

  function switchToLightmode() {
    //document.body.setAttribute('data-theme', 'light');
    if (document.body.getAttribute("data-theme") === "dark")
      document.body.setAttribute('data-theme', 'light');
    else
      document.body.setAttribute('data-theme', 'dark');

  }

  // left menu after serch button pressed.
  function start(bool){
    if (!bool)
     callGeoCoding();
    document.body.setAttribute('data-theme', 'dark');
    document.getElementById("openbtnLeft").style.display = "";
    document.getElementById("sliderLeft").style.display = "";
    document.getElementById("sliderRadius").style.display = "";
    document.getElementById("flyby").style.display = "";
    document.getElementById("pastpasses").style.display = "";
    document.getElementById("mySidebarLeft").style.pointerEvents = "auto";
    document.getElementById("mainLeft").style.pointerEvents = "auto";
    bStart = true;
    var checkboxes = document.getElementsByClassName("checkbox-hidden");   
    for (var i = 0; i < checkboxes.length; i++)
    {
      checkboxes[i].style.display = "block";
    }
    clickedL = true;
  }
   document.addEventListener("click", toggleClose)
