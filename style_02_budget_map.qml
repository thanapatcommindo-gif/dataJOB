<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.28.0" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" minScale="1e+08" maxScale="0">
  <renderer-v2 attr="total_budget" type="graduatedSymbol" graduatedMethod="GraduatedColor" enableorderby="0">
    <ranges>
      <range lower="0.00" upper="400.00" symbol="0" label="0 - 400 ลบ. (งบน้อย)" render="true"/>
      <range lower="400.00" upper="800.00" symbol="1" label="401 - 800 ลบ. (งบปานกลาง)" render="true"/>
      <range lower="800.00" upper="1500.00" symbol="2" label="801 - 1,500 ลบ. (งบสูง)" render="true"/>
      <range lower="1500.00" upper="3000.00" symbol="3" label="1,501 - 3,000 ลบ. (งบสูงมาก)" render="true"/>
      <range lower="3000.00" upper="6000.00" symbol="4" label="3,001 - 5,000 ลบ. (งบสูงสุด)" render="true"/>
    </ranges>
    <symbols>
      <symbol name="0" type="fill" alpha="0.85" clip_to_extent="1">
        <layer class="SimpleFill" pass="0" locked="0">
          <prop k="color" v="241,238,246,255"/>
          <prop k="outline_color" v="255,255,255,255"/>
          <prop k="outline_width" v="0.4"/>
        </layer>
      </symbol>
      <symbol name="1" type="fill" alpha="0.85" clip_to_extent="1">
        <layer class="SimpleFill" pass="0" locked="0">
          <prop k="color" v="189,201,225,255"/>
          <prop k="outline_color" v="255,255,255,255"/>
          <prop k="outline_width" v="0.4"/>
        </layer>
      </symbol>
      <symbol name="2" type="fill" alpha="0.85" clip_to_extent="1">
        <layer class="SimpleFill" pass="0" locked="0">
          <prop k="color" v="116,169,207,255"/>
          <prop k="outline_color" v="255,255,255,255"/>
          <prop k="outline_width" v="0.4"/>
        </layer>
      </symbol>
      <symbol name="3" type="fill" alpha="0.85" clip_to_extent="1">
        <layer class="SimpleFill" pass="0" locked="0">
          <prop k="color" v="43,140,190,255"/>
          <prop k="outline_color" v="255,255,255,255"/>
          <prop k="outline_width" v="0.5"/>
        </layer>
      </symbol>
      <symbol name="4" type="fill" alpha="0.9" clip_to_extent="1">
        <layer class="SimpleFill" pass="0" locked="0">
          <prop k="color" v="4,90,141,255"/>
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
', format_number(&quot;total_budget&quot;, 1), ' ลบ.')"/>
    </settings>
  </labeling>
</qgis>
