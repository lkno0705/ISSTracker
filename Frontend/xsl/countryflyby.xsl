<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
        <div id="countryFlyBys">
         <h2>The amount of overflights over Country</h2>
        <div class="info-container">
            <div class="numberofPasses-container">
            <div class="text numberofPasses"><xsl:value-of select="numberOfPasses"/></div>
            <div class="startTime-container">
            <div class="text startTime"><xsl:value-of select="startTime"/></div>
            <div class="endTime-container">
            <div class="text endTime"><xsl:value-of select="endTime"/></div>
            </div>
            </div>
            </div>
        </div>
</xsl:template>
</xsl:stylesheet>