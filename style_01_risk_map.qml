<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.28.0" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" minScale="1e+08" maxScale="0">
  <renderer-v2 attr="high_risk_total" type="graduatedSymbol" graduatedMethod="GraduatedColor" enableorderby="0">
    <ranges>
      <range lower="0.00" upper="10.00" symbol="0" label="0 - 10 จุด (เสี่ยงต่ำ)" render="true"/>
      <range lower="10.00" upper="35.00" symbol="1" label="11 - 35 จุด (เสี่ยงปานกลาง)" render="true"/>
      <range lower="35.00" upper="75.00" symbol="2" label="36 - 75 จุด (เสี่ยงสูง)" render="true"/>
      <range lower="75.00" upper="115.00" symbol="3" label="76 - 115 จุด (เสี่ยงสูงมาก)" render="true"/>
      <range lower="115.00" upper="200.00" symbol="4" label="116 - 185 จุด (วิกฤติสูงสุด)" render="true"/>
    </ranges>
    <symbols>
      <symbol name="0" type="fill" alpha="0.85" clip_to_extent="1">
        <layer class="SimpleFill" pass="0" locked="0">
          <prop k="color" v="254,240,217,255"/>
          <prop k="outline_color" v="255,255,255,255"/>
          <prop k="outline_width" v="0.4"/>
        </layer>
      </symbol>
      <symbol name="1" type="fill" alpha="0.85" clip_to_extent="1">
        <layer class="SimpleFill" pass="0" locked="0">
          <prop k="color" v="253,204,138,255"/>
          <prop k="outline_color" v="255,255,255,255"/>
          <prop k="outline_width" v="0.4"/>
        </layer>
      </symbol>
      <symbol name="2" type="fill" alpha="0.85" clip_to_extent="1">
        <layer class="SimpleFill" pass="0" locked="0">
          <prop k="color" v="252,141,89,255"/>
          <prop k="outline_color" v="255,255,255,255"/>
          <prop k="outline_width" v="0.4"/>
        </layer>
      </symbol>
      <symbol name="3" type="fill" alpha="0.85" clip_to_extent="1">
        <layer class="SimpleFill" pass="0" locked="0">
          <prop k="color" v="227,74,51,255"/>
          <prop k="outline_color" v="255,255,255,255"/>
          <prop k="outline_width" v="0.5"/>
        </layer>
      </symbol>
      <symbol name="4" type="fill" alpha="0.9" clip_to_extent="1">
        <layer class="SimpleFill" pass="0" locked="0">
          <prop k="color" v="179,0,0,255"/>
          <prop k="outline_color" v="255,255,255,255"/>
          <prop k="outline_width" v="0.6"/>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <labeling type="simple">
    <settings calloutType="simple">
      <text-style fontWordSpacing="0" textColor="0,0,0,255" textOpacity="1" fontLetterSpacing="0" isExpression="1" fontItalic="0" fontFamily="Sarabun" fontSizeUnit="Point" fontSize="9" previewBkClr="255,255,255,255" fontBold="1">
        <text-buffer bufferDraw="1" bufferSize="1" bufferColor="255,255,255,255"/>
      </text-style>
      <rule key="label" description="" expression="concat(&quot;amp_th&quot;, '
', &quot;high_risk_total&quot;, ' จุด')"/>
    </settings>
  </labeling>
</qgis>
