function toggleNavL() {   
    var x = document.getElementById("mySidebarLeft").style.width;
      if (document.getElementById("mySidebarLeft").style.width == "250px" )
      {
        document.getElementById("mySidebarLeft").style.width = "0";
        document.getElementById("mainLeft").style.marginLeft = "0";
        document.getElementById("arrowleft").style.transform = "rotate(180deg)";
      }
      else
      {
        document.getElementById("mySidebarLeft").style.width = "250px";
        document.getElementById("mainLeft").style.marginLeft = "250px";
        document.getElementById("arrowleft").style.transform = "rotate(0deg)";
      }
  }     