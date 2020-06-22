<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<div id="astrosOnIss">
  <h2>Crew on board the ISS</h2>
  <table>
    <xsl:for-each select="Request/data/Astro">
    <tr>
      <td><xsl:value-of select="./@name"/></td>
      <td>
		<img class="portrait">
			<xsl:attribute name="SRC">			
				<xsl:value-of select="picture"/>
			</xsl:attribute>
		</img>
	  </td>
      <td>
		<img class="flag">
			<xsl:attribute name="SRC">
				<xsl:value-of select="flag"/>
			</xsl:attribute>
		</img>
	  </td>
      <td><xsl:value-of select="nation"/></td>
    </tr>
    </xsl:for-each>
  </table>
</div>
</xsl:template>
</xsl:stylesheet>