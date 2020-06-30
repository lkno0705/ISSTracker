<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
<div id="countryPasses">
<h2>The number of overflys over Country</h2>
<div class="info-container">
	<div class="issCountyPasses-container"><xsl:value-of select="Request/data/numberOfPasses" /></div>
	<xsl:for-each select="Request/data/passes/pass">
	<div class="myPopUp">
		<div class="text-startTime"><xsl:value-of select="startTime" /></div>
		<div class="text-endTime"><xsl:value-of select="endTime"/></div>
	</div>
	</xsl:for-each>
</div>
</div>
</xsl:template>
</xsl:stylesheet>