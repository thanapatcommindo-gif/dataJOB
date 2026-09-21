<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.28.0" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" minScale="1e+08" maxScale="0">
  <renderer-v2 attr="gap_status" type="categorizedSymbol" enableorderby="0">
    <categories>
      <category symbol="0" value="🚨 เสี่ยงสูงวิกฤติ - งบประมาณไม่เพียงพอ" label="🚨 เสี่ยงสูงวิกฤติ - งบประมาณไม่เพียงพอ" render="true"/>
      <category symbol="1" value="⚠️ เสี่ยงสูง - ได้รับงบประมาณต่อเนื่อง" label="⚠️ เสี่ยงสูง - ได้รับงบประมาณต่อเนื่อง" render="true"/>
      <category symbol="2" value="🟡 เสี่ยงปานกลาง - ควรเพิ่มงบประมาณ" label="🟡 เสี่ยงปานกลาง - ควรเพิ่มงบประมาณ" render="true"/>
      <category symbol="3" value="🔵 งบประมาณสูง - ความเสี่ยงต่ำ (โครงการโครงสร้างพื้นฐานหลัก)" label="🔵 งบประมาณสูง - ความเสี่ยงต่ำ (โครงสร้างพื้นฐาน)" render="true"/>
      <category symbol="4" value="🟢 สมดุลตามเกณฑ์" label="🟢 สมดุลตามเกณฑ์" render="true"/>
    </categories>
    <symbols>
      <symbol name="0" type="fill" alpha="0.9" clip_to_extent="1">
        <layer class="SimpleFill" pass="0" locked="0">
          <prop k="color" v="239,68,68,255"/>
          <prop k="outline_color" v="185,28,28,255"/>
          <prop k="outline_width" v="0.6"/>
        </layer>
      </symbol>
      <symbol name="1" type="fill" alpha="0.85" clip_to_extent="1">
        <layer class="SimpleFill" pass="0" locked="0">
          <prop k="color" v="249,115,22,255"/>
          <prop k="outline_color" v="194,65,12,255"/>
          <prop k="outline_width" v="0.5"/>
        </layer>
      </symbol>
      <symbol name="2" type="fill" alpha="0.85" clip_to_extent="1">
        <layer class="SimpleFill" pass="0" locked="0">
          <prop k="color" v="234,179,8,255"/>
          <prop k="outline_color" v="161,98,7,255"/>
          <prop k="outline_width" v="0.4"/>
        </layer>
      </symbol>
      <symbol name="3" type="fill" alpha="0.85" clip_to_extent="1">
        <layer class="SimpleFill" pass="0" locked="0">
          <prop k="color" v="59,130,246,255"/>
          <prop k="outline_color" v="29,78,216,255"/>
          <prop k="outline_width" v="0.4"/>
        </layer>
      </symbol>
      <symbol name="4" type="fill" alpha="0.85" clip_to_extent="1">
        <layer class="SimpleFill" pass="0" locked="0">
          <prop k="color" v="34,197,94,255"/>
          <prop k="outline_color" v="21,128,61,255"/>
          <prop k="outline_width" v="0.4"/>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <labeling type="simple">
    <settings calloutType="simple">
      <text-style fontWordSpacing="0" textColor="0,0,0,255" textOpacity="1" fontLetterSpacing="0" isExpression="0" fontItalic="0" fontFamily="Sarabun" fontSizeUnit="Point" fontSize="9" previewBkClr="255,255,255,255" fontBold="1" fieldName="amp_th">
        <text-buffer bufferDraw="1" bufferSize="1" bufferColor="255,255,255,255"/>
      </text-style>
    </settings>
  </labeling>
</qgis>
