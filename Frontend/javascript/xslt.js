// Function to load xml File via URL
function load(url, callback) {
    var req = new XMLHttpRequest();
    req.open('GET', url);
    // to allow us doing XSLT in IE
    try { req.responseType = "document" } catch (ex) {}
    req.onload = function() {
      callback(req.responseXML);
    };
    req.send();
  }
  
// transform xml with xsl 
  function transform(xml, xsl,target) {
    load(
      xml,
      function(inputXml) {
        load(
          xsl,
          function(xsltSheet) {
            displayResult(inputXml, xsltSheet,target);
          }
        );
      }
    );
  }

// display result of xsl tranformation
  function displayResult(xmlInput, xsltSheet,target) {
    if (typeof XSLTProcessor !== 'undefined') {
      var proc = new XSLTProcessor();
      proc.importStylesheet(xsltSheet);
      document.getElementById(target).appendChild(proc.transformToFragment(xmlInput, document));
    }
    else if (typeof xmlInput.transformNode !== 'undefined') {
      document.getElementById(target).innerHTML = xmlInput.transformNode(xsltSheet);
    }
  }

//  test call
  transform('xml/spacetoground_vodcast.xml', 'xsl/rssfeednasa.xsl',"mySidebar");