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
  
  function transform(xml, xsl) {
    load(
      xml,
      function(inputXml) {
        load(
          xsl,
          function(xsltSheet) {
            displayResult(inputXml, xsltSheet);
          }
        );
      }
    );
  }
  
  function displayResult(xmlInput, xsltSheet) {
    if (typeof XSLTProcessor !== 'undefined') {
      var proc = new XSLTProcessor();
      proc.importStylesheet(xsltSheet);
      document.getElementById('mySidebar').appendChild(proc.transformToFragment(xmlInput, document));
    }
    else if (typeof xmlInput.transformNode !== 'undefined') {
      document.getElementById("mySidebar").innerHTML = xmlInput.transformNode(xsltSheet);
    }
  }

  transform('spacetoground_vodcast.xml', 'rssfeednasa.xsl');