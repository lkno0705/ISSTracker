<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:template match="/">						
					<xsl:for-each select="Request/data/countries/country">
						 <xsl:sort select="./@countryname" data-type="text" order="ascending"/>
                        <option>
							<xsl:attribute name="value">
							<xsl:value-of select="./@countryname"/>
							</xsl:attribute>
						</option>								
					</xsl:for-each>	
	</xsl:template>
</xsl:stylesheet>
