<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template>          
                <xsl:apply-templates select="timeValue[longtitude &gt; preceding-sibling::timeValue/longtitude]"/>
                <xsl:apply-templates select="timeValue[last()]"/>          
    </xsl:template>

    <xsl:template match="timeValue">
            <xsl:variable name="posUpper" select="position()"/>
            <xsl:variable name="posLower">
                <xsl:choose>
                    <xsl:when test="count(timeValue[position() &lt; $posUpper and longtitude > preceding-sibling::timeValue/longtitude]) = 0">1</xsl:when>
                    <xsl:otherwise><xsl:value-of select="timeValue[position() &lt; $posUpper and longtitude > preceding-sibling::timeValue/longtitude][last()][position()]"/></xsl:otherwise>
                </xsl:choose>
            </xsl:variable>
            <xsl:if test="count(timeValue[position() > $posLower and position() &gt; $posUpper]) > 0">
                <trk>
                    <xsl:for-each select="timeValue[position() > $posLower and position() &lt; $posUpper]">
                        <trkpt>  
                        </trkpt>
                    </xsl:for-each>
                </trk>
            </xsl:if>
    </xsl:template>

</xsl:stylesheet>