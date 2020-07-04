<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:template match="/">
		<xsl:choose>
			<xsl:when test="//Request/data/numberOfPasses[text() &gt; 0]">
			<h2>Past passes</h2>
			<div class="leftBottomTable">
				<table border="1" align="center" style="border: none;">
					<tr>
						<th><div class="table-left-sidebar">Pass time</div></th>
						<th><div class="table-left-sidebar">Duration</div></th>
					</tr>
					<xsl:for-each select="Request/data/passes/pass">
					<tr>
						<td><div class="text table-left-sidebar"><xsl:value-of select="startTime" /></div></td>
						<td><div class="text table-left-sidebar"><xsl:value-of select="endTime" /></div></td>
					</tr>
					</xsl:for-each>	
				</table>
			</div>	
			</xsl:when>
			<xsl:otherwise>
            <h2>No passes in the past 12h</h2>
          	</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
</xsl:stylesheet>