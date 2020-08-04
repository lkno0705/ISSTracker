"use strict";

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
  load(xml, function(inputXml) {
      load(xsl, function(xsltSheet) {
          displayResult(inputXml, xsltSheet,target);
        });
    });
}

// xml transform with local xml
function transform2(xml, xsl, target) {  
  load(xsl, function(xsltSheet) {
      displayResult(xml, xsltSheet,target);
    });
}

// xml transform with callback handler
function transform3(xml, xsl, callback) {  
  load(xsl, function(xsltSheet) {
      callback(returnResult(xml, xsltSheet));
    });
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
  if (target == "pastpasses" || target == "flyby" || target == "countryContent"){
    var objDiv = document.getElementById("leftBottom");
    objDiv.scrollTop = objDiv.scrollHeight; 
  }  
}

// return for callback
function returnResult(xmlInput, xsltSheet) {
  if (typeof XSLTProcessor !== 'undefined') {
    var proc = new XSLTProcessor();
    proc.importStylesheet(xsltSheet);
    var xml = proc.transformToFragment(xmlInput, document);
    var xmlText = new XMLSerializer().serializeToString(xml)
   return xmlText
  }
  else if (typeof xmlInput.transformNode !== 'undefined') {
    return xmlInput.transformNode(xsltSheet);
  }
}