<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<h2>Future passes</h2>
<div class="tableLeftSideBar">
	<table border="1" align="center" style="border: none;">
		<tr>
			<th><div class="table-left-sidebar">Pass time</div></th>
			<th><div class="table-left-sidebar">Duration</div></th>
		</tr>
	<xsl:for-each select="Request/data/timeValue/time">
		<tr class="table-left-sidebar">
			<td><div class="text table-left-sidebar"><xsl:value-of select="futurePassDatetime"/></div></td>
			<td><div class="text table-left-sidebar"><xsl:value-of select="duration"/><xsl:text> s</xsl:text></div></td>
		</tr>
	</xsl:for-each>	
	</table>
</div>		
</xsl:template>
</xsl:stylesheet>