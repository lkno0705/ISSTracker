<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<h2>Past passes</h2>
<table class="table-left-sidebar">
			<tr>
			<th class="table-left-sidebar">Start time</th>
			<th class="table-left-sidebar">End time</th>
			</tr>
			<xsl:for-each select="Request/data/passes/pass">
			<tr  class="table-left-sidebar">
				<td class="text table-left-sidebar"><xsl:value-of select="startTime"/></td>
				<td class="text table-left-sidebar"><xsl:value-of select="endTime"/></td>
			</tr>
			</xsl:for-each>		
</table>	
</xsl:template>
</xsl:stylesheet>