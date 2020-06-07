function loadXMLDoc(filename)
{
if (window.ActiveXObject)
  {
  xhttp = new ActiveXObject("Msxml2.XMLHTTP");
  }
else
  {
  xhttp = new XMLHttpRequest();
  }
xhttp.open("GET", filename, true);
try {xhttp.responseType = "document"} catch(err) {} // Helping IE11
xhttp.send("");
return xhttp.responseXML;
}

function xslTransform(xmlFile,xslFile)
{
xml = coordinate2pixel(loadXMLDoc(xmlFile));
xsl = loadXMLDoc(xslFile);
var s = new XMLSerializer();
// code for IE
if (window.ActiveXObject || xhttp.responseType == "document")
  {
  ex = xml.transformNode(xsl);
//   document.getElementById("example").innerHTML = ex;
return s.serializeToString(resultDocument);
  }
// code for Chrome, Firefox, Opera, etc.
else if (document.implementation && document.implementation.createDocument)
  {
  xsltProcessor = new XSLTProcessor();
  xsltProcessor.importStylesheet(xsl);
  resultDocument = xsltProcessor.transformToFragment(xml, document);
//   document.getElementById("example").appendChild(resultDocument);
 
  return s.serializeToString(resultDocument);
  }
  
}

function coordinate2pixel(xmlFile){  
  load (xmlFile, function (xmlDoc){
  var x = xmlDoc.documentElement;
  var y = xmlDoc.documentElement.childNodes;  
  var lon,lat;
  var coordinates = {};
  coordinates.points=[];
  
  for (i=0;i<y.length;i++)
  {
  if (y[i].nodeType!=3)
  {
    for (z=0;z<y[i].childNodes.length;z++)
      {
      if (y[i].childNodes[z].nodeType!=3 && y[i].childNodes[z].nodeName=="lon")
        {
          lon =y[i].childNodes[z].childNodes[0].nodeValue;
        }
      if (y[i].childNodes[z].nodeType!=3 && y[i].childNodes[z].nodeName=="lat")
        {
          lat =y[i].childNodes[z].childNodes[0].nodeValue;
        }
        if (lon && lat)
        {
        var latlng = L.latLng(lat, lon);       
        map = window.mymap;
        var point = map.latLngToContainerPoint(latlng); 
        coordinates.points.push(point);
       lon="";
       lat="";
      }
      }
    }
  }
  console.log(coordinates);
  var xml = objectToXml(coordinates);
  var x=5;
  });
}

function objectToXml(object) {
  var xml = '';
  xml += "<coordinates>"
  for (var i=0;i<object.points.length;i++)
    {
      xml +=  "<point>";
      xml += "<x>"+object.points[i].x+"</x>";
      xml += "<y>"+object.points[i].y+"</y>";
      xml += "</point>";
    }
    xml += "</coordinates>"
  return xml;
}



