<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
  <h2>RSS Feed</h2>
  <table border="1">
    <tr bgcolor="#0b3d91">
      <th style="text-align:left">Title</th>
      <th style="text-align:left">News</th>
    </tr>
    <xsl:for-each select="channel/item">
    <tr>
      <td><xsl:value-of select="title"/></td>
      <td><xsl:value-of select="description"/></td>
    </tr>
    </xsl:for-each>
  </table>
</xsl:template>
</xsl:stylesheet>