
function callBackEnd(){
  $.ajax({
    url: 'http://127.0.0.1:8082',
    data:"AstrosOnISS",
    type: 'GET',
    crossDomain: true,
    dataType: 'json',
    success: function() { console.log("Success"); },
    error: function() {  console.log('Failed!'); }
})
}

callBackEnd();