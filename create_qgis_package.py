import os
import json

print('Generating QGIS Project and Style Package...')

# 1. Generate QML Style for Risk Map (Graduated Yellow-Red)
qml_risk = '''<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
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
      <rule key="label" description="" expression="concat(&quot;amp_th&quot;, '\n', &quot;high_risk_total&quot;, ' จุด')"/>
    </settings>
  </labeling>
</qgis>
'''

# 2. Generate QML Style for Budget Map (Graduated Light Blue - Deep Teal)
qml_budget = '''<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
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
      <rule key="label" description="" expression="concat(&quot;amp_th&quot;, '\n', format_number(&quot;total_budget&quot;, 1), ' ลบ.')"/>
    </settings>
  </labeling>
</qgis>
'''

# 3. Generate QML Style for Gap Analysis (Categorized)
qml_gap = '''<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
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
'''

# 4. Generate Master QGIS Project File (.qgs)
geojson_abs_path = os.path.abspath('chiangmai_districts_gis.geojson')

qgs_project_xml = f'''<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis projectname="ChiangMai_Water_Risk_Budget_QGIS" version="3.28.0">
  <homePath path=""/>
  <title>โครงการแผนที่ GIS วิเคราะห์ความเสี่ยงและงบประมาณแผนน้ำเชียงใหม่ (2565-2570)</title>
  <autotransaction active="0"/>
  <evaluateDefaultValues active="0"/>
  <trust active="0"/>
  <projectCrs>
    <spatialrefsys nativeFormat="Wkt">
      <wkt>GEOGCRS["WGS 84",DATUM["World Geodetic System 1984",ELLIPSOID["WGS 84",6378137,298.257223563,LENGTHUNIT["metre",1]]],PRIMEM["Greenwich",0,ANGLEUNIT["degree",0.0174532925199433]],CS[ellipsoidal,2],AXIS["geodetic latitude (Lat)",north,ORDER[1],ANGLEUNIT["degree",0.0174532925199433]],AXIS["geodetic longitude (Lon)",east,ORDER[2],ANGLEUNIT["degree",0.0174532925199433]],USAGE[SCOPE["Horizontal component of 3D system."],AREA["World."],BBOX[-90,-180,90,180]],ID["EPSG",4326]]</wkt>
      <proj4>+proj=longlat +datum=WGS84 +no_defs</proj4>
      <srsid>3452</srsid>
      <srid>4326</srid>
      <authid>EPSG:4326</authid>
      <description>WGS 84</description>
      <projectionacronym>longlat</projectionacronym>
      <ellipsoidacronym>EPSG:7030</ellipsoidacronym>
      <geographicflag>true</geographicflag>
    </spatialrefsys>
  </projectCrs>
  <layer-tree-group>
    <customproperties>
      <Option/>
    </customproperties>
    <layer-tree-layer id="layer_risk" name="🚨 1. แผนที่ระดับความเสี่ยงภัยน้ำ (Risk Map)" source="{geojson_abs_path}|layername=chiangmai_districts_gis" providerKey="ogr" checked="Qt::Checked" expanded="1"/>
    <layer-tree-layer id="layer_budget" name="💰 2. แผนที่การจัดสรรงบประมาณ (Budget Map)" source="{geojson_abs_path}|layername=chiangmai_districts_gis" providerKey="ogr" checked="Qt::Unchecked" expanded="1"/>
    <layer-tree-layer id="layer_gap" name="⚖️ 3. แผนที่วิเคราะห์ช่องว่าง (Gap Analysis Status)" source="{geojson_abs_path}|layername=chiangmai_districts_gis" providerKey="ogr" checked="Qt::Unchecked" expanded="1"/>
    <custom-order enabled="0"/>
  </layer-tree-group>
  <maplayers>
    <maplayer id="layer_risk" type="vector" geometry="Polygon" minScale="1e+08" maxScale="0" refreshOnNotifyEnabled="0" refreshOnNotifyMessage="" hasScaleBasedVisibilityFlag="0" styleCategories="AllStyleCategories" autoRefreshTime="0" autoRefreshEnabled="0">
      <id>layer_risk</id>
      <datasource>{geojson_abs_path}|layername=chiangmai_districts_gis</datasource>
      <keywordList><value></value></keywordList>
      <layername>🚨 1. แผนที่ระดับความเสี่ยงภัยน้ำ (Risk Map)</layername>
      <srs>
        <spatialrefsys nativeFormat="Wkt">
          <authid>EPSG:4326</authid>
          <description>WGS 84</description>
        </spatialrefsys>
      </srs>
      <provider encoding="UTF-8">ogr</provider>
      {qml_risk.replace("<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>", "").replace('<qgis version="3.28.0" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" minScale="1e+08" maxScale="0">', "").replace('</qgis>', '')}
    </maplayer>

    <maplayer id="layer_budget" type="vector" geometry="Polygon" minScale="1e+08" maxScale="0" refreshOnNotifyEnabled="0" refreshOnNotifyMessage="" hasScaleBasedVisibilityFlag="0" styleCategories="AllStyleCategories" autoRefreshTime="0" autoRefreshEnabled="0">
      <id>layer_budget</id>
      <datasource>{geojson_abs_path}|layername=chiangmai_districts_gis</datasource>
      <keywordList><value></value></keywordList>
      <layername>💰 2. แผนที่การจัดสรรงบประมาณ (Budget Map)</layername>
      <srs>
        <spatialrefsys nativeFormat="Wkt">
          <authid>EPSG:4326</authid>
          <description>WGS 84</description>
        </spatialrefsys>
      </srs>
      <provider encoding="UTF-8">ogr</provider>
      {qml_budget.replace("<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>", "").replace('<qgis version="3.28.0" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" minScale="1e+08" maxScale="0">', "").replace('</qgis>', '')}
    </maplayer>

    <maplayer id="layer_gap" type="vector" geometry="Polygon" minScale="1e+08" maxScale="0" refreshOnNotifyEnabled="0" refreshOnNotifyMessage="" hasScaleBasedVisibilityFlag="0" styleCategories="AllStyleCategories" autoRefreshTime="0" autoRefreshEnabled="0">
      <id>layer_gap</id>
      <datasource>{geojson_abs_path}|layername=chiangmai_districts_gis</datasource>
      <keywordList><value></value></keywordList>
      <layername>⚖️ 3. แผนที่วิเคราะห์ช่องว่าง (Gap Analysis Status)</layername>
      <srs>
        <spatialrefsys nativeFormat="Wkt">
          <authid>EPSG:4326</authid>
          <description>WGS 84</description>
        </spatialrefsys>
      </srs>
      <provider encoding="UTF-8">ogr</provider>
      {qml_gap.replace("<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>", "").replace('<qgis version="3.28.0" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" minScale="1e+08" maxScale="0">', "").replace('</qgis>', '')}
    </maplayer>
  </maplayers>
</qgis>
'''

# Save files
with open('style_01_risk_map.qml', 'w', encoding='utf-8') as f:
    f.write(qml_risk)

with open('style_02_budget_map.qml', 'w', encoding='utf-8') as f:
    f.write(qml_budget)

with open('style_03_gap_status.qml', 'w', encoding='utf-8') as f:
    f.write(qml_gap)

with open('ChiangMai_Water_QGIS_Project.qgs', 'w', encoding='utf-8') as f:
    f.write(qgs_project_xml)

print('QGIS Assets created successfully:')
print('1. ChiangMai_Water_QGIS_Project.qgs (QGIS Master Project)')
print('2. style_01_risk_map.qml')
print('3. style_02_budget_map.qml')
print('4. style_03_gap_status.qml')
