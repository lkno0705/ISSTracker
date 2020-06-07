<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/"> 


<polyline>
 <xsl:attribute name="points">
<xsl:for-each select="coordinates/point">
				<xsl:value-of select="x"/>,<xsl:value-of select="y"/><xsl:text> </xsl:text>
 </xsl:for-each>
 </xsl:attribute>
 </polyline>


</xsl:template>

</xsl:stylesheet>