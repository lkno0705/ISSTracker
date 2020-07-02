<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<h2>Future passes</h2>
<table class="table-left-sidebar">
			<tr>
			<th class="table-left-sidebar">Pass time</th>
			<th class="table-left-sidebar">Duration</th>
			</tr>
			<xsl:for-each select="Request/data/timeValue/time">
			<tr class="table-left-sidebar">
				<td class="text table-left-sidebar"><xsl:value-of select="futurePassDatetime"/></td>
				<td class="text table-left-sidebar"><xsl:value-of select="duration"/><xsl:text> s</xsl:text></td>
			</tr>
			</xsl:for-each>		
</table>			
</xsl:template>
</xsl:stylesheet>