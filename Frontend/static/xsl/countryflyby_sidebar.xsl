<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
	<xsl:choose>
		<xsl:when test="//Request/data/numberOfPasses[text() = 0]">		
				<p class="text passes">
					<xsl:text>No passes in the last 12h</xsl:text>
				</p>			
		</xsl:when>
		<xsl:when test="//Request/data/numberOfPasses[text() &gt; 0]">		
				<p class="text passes">
					<xsl:text>Amount of passes: </xsl:text>
					<xsl:value-of select="Request/data/numberOfPasses" />
				</p>
			<div class="leftBottomTable">
			<table border="1" align="center" style="border: none;">
				<tr>					
					<th><div class="table-left-sidebar">Start time</div></th>
					<th><div class="table-left-sidebar">End time</div></th>
				</tr>
			<xsl:for-each select="Request/data/passes/pass">
				<tr>					
					<td><div class="text table-left-sidebar"><xsl:value-of select="startTime" /></div></td>
					<td><div class="text table-left-sidebar"><xsl:value-of select="endTime"/></div></td>
				</tr>
			</xsl:for-each>
			</table>
			</div>
		</xsl:when>
		<xsl:otherwise />
	</xsl:choose>
</xsl:template>
</xsl:stylesheet>