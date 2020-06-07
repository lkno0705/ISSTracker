// function to get xml transform with xsl and draw as svg.

function load(url, callback) {
    var req = new XMLHttpRequest();
    req.open('GET', url);
    // to allow us doing XSLT in IE
    try { req.responseType = "msxml-document" } catch (ex) {}
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
      document.getElementById('test').appendChild(proc.transformToFragment(xmlInput, document));
    }
    else if (typeof xmlInput.transformNode !== 'undefined') {
      document.getElementById("test").innerHTML = xmlInput.transformNode(xsltSheet);
    }
  }
  //test call
  transform('SVGTest.xml', 'SVGTest.xsl');