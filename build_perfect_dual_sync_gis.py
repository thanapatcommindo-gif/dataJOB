#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Perfect Dual Sync GIS Dashboard for Chiang Mai Water Master Plan
- Organic polygon boundary highlighting (No bounding boxes!)
- Both left & right maps synchronized on click and hover
- Seamless drilldown: District -> Subdistrict -> Village
- Clean Google Maps aesthetic
"""

import json

with open('chiangmai_districts_gis.geojson', 'r', encoding='utf-8') as f:
    districts_geojson = json.load(f)

with open('chiangmai_subdistricts_gis.geojson', 'r', encoding='utf-8') as f:
    subdistricts_geojson = json.load(f)

with open('chiangmai_villages_gis.geojson', 'r', encoding='utf-8') as f:
    villages_geojson = json.load(f)

with open('dashboard_data.json', 'r', encoding='utf-8') as f:
    dash_data = json.load(f)

districts_json_str = json.dumps(districts_geojson, ensure_ascii=False)
subdistricts_json_str = json.dumps(subdistricts_geojson, ensure_ascii=False)
villages_json_str = json.dumps(villages_geojson, ensure_ascii=False)
dash_data_json_str = json.dumps(dash_data, ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ระบบสารสนเทศภูมิศาสตร์ (GIS) เปรียบเทียบแผนแม่บทน้ำ จ.เชียงใหม่</title>
  
  <!-- Google Fonts & Material Icons -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
  
  <!-- Leaflet CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  
  <style>
    :root {{
      --primary: #1a73e8;
      --primary-dark: #1557b0;
      --bg: #f8fafd;
      --card-bg: #ffffff;
      --text-main: #202124;
      --text-sub: #5f6368;
      --border: #dadce0;
      --shadow: 0 2px 6px rgba(60,64,67, 0.12);
      --shadow-lg: 0 8px 24px rgba(60,64,67, 0.18);
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Prompt', 'Google Sans', sans-serif; }}
    body {{ background: var(--bg); color: var(--text-main); height: 100vh; display: flex; flex-direction: column; overflow: hidden; }}

    /* Remove outline on Leaflet SVG paths */
    path.leaflet-interactive:focus {{
      outline: none !important;
    }}
    svg:focus {{ outline: none !important; }}

    /* Top Google Navbar */
    header {{
      background: #ffffff;
      border-bottom: 1px solid var(--border);
      padding: 10px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      z-index: 1000;
      box-shadow: 0 1px 3px rgba(60,64,67, 0.08);
    }}
    .header-brand {{ display: flex; align-items: center; gap: 12px; }}
    .brand-icon {{
      width: 40px; height: 40px;
      background: linear-gradient(135deg, #1a73e8, #0d47a1);
      border-radius: 10px;
      display: flex; align-items: center; justify-content: center;
      color: #fff; font-size: 22px;
    }}
    .brand-title {{ font-size: 1.1rem; font-weight: 700; color: #1a73e8; line-height: 1.2; }}
    .brand-sub {{ font-size: 0.76rem; color: var(--text-sub); }}

    .header-kpis {{ display: flex; align-items: center; gap: 12px; }}
    .kpi-chip {{
      background: #f8f9fa;
      border: 1px solid var(--border);
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 0.8rem;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .kpi-chip strong {{ color: #1a73e8; font-weight: 700; }}

    /* Filter Action Bar (Top) */
    .filter-bar {{
      background: #ffffff;
      border-bottom: 1px solid var(--border);
      padding: 10px 24px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      z-index: 900;
    }}
    .filter-group {{ display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }}
    
    .search-input-wrap {{
      position: relative;
      width: 250px;
    }}
    .search-input-wrap input {{
      width: 100%;
      height: 36px;
      padding: 0 12px 0 34px;
      border: 1px solid var(--border);
      border-radius: 18px;
      font-size: 0.82rem;
      outline: none;
      background: #f8fafd;
    }}
    .search-input-wrap input:focus {{
      background: #fff;
      border-color: var(--primary);
    }}
    .search-input-wrap .material-symbols-outlined {{
      position: absolute;
      left: 10px;
      top: 9px;
      font-size: 18px;
      color: var(--text-sub);
    }}

    .filter-select {{
      height: 36px;
      padding: 0 12px;
      border: 1px solid var(--border);
      border-radius: 18px;
      font-size: 0.82rem;
      background: #ffffff;
      outline: none;
      cursor: pointer;
      font-weight: 500;
      color: var(--text-main);
    }}
    .filter-select:focus {{
      border-color: var(--primary);
    }}

    .layer-toggle-btn {{
      height: 36px;
      padding: 0 14px;
      border: 1px solid var(--border);
      border-radius: 18px;
      font-size: 0.82rem;
      background: #f8f9fa;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      font-weight: 600;
      color: var(--text-sub);
      transition: all 0.2s;
    }}
    .layer-toggle-btn.active {{
      background: #e8f0fe;
      color: #1a73e8;
      border-color: #aecbfa;
    }}

    /* Main Dual Map Layout */
    .dual-map-container {{
      flex: 1;
      display: grid;
      grid-template-columns: 1fr 1fr;
      position: relative;
      background: #eaebed;
      gap: 2px;
    }}

    .map-box {{
      position: relative;
      height: 100%;
      background: #fff;
    }}

    .map-header-badge {{
      position: absolute;
      top: 14px;
      left: 14px;
      z-index: 500;
      background: rgba(255, 255, 255, 0.96);
      backdrop-filter: blur(8px);
      padding: 8px 16px;
      border-radius: 20px;
      box-shadow: var(--shadow);
      border: 1px solid var(--border);
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.86rem;
      font-weight: 700;
    }}
    .badge-risk {{ color: #d93025; border-left: 4px solid #d93025; }}
    .badge-budget {{ color: #1a73e8; border-left: 4px solid #1a73e8; }}

    .map-legend-card {{
      position: absolute;
      bottom: 20px;
      left: 14px;
      z-index: 500;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(8px);
      padding: 10px 14px;
      border-radius: 12px;
      box-shadow: var(--shadow);
      border: 1px solid var(--border);
      font-size: 0.74rem;
    }}
    .legend-title {{ font-weight: 700; margin-bottom: 6px; color: var(--text-main); }}
    .legend-row {{ display: flex; align-items: center; gap: 8px; margin-bottom: 3px; }}
    .legend-color {{ width: 14px; height: 12px; border-radius: 3px; display: inline-block; }}

    /* Detail Modal Drawer */
    .info-panel {{
      position: absolute;
      bottom: 20px;
      right: 14px;
      z-index: 600;
      width: 380px;
      background: #ffffff;
      border-radius: 16px;
      box-shadow: var(--shadow-lg);
      border: 1px solid var(--border);
      display: none;
      flex-direction: column;
      overflow: hidden;
      animation: slideUp 0.2s ease-out;
    }}
    @keyframes slideUp {{
      from {{ transform: translateY(20px); opacity: 0; }}
      to {{ transform: translateY(0); opacity: 1; }}
    }}
    .panel-header {{
      padding: 12px 18px;
      background: #f8fafd;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .panel-header h4 {{ font-size: 0.95rem; font-weight: 700; color: #1a73e8; }}
    .panel-close {{ background: none; border: none; cursor: pointer; color: var(--text-sub); }}
    .panel-body {{ padding: 16px 18px; max-height: 380px; overflow-y: auto; font-size: 0.84rem; }}

    .district-pill {{
      background: #ffffff;
      border: 1.5px solid #1a73e8;
      border-radius: 14px;
      padding: 2px 7px;
      font-size: 11px;
      font-weight: 600;
      color: #1a73e8;
      box-shadow: 0 1px 4px rgba(0,0,0,0.15);
      white-space: nowrap;
      pointer-events: none;
    }}
  </style>
</head>
<body>

  <!-- Top Brand Navigation Header -->
  <header>
    <div class="header-brand">
      <div class="brand-icon">
        <span class="material-symbols-outlined">water_drop</span>
      </div>
      <div>
        <div class="brand-title">ระบบแผนที่ GIS เปรียบเทียบแผนแม่บทบริหารจัดการน้ำ จ.เชียงใหม่</div>
        <div class="brand-sub">เปรียบเทียบจุดเสี่ยง 5 มิติ (2,200 หมู่บ้าน) vs งบประมาณที่ได้รับจัดสรร 65-70 (3.5 หมื่นล้านบาท)</div>
      </div>
    </div>

    <div class="header-kpis">
      <div class="kpi-chip">
        <span class="material-symbols-outlined" style="color:#1a73e8; font-size:18px;">payments</span>
        งบประมาณรวม: <strong>35,094.77 ลบ.</strong>
      </div>
      <div class="kpi-chip">
        <span class="material-symbols-outlined" style="color:#1a73e8; font-size:18px;">construction</span>
        โครงการ: <strong>6,312 โครงการ</strong>
      </div>
      <div class="kpi-chip">
        <span class="material-symbols-outlined" style="color:#d93025; font-size:18px;">warning</span>
        จุดเสี่ยง: <strong>2,200 หมู่บ้าน</strong>
      </div>
    </div>
  </header>

  <!-- Filter & Control Bar (Clean Top Bar) -->
  <div class="filter-bar">
    <div class="filter-group">
      
      <!-- Search Input -->
      <div class="search-input-wrap">
        <span class="material-symbols-outlined">search</span>
        <input type="text" id="searchInput" placeholder="ค้นหา อำเภอ / ตำบล / หมู่บ้าน..." oninput="onSearchInput()">
      </div>

      <!-- District Selector -->
      <select class="filter-select" id="districtSelect" onchange="onDistrictChange()">
        <option value="all">📍 ทุกอำเภอ (25 อำเภอ)</option>
      </select>

      <!-- Subdistrict Selector -->
      <select class="filter-select" id="subdistrictSelect" onchange="onSubdistrictChange()">
        <option value="all">🏘️ ทุกตำบล (194 ตำบล)</option>
      </select>

      <!-- 5 Pillars Selector -->
      <select class="filter-select" id="pillarSelect" onchange="onPillarChange()">
        <option value="all">🌟 รวม 5 ด้านแผนแม่บท</option>
        <option value="p1">💧 ด้าน 1: น้ำอุปโภคบริโภค</option>
        <option value="p2">🌾 ด้าน 2: น้ำภาคการผลิต (เกษตร)</option>
        <option value="p3">🌊 ด้าน 3: น้ำท่วมและอุทกภัย</option>
        <option value="p4">🧪 ด้าน 4: คุณภาพน้ำและการอนุรักษ์</option>
        <option value="p5">🌲 ด้าน 5: ฟื้นฟูป่าต้นน้ำดินพังทลาย</option>
      </select>

      <!-- Risk Level Score Selector -->
      <select class="filter-select" id="riskLevelSelect" onchange="onFilterUpdate()">
        <option value="all">⚡ ทุกระดับความเสี่ยง</option>
        <option value="เสี่ยงสูง">🚨 เสี่ยงสูง (คะแนน 3)</option>
        <option value="เสี่ยงปานกลาง">🟡 เสี่ยงปานกลาง (คะแนน 2)</option>
        <option value="เสี่ยงน้อย">🟢 เสี่ยงน้อย (คะแนน 1)</option>
      </select>
    </div>

    <!-- Toggle Village Points Layer -->
    <div class="filter-group">
      <button class="layer-toggle-btn active" id="btn-toggle-villages" onclick="toggleVillagePoints()">
        <span class="material-symbols-outlined" style="font-size:18px;">pin_drop</span>
        <span>แสดงจุดพิกัด 2,200 หมู่บ้าน</span>
      </button>

      <button class="layer-toggle-btn" onclick="resetToOverview()" title="จัดกึ่งกลางเชียงใหม่">
        <span class="material-symbols-outlined" style="font-size:18px;">restart_alt</span>
        <span>รีเซ็ตมุมมอง</span>
      </button>
    </div>
  </div>

  <!-- Dual Maps Container (Side-by-Side Sync) -->
  <div class="dual-map-container">
    
    <!-- Left Map: Risk Analysis (Choropleth + Village Dots) -->
    <div class="map-box">
      <div class="map-header-badge badge-risk">
        <span class="material-symbols-outlined" style="font-size:18px;">warning</span>
        <span id="risk-map-title">1. แผนที่ระดับความเสี่ยง (2,200 หมู่บ้าน)</span>
      </div>
      <div id="map-risk" style="height:100%; width:100%;"></div>

      <!-- Risk Legend -->
      <div class="map-legend-card">
        <div class="legend-title" id="legend-risk-title">ความหนาแน่นจุดเสี่ยงสูง</div>
        <div class="legend-row"><span class="legend-color" style="background:#b71c1c;"></span> เสี่ยงสูงวิกฤติ (> 70 จุด)</div>
        <div class="legend-row"><span class="legend-color" style="background:#e53935;"></span> เสี่ยงสูงมาก (40 - 70 จุด)</div>
        <div class="legend-row"><span class="legend-color" style="background:#fb8c00;"></span> เสี่ยงปานกลาง (20 - 40 จุด)</div>
        <div class="legend-row"><span class="legend-color" style="background:#fdd835;"></span> เสี่ยงน้อย (10 - 20 จุด)</div>
        <div class="legend-row"><span class="legend-color" style="background:#43a047;"></span> ต่ำมาก (< 10 จุด)</div>
      </div>
    </div>

    <!-- Right Map: Budget Allocation (Choropleth) -->
    <div class="map-box">
      <div class="map-header-badge badge-budget">
        <span class="material-symbols-outlined" style="font-size:18px;">payments</span>
        <span id="budget-map-title">2. แผนที่งบประมาณจัดสรร 65-70 (3.5 หมื่นลบ.)</span>
      </div>
      <div id="map-budget" style="height:100%; width:100%;"></div>

      <!-- Budget Legend -->
      <div class="map-legend-card">
        <div class="legend-title">วงเงินจัดสรรรายอำเภอ</div>
        <div class="legend-row"><span class="legend-color" style="background:#0d47a1;"></span> สูงมาก (> 3,000 ล้านบาท)</div>
        <div class="legend-row"><span class="legend-color" style="background:#1976d2;"></span> สูง (1,500 - 3,000 ล้านบาท)</div>
        <div class="legend-row"><span class="legend-color" style="background:#42a5f5;"></span> ปานกลาง (800 - 1,500 ล้านบาท)</div>
        <div class="legend-row"><span class="legend-color" style="background:#90caf9;"></span> น้อย (400 - 800 ล้านบาท)</div>
        <div class="legend-row"><span class="legend-color" style="background:#e3f2fd;"></span> น้อยมาก (< 400 ล้านบาท)</div>
      </div>
    </div>

    <!-- Detail Drawer Panel -->
    <div class="info-panel" id="infoPanel">
      <div class="panel-header">
        <h4 id="panelTitle">ข้อมูลพื้นที่</h4>
        <button class="panel-close" onclick="closePanel()">
          <span class="material-symbols-outlined">close</span>
        </button>
      </div>
      <div class="panel-body" id="panelBody"></div>
    </div>

  </div>

  <script>
    // Injected GeoJSON Datasets
    const DISTRICTS_DATA = {districts_json_str};
    const SUBDISTRICTS_DATA = {subdistricts_json_str};
    const VILLAGES_DATA = {villages_json_str};
    const SUMMARY_DATA = {dash_data_json_str};

    let mapRisk, mapBudget;
    let districtLayersRisk = {{}}, districtLayersBudget = {{}};
    let subdistrictLayersRisk = [], subdistrictLayersBudget = [];
    let villagePointsLayer;
    let showVillages = true;
    let isSyncing = false;
    let cmBounds;
    let selectedDistrict = 'all';
    let selectedSubdistrict = 'all';
    let selectedPillar = 'all';
    let selectedRiskLevel = 'all';

    window.addEventListener('DOMContentLoaded', () => {{
      initMaps();
      populateDropdowns();
      renderAllLayers();
      resetToOverview();
    }});

    function initMaps() {{
      const cmCenter = [18.7883, 98.9853];
      const initialZoom = 9;
      const googleMapsUrl = 'https://mt1.google.com/vt/lyrs=m&hl=th&x={{x}}&y={{y}}&z={{z}}';

      // Left Map
      mapRisk = L.map('map-risk', {{
        center: cmCenter,
        zoom: initialZoom,
        zoomControl: false
      }});
      L.tileLayer(googleMapsUrl, {{ maxZoom: 18, attribution: '© Google Maps' }}).addTo(mapRisk);
      L.control.zoom({{ position: 'bottomright' }}).addTo(mapRisk);

      // Right Map
      mapBudget = L.map('map-budget', {{
        center: cmCenter,
        zoom: initialZoom,
        zoomControl: false
      }});
      L.tileLayer(googleMapsUrl, {{ maxZoom: 18, attribution: '© Google Maps' }}).addTo(mapBudget);
      L.control.zoom({{ position: 'bottomright' }}).addTo(mapBudget);

      // Synchronize Left -> Right
      mapRisk.on('move', () => {{
        if (!isSyncing) {{
          isSyncing = true;
          mapBudget.setView(mapRisk.getCenter(), mapRisk.getZoom(), {{ animate: false }});
          isSyncing = false;
        }}
      }});

      // Synchronize Right -> Left
      mapBudget.on('move', () => {{
        if (!isSyncing) {{
          isSyncing = true;
          mapRisk.setView(mapBudget.getCenter(), mapBudget.getZoom(), {{ animate: false }});
          isSyncing = false;
        }}
      }});
    }}

    function populateDropdowns() {{
      const distSelect = document.getElementById('districtSelect');
      const districts = [...new Set(VILLAGES_DATA.features.map(f => f.properties.district))].sort((a,b) => a.localeCompare(b, 'th'));

      districts.forEach(d => {{
        const opt = document.createElement('option');
        opt.value = d;
        opt.textContent = `📍 อ.${{d}}`;
        distSelect.appendChild(opt);
      }});
    }}

    function onDistrictChange() {{
      selectedDistrict = document.getElementById('districtSelect').value;
      const subSelect = document.getElementById('subdistrictSelect');
      subSelect.innerHTML = '<option value="all">🏘️ ทุกตำบล</option>';

      if (selectedDistrict !== 'all') {{
        const subdistricts = [...new Set(
          VILLAGES_DATA.features
            .filter(f => f.properties.district === selectedDistrict)
            .map(f => f.properties.subdistrict)
        )].sort((a,b) => a.localeCompare(b, 'th'));

        subdistricts.forEach(s => {{
          const opt = document.createElement('option');
          opt.value = s;
          opt.textContent = `ต.${{s}}`;
          subSelect.appendChild(opt);
        }});
      }}
      selectedSubdistrict = 'all';
      selectDistrictOnBothMaps(selectedDistrict);
    }}

    function onSubdistrictChange() {{
      selectedSubdistrict = document.getElementById('subdistrictSelect').value;
      renderVillageDots();
      zoomToSubdistrict(selectedSubdistrict);
    }}

    function onPillarChange() {{
      selectedPillar = document.getElementById('pillarSelect').value;
      const pillarTitles = {{
        all: '1. แผนที่ระดับความเสี่ยง (2,200 หมู่บ้าน)',
        p1: '1. ความเสี่ยง ด1: น้ำอุปโภคบริโภค',
        p2: '1. ความเสี่ยง ด2: น้ำภาคการผลิต (เกษตร)',
        p3: '1. ความเสี่ยง ด3: น้ำท่วมและอุทกภัย',
        p4: '1. ความเสี่ยง ด4: คุณภาพน้ำและการอนุรักษ์',
        p5: '1. ความเสี่ยง ด5: ฟื้นฟูป่าต้นน้ำดินพังทลาย'
      }};
      document.getElementById('risk-map-title').textContent = pillarTitles[selectedPillar];
      updatePolygonColors();
      renderVillageDots();
    }}

    function onFilterUpdate() {{
      selectedRiskLevel = document.getElementById('riskLevelSelect').value;
      renderVillageDots();
    }}

    function onSearchInput() {{
      const query = document.getElementById('searchInput').value.trim().toLowerCase();
      if (!query) {{
        renderVillageDots();
        return;
      }}

      // Check if search matches district
      const matchedDist = DISTRICTS_DATA.features.find(f => (f.properties.amp_th || '').toLowerCase().includes(query));
      if (matchedDist) {{
        document.getElementById('districtSelect').value = matchedDist.properties.amp_th;
        onDistrictChange();
        return;
      }}

      renderVillageDots();
    }}

    function getDistrictRiskColor(p) {{
      let count = p.high_risk_total || 0;
      if (selectedPillar === 'p1') count = p.high_p1 || 0;
      else if (selectedPillar === 'p2') count = p.high_p2 || 0;
      else if (selectedPillar === 'p3') count = p.high_p3 || 0;
      else if (selectedPillar === 'p4') count = p.high_p4 || 0;
      else if (selectedPillar === 'p5') count = p.high_p5 || 0;

      if (count >= 70) return '#b71c1c';
      if (count >= 40) return '#e53935';
      if (count >= 20) return '#fb8c00';
      if (count >= 10) return '#fdd835';
      return '#43a047';
    }}

    function getDistrictBudgetColor(p) {{
      let b = p.total_budget || 0;
      if (selectedPillar === 'p1') b = p.budget_p1 || 0;
      else if (selectedPillar === 'p2') b = p.budget_p2 || 0;
      else if (selectedPillar === 'p3') b = p.budget_p3 || 0;
      else if (selectedPillar === 'p4') b = p.budget_p4 || 0;
      else if (selectedPillar === 'p5') b = p.budget_p5 || 0;

      if (b >= 3000) return '#0d47a1';
      if (b >= 1500) return '#1976d2';
      if (b >= 800) return '#42a5f5';
      if (b >= 400) return '#90caf9';
      return '#e3f2fd';
    }}

    function renderAllLayers() {{
      districtLayersRisk = {{}};
      districtLayersBudget = {{}};

      // Left Map District Layers
      const distGroupRisk = L.geoJSON(DISTRICTS_DATA, {{
        style: (feat) => ({{
          fillColor: getDistrictRiskColor(feat.properties),
          weight: 1.5,
          opacity: 0.9,
          color: '#ffffff',
          fillOpacity: 0.65
        }}),
        onEachFeature: (feat, layer) => {{
          const p = feat.properties;
          const name = p.amp_th || p.d_name;
          districtLayersRisk[name] = layer;

          layer.bindTooltip(`<div class="district-pill">${{name}}</div>`, {{ permanent: false, direction: 'center' }});

          layer.on('click', (e) => {{
            L.DomEvent.stopPropagation(e);
            selectDistrictOnBothMaps(name);
          }});

          layer.on('mouseover', () => highlightDistrictHover(name, true));
          layer.on('mouseout', () => highlightDistrictHover(name, false));
        }}
      }}).addTo(mapRisk);

      cmBounds = distGroupRisk.getBounds();

      // Right Map District Layers
      L.geoJSON(DISTRICTS_DATA, {{
        style: (feat) => ({{
          fillColor: getDistrictBudgetColor(feat.properties),
          weight: 1.5,
          opacity: 0.9,
          color: '#ffffff',
          fillOpacity: 0.68
        }}),
        onEachFeature: (feat, layer) => {{
          const p = feat.properties;
          const name = p.amp_th || p.d_name;
          districtLayersBudget[name] = layer;

          layer.bindTooltip(`<div class="district-pill" style="border-color:#0d47a1; color:#0d47a1;">${{name}}</div>`, {{ permanent: false, direction: 'center' }});

          layer.on('click', (e) => {{
            L.DomEvent.stopPropagation(e);
            selectDistrictOnBothMaps(name);
          }});

          layer.on('mouseover', () => highlightDistrictHover(name, true));
          layer.on('mouseout', () => highlightDistrictHover(name, false));
        }}
      }}).addTo(mapBudget);

      renderVillageDots();
    }}

    function updatePolygonColors() {{
      for (const [name, layer] of Object.entries(districtLayersRisk)) {{
        const p = layer.feature.properties;
        layer.setStyle({{ fillColor: getDistrictRiskColor(p) }});
      }}
      for (const [name, layer] of Object.entries(districtLayersBudget)) {{
        const p = layer.feature.properties;
        layer.setStyle({{ fillColor: getDistrictBudgetColor(p) }});
      }}
    }}

    function highlightDistrictHover(name, isHover) {{
      if (selectedDistrict !== 'all' && selectedDistrict !== name) return;
      
      const layerL = districtLayersRisk[name];
      const layerR = districtLayersBudget[name];

      if (isHover) {{
        if (layerL) layerL.setStyle({{ weight: 3, color: '#1a73e8', fillOpacity: 0.85 }});
        if (layerR) layerR.setStyle({{ weight: 3, color: '#0d47a1', fillOpacity: 0.88 }});
      }} else {{
        if (layerL && selectedDistrict !== name) layerL.setStyle({{ weight: 1.5, color: '#ffffff', fillOpacity: 0.65 }});
        if (layerR && selectedDistrict !== name) layerR.setStyle({{ weight: 1.5, color: '#ffffff', fillOpacity: 0.68 }});
      }}
    }}

    function selectDistrictOnBothMaps(name) {{
      selectedDistrict = name;
      document.getElementById('districtSelect').value = name;

      // Reset all styles
      for (const [dName, layer] of Object.entries(districtLayersRisk)) {{
        const isTarget = (name === 'all' || dName === name);
        layer.setStyle({{
          weight: (dName === name) ? 3.5 : 1.2,
          color: (dName === name) ? '#1a73e8' : '#ffffff',
          fillOpacity: isTarget ? 0.75 : 0.2
        }});
      }}

      for (const [dName, layer] of Object.entries(districtLayersBudget)) {{
        const isTarget = (name === 'all' || dName === name);
        layer.setStyle({{
          weight: (dName === name) ? 3.5 : 1.2,
          color: (dName === name) ? '#0d47a1' : '#ffffff',
          fillOpacity: isTarget ? 0.78 : 0.2
        }});
      }}

      if (name !== 'all' && districtLayersRisk[name]) {{
        const targetLayer = districtLayersRisk[name];
        const bounds = targetLayer.getBounds();
        
        isSyncing = true;
        mapRisk.fitBounds(bounds, {{ padding: [30, 30], animate: true }});
        mapBudget.fitBounds(bounds, {{ padding: [30, 30], animate: true }});
        isSyncing = false;

        showDistrictDetails(targetLayer.feature.properties);
      }} else {{
        resetToOverview();
      }}

      renderVillageDots();
    }}

    function zoomToSubdistrict(tamName) {{
      if (tamName === 'all') {{
        if (selectedDistrict !== 'all' && districtLayersRisk[selectedDistrict]) {{
          const bounds = districtLayersRisk[selectedDistrict].getBounds();
          mapRisk.fitBounds(bounds, {{ padding: [20, 20] }});
          mapBudget.fitBounds(bounds, {{ padding: [20, 20] }});
        }}
        return;
      }}

      const subFeats = SUBDISTRICTS_DATA.features.filter(f => (f.properties.tam_th === tamName || f.properties.tam_en === tamName));
      if (subFeats.length > 0) {{
        const group = L.geoJSON(subFeats[0]);
        const bounds = group.getBounds();
        isSyncing = true;
        mapRisk.fitBounds(bounds, {{ padding: [30, 30] }});
        mapBudget.fitBounds(bounds, {{ padding: [30, 30] }});
        isSyncing = false;
      }}
    }}

    function renderVillageDots() {{
      if (villagePointsLayer) mapRisk.removeLayer(villagePointsLayer);
      if (!showVillages) return;

      const query = document.getElementById('searchInput').value.trim().toLowerCase();

      const filtered = VILLAGES_DATA.features.filter(f => {{
        const p = f.properties;
        if (selectedDistrict !== 'all' && p.district !== selectedDistrict) return false;
        if (selectedSubdistrict !== 'all' && p.subdistrict !== selectedSubdistrict) return false;

        // Pillar & Risk Level Filter
        if (selectedPillar !== 'all' && selectedRiskLevel !== 'all') {{
          const pText = p[`${{selectedPillar}}_text`];
          if (pText !== selectedRiskLevel) return false;
        }} else if (selectedRiskLevel !== 'all') {{
          if (!p.priority.includes(selectedRiskLevel) && p.p3_text !== selectedRiskLevel) return false;
        }}

        // Search query
        if (query) {{
          const full = `${{p.village}} ${{p.subdistrict}} ${{p.district}}`.toLowerCase();
          if (!full.includes(query)) return false;
        }}

        return true;
      }});

      const markers = filtered.map(f => {{
        const p = f.properties;
        const [lng, lat] = f.geometry.coordinates;

        // Village Point Color
        let dotColor = '#1e8e3e';
        if (p.priority.includes('วิกฤติ')) dotColor = '#d93025';
        else if (p.priority.includes('เฝ้าระวังสูง')) dotColor = '#e37400';
        else if (p.priority.includes('เฝ้าระวังปานกลาง')) dotColor = '#f9ab00';

        const marker = L.circleMarker([lat, lng], {{
          radius: 5,
          fillColor: dotColor,
          color: '#ffffff',
          weight: 1.2,
          opacity: 1,
          fillOpacity: 0.95
        }});

        marker.on('click', (e) => {{
          L.DomEvent.stopPropagation(e);
          showVillageDetails(p);
        }});

        marker.bindTooltip(`<b>${{p.village}}</b> (ต.${{p.subdistrict}} อ.${{p.district}})`, {{
          direction: 'top',
          offset: [0, -5]
        }});

        return marker;
      }});

      villagePointsLayer = L.featureGroup(markers).addTo(mapRisk);
    }}

    function toggleVillagePoints() {{
      showVillages = !showVillages;
      const btn = document.getElementById('btn-toggle-villages');
      if (showVillages) {{
        btn.classList.add('active');
        renderVillageDots();
      }} else {{
        btn.classList.remove('active');
        if (villagePointsLayer) mapRisk.removeLayer(villagePointsLayer);
      }}
    }}

    function resetToOverview() {{
      document.getElementById('searchInput').value = '';
      document.getElementById('districtSelect').value = 'all';
      document.getElementById('subdistrictSelect').innerHTML = '<option value="all">🏘️ ทุกตำบล (194 ตำบล)</option>';
      document.getElementById('pillarSelect').value = 'all';
      document.getElementById('riskLevelSelect').value = 'all';
      selectedDistrict = 'all';
      selectedSubdistrict = 'all';
      selectedPillar = 'all';
      selectedRiskLevel = 'all';

      updatePolygonColors();

      for (const [name, layer] of Object.entries(districtLayersRisk)) {{
        layer.setStyle({{ weight: 1.5, color: '#ffffff', fillOpacity: 0.65 }});
      }}
      for (const [name, layer] of Object.entries(districtLayersBudget)) {{
        layer.setStyle({{ weight: 1.5, color: '#ffffff', fillOpacity: 0.68 }});
      }}

      renderVillageDots();

      if (cmBounds) {{
        isSyncing = true;
        mapRisk.fitBounds(cmBounds.pad(0.04));
        mapBudget.fitBounds(cmBounds.pad(0.04));
        isSyncing = false;
      }} else {{
        mapRisk.setView([18.7883, 98.9853], 9);
      }}
      closePanel();
    }}

    function showDistrictDetails(p) {{
      const panel = document.getElementById('infoPanel');
      const ampName = p.amp_th || p.d_name || 'อำเภอ';
      document.getElementById('panelTitle').innerHTML = `🏛️ อำเภอ${{ampName}}`;

      const budget = (p.total_budget || 0).toLocaleString('th-TH', {{ minimumFractionDigits: 1 }});
      const highRisk = p.high_risk_total || 0;

      document.getElementById('panelBody').innerHTML = `
        <div style="font-size:0.9rem; margin-bottom:14px;">
          <div style="color:#5f6368;">สถานะจัดสรรงบประมาณ:</div>
          <div style="font-weight:700; margin-top:2px;">${{p.gap_status || 'ปกติ'}}</div>
        </div>

        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; background:#f8f9fa; padding:12px; border-radius:12px; margin-bottom:14px;">
          <div>
            <div style="font-size:0.75rem; color:#5f6368;">งบประมาณรวม</div>
            <div style="font-size:1.1rem; font-weight:700; color:#1a73e8;">${{budget}} ลบ.</div>
          </div>
          <div>
            <div style="font-size:0.75rem; color:#5f6368;">โครงการทั้งหมด</div>
            <div style="font-size:1.1rem; font-weight:700; color:#202124;">${{p.total_projects || 0}} โครงการ</div>
          </div>
          <div>
            <div style="font-size:0.75rem; color:#5f6368;">จุดเสี่ยงสูง</div>
            <div style="font-size:1.1rem; font-weight:700; color:#d93025;">${{highRisk}} จุด</div>
          </div>
          <div>
            <div style="font-size:0.75rem; color:#5f6368;">หมู่บ้านทั้งหมด</div>
            <div style="font-size:1.1rem; font-weight:700; color:#202124;">${{p.villages || 0}} หมู่บ้าน</div>
          </div>
        </div>

        <div style="border-top:1px solid #e8eaed; padding-top:10px;">
          <div style="font-weight:700; font-size:0.82rem; margin-bottom:8px;">สรุปงบประมาณและจุดเสี่ยง 5 มิติ:</div>
          <div style="display:flex; justify-content:space-between; font-size:0.78rem; margin-bottom:4px;">
            <span>💧 ด1: น้ำอุปโภคบริโภค</span>
            <strong>${{(p.budget_p1 || 0).toFixed(1)}} ลบ. (${{p.high_p1 || 0}} เสี่ยงสูง)</strong>
          </div>
          <div style="display:flex; justify-content:space-between; font-size:0.78rem; margin-bottom:4px;">
            <span>🌾 ด2: น้ำภาคการผลิต (เกษตร)</span>
            <strong>${{(p.budget_p2 || 0).toFixed(1)}} ลบ. (${{p.high_p2 || 0}} เสี่ยงสูง)</strong>
          </div>
          <div style="display:flex; justify-content:space-between; font-size:0.78rem; margin-bottom:4px;">
            <span>🌊 ด3: น้ำท่วมและอุทกภัย</span>
            <strong>${{(p.budget_p3 || 0).toFixed(1)}} ลบ. (${{p.high_p3 || 0}} เสี่ยงสูง)</strong>
          </div>
          <div style="display:flex; justify-content:space-between; font-size:0.78rem; margin-bottom:4px;">
            <span>🧪 ด4: คุณภาพน้ำและอนุรักษ์</span>
            <strong>${{(p.budget_p4 || 0).toFixed(1)}} ลบ. (${{p.high_p4 || 0}} เสี่ยงสูง)</strong>
          </div>
          <div style="display:flex; justify-content:space-between; font-size:0.78rem;">
            <span>🌲 ด5: ฟื้นฟูป่าต้นน้ำ</span>
            <strong>${{(p.budget_p5 || 0).toFixed(1)}} ลบ. (${{p.high_p5 || 0}} เสี่ยงสูง)</strong>
          </div>
        </div>
      `;
      panel.style.display = 'flex';
    }}

    function showVillageDetails(p) {{
      const panel = document.getElementById('infoPanel');
      document.getElementById('panelTitle').innerHTML = `📍 ${{p.village}}`;

      const getBadge = (text, score) => {{
        if (score === 3) return `<span style="background:#fce8e6; color:#d93025; padding:2px 8px; border-radius:10px; font-weight:600; font-size:0.75rem;">เสี่ยงสูง (3)</span>`;
        if (score === 2) return `<span style="background:#fef7e0; color:#b06000; padding:2px 8px; border-radius:10px; font-weight:600; font-size:0.75rem;">ปานกลาง (2)</span>`;
        return `<span style="background:#e6f4ea; color:#137333; padding:2px 8px; border-radius:10px; font-weight:600; font-size:0.75rem;">เสี่ยงน้อย (1)</span>`;
      }};

      document.getElementById('panelBody').innerHTML = `
        <div style="margin-bottom:12px; font-size:0.9rem;">
          <div style="color:#5f6368;">ตำแหน่ง: <strong>ต.${{p.subdistrict}} อ.${{p.district}}</strong></div>
          <div style="margin-top:4px;">ระดับความสำคัญ: <strong>${{p.priority}}</strong></div>
          <div style="margin-top:4px;">คะแนนความเสี่ยงรวม: <strong style="color:#1a73e8; font-size:1.1rem;">${{p.total_score}} / 15</strong></div>
        </div>

        <div style="border-top:1px solid #e8eaed; padding-top:10px;">
          <div style="font-weight:700; font-size:0.82rem; margin-bottom:8px;">คะแนนความเสี่ยง 5 มิติ:</div>
          <div style="display:flex; justify-content:space-between; font-size:0.8rem; margin-bottom:6px;">
            <span>💧 ด1: น้ำอุปโภคบริโภค</span>
            ${{getBadge(p.p1_text, p.p1_score)}}
          </div>
          <div style="display:flex; justify-content:space-between; font-size:0.8rem; margin-bottom:6px;">
            <span>🌾 ด2: น้ำภาคการผลิต (เกษตร)</span>
            ${{getBadge(p.p2_text, p.p2_score)}}
          </div>
          <div style="display:flex; justify-content:space-between; font-size:0.8rem; margin-bottom:6px;">
            <span>🌊 ด3: น้ำท่วมและอุทกภัย</span>
            ${{getBadge(p.p3_text, p.p3_score)}}
          </div>
          <div style="display:flex; justify-content:space-between; font-size:0.8rem; margin-bottom:6px;">
            <span>🧪 ด4: คุณภาพน้ำและอนุรักษ์</span>
            ${{getBadge(p.p4_text, p.p4_score)}}
          </div>
          <div style="display:flex; justify-content:space-between; font-size:0.8rem;">
            <span>🌲 ด5: ฟื้นฟูป่าต้นน้ำ</span>
            ${{getBadge(p.p5_text, p.p5_score)}}
          </div>
        </div>
      `;
      panel.style.display = 'flex';
    }}

    function closePanel() {{
      document.getElementById('infoPanel').style.display = 'none';
    }}
  </script>
</body>
</html>
"""

with open('ChiangMai_Water_GIS_Dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Dual Sync GIS updated with organic polygon highlights and dual map clicks!")
