<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
<div id="countryPasses">
<!-- <h2>The number of overflys over Country</h2> -->
<div class="info-container">
	<div class="issCountyPasses-container">
	<p class="text passes">
	<xsl:text>Amount of passes: </xsl:text>
	<xsl:value-of select="Request/data/numberOfPasses" />
	</p></div>
	<div class="myPopUp">
	<table border="1" align="center" style="border: none;">
	<tr>
		<th style="padding-inline-start: 5px; padding-inline-end: 5px;">Pass</th>
		<th>Start time</th>
		<th>End time</th>
	</tr>
	<xsl:for-each select="Request/data/passes/pass">
	<tr>
		<td><CurrentIteration><xsl:value-of select="position()" /></CurrentIteration></td>
		<td><div class="text startTime"><xsl:value-of select="startTime" /></div></td>
		<td><div class="text endTime"><xsl:value-of select="endTime"/></div></td>
	</tr>
	</xsl:for-each>
	</table>
	</div>
</div>
</div>
</xsl:template>
</xsl:stylesheet>