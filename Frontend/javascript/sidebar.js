// function to toggle width of menues, function needs to be adjusted for responsive use

// left menu
function toggleNavL() {   
  var x = document.getElementById("mySidebarLeft").style.width;
    if (document.getElementById("mySidebarLeft").style.width == "250px" || document.getElementById("mySidebarLeft").style.width == "")
    {
      document.getElementById("mySidebarLeft").style.width = "0";
      document.getElementById("mainLeft").style.marginLeft = "-250px";
      document.getElementById("arrowleft").style.transform = "rotate(180deg)";
    }
    else
    {
      document.getElementById("mySidebarLeft").style.width = "250px";
      document.getElementById("mainLeft").style.marginLeft = "0";
      document.getElementById("arrowleft").style.transform = "rotate(0deg)";
    }
}  

//  right menu
  function toggleNav() {   
    var x = document.getElementById("mySidebar").style.width;
      if (document.getElementById("mySidebar").style.width == "250px")
      {
        document.getElementById("mySidebar").style.width = "0";
        document.getElementById("main").style.marginRight = "0";
        document.getElementById("arrowright").style.transform = "rotate(0deg)";
      }
      else
      {
        document.getElementById("mySidebar").style.width = "250px";
        document.getElementById("main").style.marginRight = "250px";
        document.getElementById("arrowright").style.transform = "rotate(180deg)";
      }
  }     

  // left menu after serch button pressed. 
  function start(){
    document.getElementById("mySidebarLeft").style.backgroundColor = "#111";
    document.getElementById("openbtnLeft").style.display = "";
    document.getElementById("sliderLeft").style.display = "";
  }