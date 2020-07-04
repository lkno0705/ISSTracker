<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
<div class="info-container">
	<xsl:choose>
		<xsl:when test="//Request/data/numberOfPasses[text() = 0]">
			<div class="issCountyPasses-container">
				<p class="text passes">
					<xsl:text>No passes in the last 12h</xsl:text>
				</p>
			</div>
		</xsl:when>
		<xsl:when test="//Request/data/numberOfPasses[text() &gt; 0]">
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
		</xsl:when>
		<xsl:otherwise />
	</xsl:choose>
</div>
</xsl:template>
</xsl:stylesheet>