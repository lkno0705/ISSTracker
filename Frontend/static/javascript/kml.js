"use strict";

//call to get XML for KML
function callBackendDrawCounties(map) {
    var date = new Date();
    $.ajax({
        crossDomain: true,
        type: 'GET',
        url: 'xml/xmlForCounties.xml',
        xml: "application/xml",
        dataType: 'xml',
        success: function (oReturnData) { drawCounties(map, oReturnData) }
    });
}

// draw KML
function drawCounties(map, countiesXML) {
    // XSLT XML to KML
    transform3(countiesXML, 'xsl/CountiesXML2KML.xsl', function (oData) {
        // create new KML overlay
        const parser = new DOMParser();
        const kml = parser.parseFromString(oData,'text/html')
        const track = new L.KML(kml);
        map.addLayer(track);

        // adjust map to show the KML
        const bounds = track.getBounds();
        map.fitBounds(bounds);
    })
}
