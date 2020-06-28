<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:template match="/">
		<gpx version="1.0">	
			<wpt></wpt>
				<trk>		
					<xsl:for-each select="Request/data/timeValue">		
						<trkpt>
						<xsl:attribute name="lat">			
							<xsl:value-of select="latitude"/>
						</xsl:attribute>
						<xsl:attribute name="lon">			
							<xsl:value-of select="longitude"/>
						</xsl:attribute>					
							<time><xsl:value-of select="./@time"/></time>
						</trkpt>				
					</xsl:for-each> 			
				</trk>
		</gpx>
	</xsl:template>
</xsl:stylesheet>
