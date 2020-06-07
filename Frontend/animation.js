/* Set the width of the side navigation to 250px */
function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
}

/* Set the width of the side navigation to 0 */
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  
}

function closeNav1() {
    document.getElementById("menuleft").style.width = "0";
    document.getElementById("menuleft").style.opacity = "0";
  }

  function openNav1() {
    document.getElementById("menuleft").style.width = "20%";
    document.getElementById("menuleft").style.opacity = "1";
  }