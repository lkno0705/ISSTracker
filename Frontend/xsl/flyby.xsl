<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<h2>Future </h2>
<div class="table-lefet-sidbar">
	<table border="1" align="center" style="border: none;">
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
</div>		
</xsl:template>
</xsl:stylesheet>