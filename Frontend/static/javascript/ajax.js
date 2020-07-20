"use strict";

// jQuery AJAX call to back end. 

var ajaxCall = function(oData){
    var date = new Date;    // date for time stamp
    if(!oData.e) // if event is associated with call
        oData.e= "";
    if (oData.type == "POST") // post call
    {
     oData.data =   '<?xml version=\'1.0\' encoding=\'UTF-8\'?>' + 
                    '<!DOCTYPE Request SYSTEM \'./DTD/' + oData.call + '.dtd\'>' + 
                    "<Request>" +
                       oData.data +
                    "</Request>";
        $.ajax({
            crossDomain: true, // CORS
            contentType: "application/xml; charset=utf-8",    
            type: oData.type,
            url: 'https://iss-trackr-api.azurewebsites.net/' + oData.call,        
            xml: "application/xml",
            dataType: 'xml',
            headers: {  'Access-Control-Allow-Origin': 'https://iss-trackr-api.azurewebsites.net/' + oData.call},   // CORS
            data: oData.data,
            success: function(oReturnData) { oData.callback(oReturnData, oData.e); },
            error: function() { oData.callback("error", ""); }      
        });
    }
    else // get call
    {
        $.ajax({
            crossDomain: true,  // CORS        
            type: oData.type,            
            url: 'https://iss-trackr-api.azurewebsites.net/' + oData.call, 
            xml: "application/xml",       
            dataType: 'xml',         
            success: function(oReturnData) { oData.callback(oReturnData, oData.e); } 
        });
    }
}