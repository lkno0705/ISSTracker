// function to toggle width of menues, function needs to be adjusted for responsive use

// left menu
function toggleNavL() {   
  var x = document.getElementById("mySidebarLeft").style.left;
    if (document.getElementById("mySidebarLeft").style.left == "0px" || document.getElementById("mySidebarLeft").style.left == "")
    {
      document.getElementById("mySidebarLeft").style.left = "-250px";
      document.getElementById("mainLeft").style.marginLeft = "-250px";
      document.getElementById("arrowleft").style.transform = "rotate(180deg)";
    }
    else
    {
      document.getElementById("mySidebarLeft").style.left = "0px";
      document.getElementById("mainLeft").style.marginLeft = "0px";
      document.getElementById("arrowleft").style.transform = "rotate(0deg)";
    }
}  

//  right menu
  function toggleNav() {   
    var x = document.getElementById("mySidebar").style.right;
      if (document.getElementById("mySidebar").style.right == "-250px" || document.getElementById("mySidebar").style.right == "" )
      {
        document.getElementById("mySidebar").style.right = "0";
        document.getElementById("main").style.marginRight = "250px";
        document.getElementById("arrowright").style.transform = "rotate(180deg)";
      }
      else
      {
        document.getElementById("mySidebar").style.right = "-250px";
        document.getElementById("main").style.marginRight = "0px";
        document.getElementById("arrowright").style.transform = "rotate(0deg)";
      }
  }     

  // left menu after serch button pressed. 
  function start(){
    document.getElementById("mySidebarLeft").style.backgroundColor = "#111";
    document.getElementById("openbtnLeft").style.display = "";
    document.getElementById("sliderLeft").style.display = "";
    document.getElementById("sliderLeft").style.pointerEvents = "auto";
  }