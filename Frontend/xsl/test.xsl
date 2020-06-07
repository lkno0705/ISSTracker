<xsl:stylesheet
   version="1.0"
   xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
   xmlns="http://www.w3.org/2000/svg"
>
  <xsl:output indent="yes" cdata-section-elements="style" />

  <xsl:param name="width" select="40" /><!-- width of bars -->
  <xsl:param name="space" select="10" /><!-- space between bars and items -->

  <xsl:variable name="max-y" select="//detail[not(//detail &gt; .)][1]" />

  <xsl:template match="root">
    <svg>
      <defs>
        <style type="text/css"><![CDATA[
          g.bar text {
            font-family: Arial; 
            text-anchor: middle;
            fill: white;
          }
          g.bar rect {
            fill: black;
          }
        ]]></style>
      </defs>
      <g transform="translate(10, 10)">
        <xsl:apply-templates select="item" />
      </g>
    </svg>
  </xsl:template>

  <xsl:template match="item">
    <xsl:variable name="prev-item" select="preceding-sibling::item" />
    <g class="item" id="item-{position()}" transform="translate({
      count($prev-item/detail) * ($width + $space)
      + count($prev-item) * $space
    })">
      <xsl:apply-templates select="detail" />
    </g>
  </xsl:template>

  <xsl:template match="detail">
    <xsl:variable name="idx" select="count(preceding-sibling::detail)" />
    <xsl:variable name="pos" select="$idx * ($width + $space)" />
    <g class="bar">
      <rect x="{$pos}" y="{$max-y - .}" height="{.}" width="{$width}" />
      <text x="{$pos + $width div 2.0}" y="{$max-y - $space}">
        <xsl:value-of select="."/>
      </text>
    </g>
  </xsl:template>
</xsl:stylesheet>