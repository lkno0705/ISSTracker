<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">	
		<div id="astrosOnIss">	
		  <h2>Crew on board the ISS</h2>		  
		<div class="slideshow-container">		 
			<xsl:for-each select="Request/data/Astro">
			<div class="mySlides fade">
			<div class="innerSlider">
			  <span><xsl:value-of select="./@name"/></span>
			  <span>
				<img class="portrait">
					<xsl:attribute name="SRC">			
						<xsl:value-of select="picture"/>
					</xsl:attribute>
				</img>
			  </span>
			  <span>
				<img class="flag">
					<xsl:attribute name="SRC">
						<xsl:value-of select="flag"/>
					</xsl:attribute>
				</img>
			  </span>
			  <span><xsl:value-of select="nation"/></span>
			</div>
			</div>
			</xsl:for-each>		
			<a class="prev" onclick="plusSlides(-1)">&#10094;</a>
			<a class="next" onclick="plusSlides(1)">&#10095;</a>			
		  </div>
		</div>	
</xsl:template>
</xsl:stylesheet>