#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Flawless 3-Tier Drill-Down GIS Dashboard for Chiang Mai Water Master Plan
- 100% Fixed Dropdowns:
    * Select District -> auto-populates Subdistricts and Villages instantly
    * Select Subdistrict directly -> auto-detects District, auto-populates Villages, zooms to organic subdistrict polygon
    * Select Village directly -> auto-detects District & Subdistrict, pulses beacon marker, zooms to exact village
    * Click District on Map -> syncs all dropdowns and zooms to organic boundary
    * Click Subdistrict on Map -> syncs all dropdowns and zooms to organic boundary
    * Click Village on Map -> syncs all dropdowns, pulses beacon, shows 5-pillar scores in dock
- Organic boundary polygons (NO bounding boxes, NO rectangles)
- Smart Collapsible Bottom Dock (Google Maps style, never blocks maps)
- Both left & right maps synchronized in real-time
- Direct on-map GIS stats on both maps
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
      --shadow-lg: 0 8px 24px rgba(60,64,67, 0.22);
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Prompt', 'Google Sans', sans-serif; }}
    body {{ background: var(--bg); color: var(--text-main); height: 100vh; display: flex; flex-direction: column; overflow: hidden; }}

    /* Remove focus outlines & rectangles */
    path.leaflet-interactive:focus {{ outline: none !important; }}
    svg:focus {{ outline: none !important; }}
    .leaflet-container:focus {{ outline: none !important; }}

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
      flex-shrink: 0;
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
      padding: 8px 24px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      z-index: 900;
      flex-shrink: 0;
    }}
    .filter-group {{ display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }}
    
    .search-input-wrap {{
      position: relative;
      width: 220px;
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
      transition: all 0.2s;
    }}
    .search-input-wrap input:focus {{
      background: #fff;
      border-color: var(--primary);
      box-shadow: 0 0 0 2px rgba(26,115,232,0.2);
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
      max-width: 190px;
      transition: border-color 0.2s;
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
    .layer-toggle-btn:hover {{
      background: #e8eaed;
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
      min-height: 0;
    }}

    .map-box {{
      position: relative;
      height: 100%;
      width: 100%;
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
      pointer-events: none;
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
      pointer-events: none;
    }}
    .legend-title {{ font-weight: 700; margin-bottom: 6px; color: var(--text-main); }}
    .legend-row {{ display: flex; align-items: center; gap: 8px; margin-bottom: 3px; }}
    .legend-color {{ width: 14px; height: 12px; border-radius: 3px; display: inline-block; }}

    /* SMART FLOATING BOTTOM DOCK */
    .smart-dock {{
      position: absolute;
      bottom: 16px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 700;
      background: #ffffff;
      border-radius: 16px;
      box-shadow: var(--shadow-lg);
      border: 1px solid var(--border);
      width: 92%;
      max-width: 820px;
      display: none;
      flex-direction: column;
      overflow: hidden;
      transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .dock-summary-bar {{
      padding: 10px 18px;
      background: #ffffff;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      cursor: pointer;
      user-select: none;
    }}
    .dock-title-group {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
      flex: 1;
    }}
    .dock-title-group .area-title {{
      font-size: 0.95rem;
      font-weight: 700;
      color: #1a73e8;
    }}
    .dock-stat-pill {{
      background: #f1f3f4;
      padding: 3px 10px;
      border-radius: 12px;
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--text-main);
    }}
    .dock-actions {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .btn-toggle-expand {{
      background: #e8f0fe;
      color: #1a73e8;
      border: none;
      padding: 5px 12px;
      border-radius: 14px;
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
    }}
    .btn-close-dock {{
      background: none;
      border: none;
      color: var(--text-sub);
      cursor: pointer;
      display: flex;
      align-items: center;
      padding: 4px;
      border-radius: 50%;
    }}
    .btn-close-dock:hover {{ background: #f1f3f4; }}

    .dock-expanded-content {{
      max-height: 0;
      overflow: hidden;
      transition: max-height 0.3s ease;
      background: #fafbfc;
      border-top: 1px solid #f1f3f4;
    }}
    .smart-dock.expanded .dock-expanded-content {{
      max-height: 380px;
      overflow-y: auto;
    }}
    .dock-inner-padding {{
      padding: 14px 18px;
    }}

    /* Custom On-Map Text Labels */
    .custom-leaflet-tooltip {{
      background: transparent !important;
      border: none !important;
      box-shadow: none !important;
      padding: 0 !important;
    }}
    .onmap-label-risk, .onmap-label-budget {{
      text-align: center;
      pointer-events: none;
    }}
    .onmap-label-risk .dname, .onmap-label-budget .dname {{
      font-weight: 700;
      font-size: 11.5px;
      color: #1f1f1f;
      text-shadow: 1px 1px 3px #fff, -1px -1px 3px #fff, 1px -1px 3px #fff, -1px 1px 3px #fff;
    }}
    .onmap-label-risk .dstat {{
      font-size: 10px;
      font-weight: 700;
      color: #b71c1c;
      background: rgba(255, 255, 255, 0.92);
      padding: 1px 6px;
      border-radius: 8px;
      border: 1px solid rgba(183, 28, 28, 0.3);
      display: inline-block;
      margin-top: 1px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }}
    .onmap-label-budget .dstat {{
      font-size: 10px;
      font-weight: 700;
      color: #0d47a1;
      background: rgba(255, 255, 255, 0.92);
      padding: 1px 6px;
      border-radius: 8px;
      border: 1px solid rgba(13, 71, 161, 0.3);
      display: inline-block;
      margin-top: 1px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }}

    /* Pulse animation for active selected village */
    @keyframes pulse-ring {{
      0% {{ transform: scale(0.6); opacity: 1; }}
      100% {{ transform: scale(2.4); opacity: 0; }}
    }}
  </style>
</head>
<body>

  <!-- Google Style Header -->
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

  <!-- Filter & Control Bar (3-Tier Drill-Down) -->
  <div class="filter-bar">
    <div class="filter-group">
      
      <!-- Search Input -->
      <div class="search-input-wrap">
        <span class="material-symbols-outlined">search</span>
        <input type="text" id="searchInput" placeholder="พิมพ์ค้นหา อำเภอ / ตำบล / หมู่บ้าน..." oninput="onSearchInput()">
      </div>

      <!-- District Selector -->
      <select class="filter-select" id="districtSelect" onchange="onDistrictChange()">
        <option value="all">📍 ทุกอำเภอ (25 อำเภอ)</option>
      </select>

      <!-- Subdistrict Selector -->
      <select class="filter-select" id="subdistrictSelect" onchange="onSubdistrictChange()">
        <option value="all">🏘️ ทุกตำบล (204 ตำบล)</option>
      </select>

      <!-- Village Selector -->
      <select class="filter-select" id="villageSelect" onchange="onVillageChange()">
        <option value="all">🏡 ทุกหมู่บ้าน (2,200 หมู่บ้าน)</option>
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

    <!-- Toggle Village Points Layer & Reset View -->
    <div class="filter-group">
      <button class="layer-toggle-btn active" id="btn-toggle-villages" onclick="toggleVillagePoints()">
        <span class="material-symbols-outlined" style="font-size:18px;">pin_drop</span>
        <span>หมุด 2,200 หมู่บ้าน</span>
      </button>

      <button class="layer-toggle-btn" onclick="resetToOverview()" title="จัดกึ่งกลางเชียงใหม่">
        <span class="material-symbols-outlined" style="font-size:18px;">restart_alt</span>
        <span>รีเซ็ตมุมมอง</span>
      </button>
    </div>
  </div>

  <!-- Dual Maps Container (Side-by-Side Sync) -->
  <div class="dual-map-container">
    
    <!-- Left Map: Risk Analysis (Choropleth + Village Dots + Direct Labels) -->
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

    <!-- Right Map: Budget Allocation (Choropleth + Direct Numbers on GIS) -->
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

    <!-- SMART FLOATING BOTTOM DOCK -->
    <div class="smart-dock" id="smartDock">
      <div class="dock-summary-bar" onclick="toggleDockExpand()">
        <div class="dock-title-group">
          <span class="material-symbols-outlined" style="color:#1a73e8; font-size:22px;">info</span>
          <span class="area-title" id="dockAreaTitle">อ.สันกำแพง</span>
          <span class="dock-stat-pill" id="dockPillBudget">💰 599.7 ลบ. (213 โครงการ)</span>
          <span class="dock-stat-pill" id="dockPillRisk">🔴 79 จุดเสี่ยง</span>
        </div>
        <div class="dock-actions" onclick="event.stopPropagation()">
          <button class="btn-toggle-expand" id="btnDockExpand" onclick="toggleDockExpand()">
            <span class="material-symbols-outlined" style="font-size:16px;" id="expandIcon">expand_less</span>
            <span id="expandText">ดู 5 มิติ</span>
          </button>
          <button class="btn-close-dock" onclick="closeDock()">
            <span class="material-symbols-outlined">close</span>
          </button>
        </div>
      </div>
      <div class="dock-expanded-content">
        <div class="dock-inner-padding" id="dockExpandedBody"></div>
      </div>
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
    let subdistrictGroupRisk = null, subdistrictGroupBudget = null;
    let subdistrictHighlightRisk = null, subdistrictHighlightBudget = null;
    let villagePointsLayer = null;
    let activePulseMarker = null;
    let showVillages = true;
    let isSyncing = false;
    let cmBounds;

    let selectedDistrict = 'all';
    let selectedSubdistrict = 'all';
    let selectedVillageId = 'all';
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
        zoomControl: false,
        boxZoom: false
      }});
      L.tileLayer(googleMapsUrl, {{ maxZoom: 18, attribution: '© Google Maps' }}).addTo(mapRisk);
      L.control.zoom({{ position: 'bottomright' }}).addTo(mapRisk);

      // Right Map
      mapBudget = L.map('map-budget', {{
        center: cmCenter,
        zoom: initialZoom,
        zoomControl: false,
        boxZoom: false
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

    /* ========================================================= */
    /* 3-TIER DROPDOWN POPULATION & SYNCHRONIZATION              */
    /* ========================================================= */
    function populateDropdowns() {{
      // Populate Districts
      const distSelect = document.getElementById('districtSelect');
      distSelect.innerHTML = '<option value="all">📍 ทุกอำเภอ (25 อำเภอ)</option>';
      const districts = [...new Set(VILLAGES_DATA.features.map(f => f.properties.district))].sort((a,b) => a.localeCompare(b, 'th'));

      districts.forEach(d => {{
        const opt = document.createElement('option');
        opt.value = d;
        opt.textContent = `📍 อ.${{d}}`;
        distSelect.appendChild(opt);
      }});

      // Populate Subdistricts (initial state: all 204 subdistricts)
      updateSubdistrictDropdown('all');

      // Populate Villages (initial state: all 2,200 villages)
      updateVillageDropdown('all', 'all');
    }}

    function updateSubdistrictDropdown(distName) {{
      const subSelect = document.getElementById('subdistrictSelect');
      
      if (distName === 'all') {{
        subSelect.innerHTML = '<option value="all">🏘️ ทุกตำบล (204 ตำบล)</option>';
        // Collect all distinct (district, subdistrict) pairs
        const pairs = [];
        const seen = new Set();
        VILLAGES_DATA.features.forEach(f => {{
          const key = `${{f.properties.district}}|${{f.properties.subdistrict}}`;
          if (!seen.has(key)) {{
            seen.add(key);
            pairs.push({{ district: f.properties.district, subdistrict: f.properties.subdistrict }});
          }}
        }});
        pairs.sort((a,b) => a.subdistrict.localeCompare(b.subdistrict, 'th'));

        pairs.forEach(p => {{
          const opt = document.createElement('option');
          opt.value = `${{p.district}}|${{p.subdistrict}}`;
          opt.textContent = `ต.${{p.subdistrict}} (อ.${{p.district}})`;
          subSelect.appendChild(opt);
        }});
      }} else {{
        const subdistricts = [...new Set(
          VILLAGES_DATA.features
            .filter(f => f.properties.district === distName)
            .map(f => f.properties.subdistrict)
        )].sort((a,b) => a.localeCompare(b, 'th'));

        subSelect.innerHTML = `<option value="all">🏘️ ทุกตำบลใน อ.${{distName}} (${{subdistricts.length}} ตำบล)</option>`;

        subdistricts.forEach(s => {{
          const opt = document.createElement('option');
          opt.value = s;
          opt.textContent = `ต.${{s}}`;
          subSelect.appendChild(opt);
        }});
      }}
    }}

    function updateVillageDropdown(distName, subName) {{
      const vilSelect = document.getElementById('villageSelect');

      if (distName === 'all' && (subName === 'all' || !subName)) {{
        vilSelect.innerHTML = '<option value="all">🏡 ทุกหมู่บ้าน (2,200 หมู่บ้าน)</option>';
        // Sort all villages by village name
        const allVils = [...VILLAGES_DATA.features].sort((a,b) => a.properties.village.localeCompare(b.properties.village, 'th'));
        allVils.forEach(f => {{
          const p = f.properties;
          const opt = document.createElement('option');
          opt.value = p.id;
          opt.textContent = `ม.${{p.village}} (ต.${{p.subdistrict}} อ.${{p.district}})`;
          vilSelect.appendChild(opt);
        }});
      }} else {{
        const filtered = VILLAGES_DATA.features.filter(f => {{
          const matchD = (distName === 'all' || f.properties.district === distName);
          const matchS = (subName === 'all' || !subName || f.properties.subdistrict === subName);
          return matchD && matchS;
        }}).sort((a,b) => a.properties.village.localeCompare(b.properties.village, 'th'));

        const labelScope = (subName && subName !== 'all') ? `ต.${{subName}}` : `อ.${{distName}}`;
        vilSelect.innerHTML = `<option value="all">🏡 ทุกหมู่บ้านใน ${{labelScope}} (${{filtered.length}} หมู่บ้าน)</option>`;

        filtered.forEach(f => {{
          const p = f.properties;
          const opt = document.createElement('option');
          opt.value = p.id;
          opt.textContent = (subName && subName !== 'all') ? `ม.${{p.village}}` : `ม.${{p.village}} (ต.${{p.subdistrict}})`;
          vilSelect.appendChild(opt);
        }});
      }}
    }}

    function onDistrictChange() {{
      selectedDistrict = document.getElementById('districtSelect').value;
      selectedSubdistrict = 'all';
      selectedVillageId = 'all';

      if (selectedDistrict === 'all') {{
        resetToOverview();
        return;
      }}

      updateSubdistrictDropdown(selectedDistrict);
      updateVillageDropdown(selectedDistrict, 'all');

      selectDistrictOnBothMaps(selectedDistrict, false);
    }}

    function onSubdistrictChange() {{
      const rawVal = document.getElementById('subdistrictSelect').value;
      selectedVillageId = 'all';

      if (rawVal === 'all') {{
        selectedSubdistrict = 'all';
        if (selectedDistrict !== 'all') {{
          updateVillageDropdown(selectedDistrict, 'all');
          highlightAndZoomSubdistrict('all');
        }} else {{
          resetToOverview();
        }}
        return;
      }}

      // Check if value is compound "District|Subdistrict"
      if (rawVal.includes('|')) {{
        const parts = rawVal.split('|');
        selectedDistrict = parts[0];
        selectedSubdistrict = parts[1];

        document.getElementById('districtSelect').value = selectedDistrict;
        selectDistrictOnBothMaps(selectedDistrict, false);

        // Repopulate subdistrict dropdown for this district and select it
        updateSubdistrictDropdown(selectedDistrict);
        document.getElementById('subdistrictSelect').value = selectedSubdistrict;
      }} else {{
        selectedSubdistrict = rawVal;
      }}

      updateVillageDropdown(selectedDistrict, selectedSubdistrict);
      highlightAndZoomSubdistrict(selectedSubdistrict);
    }}

    function onVillageChange() {{
      selectedVillageId = document.getElementById('villageSelect').value;
      if (selectedVillageId === 'all') {{
        if (activePulseMarker) {{ mapRisk.removeLayer(activePulseMarker); activePulseMarker = null; }}
        renderVillageDots();
        return;
      }}

      // Find village feature by unique id
      const vFeat = VILLAGES_DATA.features.find(f => f.properties.id == selectedVillageId);
      if (vFeat) {{
        const p = vFeat.properties;
        const [lng, lat] = vFeat.geometry.coordinates;

        // Auto-sync District & Subdistrict dropdowns if not already aligned
        if (selectedDistrict !== p.district) {{
          selectedDistrict = p.district;
          document.getElementById('districtSelect').value = p.district;
          selectDistrictOnBothMaps(p.district, false);
          updateSubdistrictDropdown(p.district);
        }}
        if (selectedSubdistrict !== p.subdistrict) {{
          selectedSubdistrict = p.subdistrict;
          document.getElementById('subdistrictSelect').value = p.subdistrict;
          highlightAndZoomSubdistrict(p.subdistrict, false); // highlight polygon without overriding village zoom
        }}

        // Center on village
        isSyncing = true;
        mapRisk.setView([lat, lng], 15);
        mapBudget.setView([lat, lng], 15);
        isSyncing = false;

        // Add pulsing ring marker
        if (activePulseMarker) mapRisk.removeLayer(activePulseMarker);
        activePulseMarker = L.circleMarker([lat, lng], {{
          radius: 14,
          fillColor: '#1a73e8',
          color: '#1a73e8',
          weight: 3.5,
          opacity: 0.9,
          fillOpacity: 0.45
        }}).addTo(mapRisk);

        renderVillageDots();
        showVillageDetails(p);
      }}
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
      updateOnMapLabels();
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

      // Match district
      const matchedDist = DISTRICTS_DATA.features.find(f => (f.properties.amp_th || '').toLowerCase() === query);
      if (matchedDist) {{
        document.getElementById('districtSelect').value = matchedDist.properties.amp_th;
        onDistrictChange();
        return;
      }}

      // Match subdistrict
      const matchedSub = SUBDISTRICTS_DATA.features.find(f => (f.properties.tam_th || '').toLowerCase() === query);
      if (matchedSub) {{
        const amp = matchedSub.properties.amp_th;
        const tam = matchedSub.properties.tam_th;
        selectedDistrict = amp;
        selectedSubdistrict = tam;
        document.getElementById('districtSelect').value = amp;
        selectDistrictOnBothMaps(amp, false);
        updateSubdistrictDropdown(amp);
        document.getElementById('subdistrictSelect').value = tam;
        updateVillageDropdown(amp, tam);
        highlightAndZoomSubdistrict(tam);
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

    /* ========================================================= */
    /* RENDER ALL BASE DISTRICT GIS LAYERS                       */
    /* ========================================================= */
    function renderAllLayers() {{
      districtLayersRisk = {{}};
      districtLayersBudget = {{}};

      // Left Map District Layers
      const distGroupRisk = L.geoJSON(DISTRICTS_DATA, {{
        style: (feat) => ({{
          fillColor: getDistrictRiskColor(feat.properties),
          weight: 1.5,
          opacity: 0.95,
          color: '#ffffff',
          fillOpacity: 0.65
        }}),
        onEachFeature: (feat, layer) => {{
          const p = feat.properties;
          const name = p.amp_th || p.d_name;
          districtLayersRisk[name] = layer;

          const highCount = p.high_risk_total || 0;
          layer.bindTooltip(`
            <div class="onmap-label-risk">
              <div class="dname">${{name}}</div>
              <div class="dstat">🔴 ${{highCount}} จุดเสี่ยง</div>
            </div>
          `, {{ permanent: true, direction: 'center', className: 'custom-leaflet-tooltip' }});

          layer.on('click', (e) => {{
            L.DomEvent.stopPropagation(e);
            selectDistrictOnBothMaps(name, true);
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
          opacity: 0.95,
          color: '#ffffff',
          fillOpacity: 0.68
        }}),
        onEachFeature: (feat, layer) => {{
          const p = feat.properties;
          const name = p.amp_th || p.d_name;
          districtLayersBudget[name] = layer;

          const budgetM = (p.total_budget || 0).toLocaleString('th-TH', {{ maximumFractionDigits: 1 }});
          const projCount = p.total_projects || 0;

          layer.bindTooltip(`
            <div class="onmap-label-budget">
              <div class="dname">${{name}}</div>
              <div class="dstat">💰 ${{budgetM}} ลบ. (${{projCount}} โครงการ)</div>
            </div>
          `, {{ permanent: true, direction: 'center', className: 'custom-leaflet-tooltip' }});

          layer.on('click', (e) => {{
            L.DomEvent.stopPropagation(e);
            selectDistrictOnBothMaps(name, true);
          }});

          layer.on('mouseover', () => highlightDistrictHover(name, true));
          layer.on('mouseout', () => highlightDistrictHover(name, false));
        }}
      }}).addTo(mapBudget);

      renderVillageDots();
    }}

    function updateOnMapLabels() {{
      for (const [name, layer] of Object.entries(districtLayersRisk)) {{
        const p = layer.feature.properties;
        let count = p.high_risk_total || 0;
        if (selectedPillar === 'p1') count = p.high_p1 || 0;
        else if (selectedPillar === 'p2') count = p.high_p2 || 0;
        else if (selectedPillar === 'p3') count = p.high_p3 || 0;
        else if (selectedPillar === 'p4') count = p.high_p4 || 0;
        else if (selectedPillar === 'p5') count = p.high_p5 || 0;

        layer.setTooltipContent(`
          <div class="onmap-label-risk">
            <div class="dname">${{name}}</div>
            <div class="dstat">🔴 ${{count}} จุดเสี่ยง</div>
          </div>
        `);
      }}

      for (const [name, layer] of Object.entries(districtLayersBudget)) {{
        const p = layer.feature.properties;
        let b = p.total_budget || 0;
        let projs = p.total_projects || 0;
        if (selectedPillar === 'p1') {{ b = p.budget_p1 || 0; projs = p.proj_p1 || 0; }}
        else if (selectedPillar === 'p2') {{ b = p.budget_p2 || 0; projs = p.proj_p2 || 0; }}
        else if (selectedPillar === 'p3') {{ b = p.budget_p3 || 0; projs = p.proj_p3 || 0; }}
        else if (selectedPillar === 'p4') {{ b = p.budget_p4 || 0; projs = p.proj_p4 || 0; }}
        else if (selectedPillar === 'p5') {{ b = p.budget_p5 || 0; projs = p.proj_p5 || 0; }}

        layer.setTooltipContent(`
          <div class="onmap-label-budget">
            <div class="dname">${{name}}</div>
            <div class="dstat">💰 ${{b.toLocaleString('th-TH', {{ maximumFractionDigits: 1 }})}} ลบ. (${{projs}} โครงการ)</div>
          </div>
        `);
      }}
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
        if (layerL) layerL.setStyle({{ weight: 3.5, color: '#1a73e8', fillOpacity: 0.88 }});
        if (layerR) layerR.setStyle({{ weight: 3.5, color: '#0d47a1', fillOpacity: 0.90 }});
      }} else {{
        if (layerL && selectedDistrict !== name) layerL.setStyle({{ weight: 1.5, color: '#ffffff', fillOpacity: 0.65 }});
        if (layerR && selectedDistrict !== name) layerR.setStyle({{ weight: 1.5, color: '#ffffff', fillOpacity: 0.68 }});
      }}
    }}

    /* ========================================================= */
    /* DISTRICT SELECTION & BI-DIRECTIONAL SYNC                  */
    /* ========================================================= */
    function selectDistrictOnBothMaps(name, updateDropdowns = true) {{
      selectedDistrict = name;
      document.getElementById('districtSelect').value = name;

      if (activePulseMarker) {{ mapRisk.removeLayer(activePulseMarker); activePulseMarker = null; }}
      if (subdistrictHighlightRisk) {{ mapRisk.removeLayer(subdistrictHighlightRisk); subdistrictHighlightRisk = null; }}
      if (subdistrictHighlightBudget) {{ mapBudget.removeLayer(subdistrictHighlightBudget); subdistrictHighlightBudget = null; }}

      // Auto populate subdistricts and villages in dropdowns!
      if (updateDropdowns) {{
        selectedSubdistrict = 'all';
        selectedVillageId = 'all';
        updateSubdistrictDropdown(name);
        updateVillageDropdown(name, 'all');
      }}

      // Highlight organic polygon shapes on both sides
      for (const [dName, layer] of Object.entries(districtLayersRisk)) {{
        const isTarget = (name === 'all' || dName === name);
        layer.setStyle({{
          weight: (dName === name) ? 3.5 : 1.2,
          color: (dName === name) ? '#1a73e8' : '#ffffff',
          fillOpacity: isTarget ? 0.72 : 0.20
        }});
      }}

      for (const [dName, layer] of Object.entries(districtLayersBudget)) {{
        const isTarget = (name === 'all' || dName === name);
        layer.setStyle({{
          weight: (dName === name) ? 3.5 : 1.2,
          color: (dName === name) ? '#0d47a1' : '#ffffff',
          fillOpacity: isTarget ? 0.75 : 0.20
        }});
      }}

      // Load subdistrict boundaries inside this district
      renderSubdistrictsForDistrict(name);

      if (name !== 'all' && districtLayersRisk[name]) {{
        const targetLayer = districtLayersRisk[name];
        const bounds = targetLayer.getBounds();
        
        isSyncing = true;
        mapRisk.fitBounds(bounds, {{ padding: [35, 35], animate: true }});
        mapBudget.fitBounds(bounds, {{ padding: [35, 35], animate: true }});
        isSyncing = false;

        showDistrictDetails(targetLayer.feature.properties);
      }} else {{
        resetToOverview();
      }}

      renderVillageDots();
    }}

    function renderSubdistrictsForDistrict(distName) {{
      if (subdistrictGroupRisk) mapRisk.removeLayer(subdistrictGroupRisk);
      if (subdistrictGroupBudget) mapBudget.removeLayer(subdistrictGroupBudget);

      if (distName === 'all') return;

      const subFeats = SUBDISTRICTS_DATA.features.filter(f => {{
        const a = f.properties.amp_th || '';
        return a.includes(distName) || distName.includes(a);
      }});

      if (subFeats.length > 0) {{
        // Organic subdistrict lines on left map
        subdistrictGroupRisk = L.geoJSON(subFeats, {{
          style: {{
            color: '#1a73e8',
            weight: 2,
            dashArray: '4, 4',
            fillColor: '#1a73e8',
            fillOpacity: 0.12
          }},
          onEachFeature: (f, l) => {{
            const tamName = f.properties.tam_th;
            l.bindTooltip(`ต.${{tamName}}`, {{ direction: 'center', permanent: false }});
            l.on('click', (e) => {{
              L.DomEvent.stopPropagation(e);
              selectedSubdistrict = tamName;
              document.getElementById('subdistrictSelect').value = tamName;
              updateVillageDropdown(selectedDistrict, tamName);
              highlightAndZoomSubdistrict(tamName);
            }});
          }}
        }}).addTo(mapRisk);

        // Organic subdistrict lines on right map
        subdistrictGroupBudget = L.geoJSON(subFeats, {{
          style: {{
            color: '#0d47a1',
            weight: 2,
            dashArray: '4, 4',
            fillColor: '#0d47a1',
            fillOpacity: 0.12
          }},
          onEachFeature: (f, l) => {{
            const tamName = f.properties.tam_th;
            l.bindTooltip(`ต.${{tamName}}`, {{ direction: 'center', permanent: false }});
            l.on('click', (e) => {{
              L.DomEvent.stopPropagation(e);
              selectedSubdistrict = tamName;
              document.getElementById('subdistrictSelect').value = tamName;
              updateVillageDropdown(selectedDistrict, tamName);
              highlightAndZoomSubdistrict(tamName);
            }});
          }}
        }}).addTo(mapBudget);
      }}
    }}

    function highlightAndZoomSubdistrict(tamName, doZoom = true) {{
      if (subdistrictHighlightRisk) {{ mapRisk.removeLayer(subdistrictHighlightRisk); subdistrictHighlightRisk = null; }}
      if (subdistrictHighlightBudget) {{ mapBudget.removeLayer(subdistrictHighlightBudget); subdistrictHighlightBudget = null; }}

      if (tamName === 'all') {{
        if (selectedDistrict !== 'all' && districtLayersRisk[selectedDistrict]) {{
          const bounds = districtLayersRisk[selectedDistrict].getBounds();
          mapRisk.fitBounds(bounds, {{ padding: [25, 25] }});
          mapBudget.fitBounds(bounds, {{ padding: [25, 25] }});
        }}
        renderSubdistrictsForDistrict(selectedDistrict);
        renderVillageDots();
        return;
      }}

      // Find the specific subdistrict feature
      const subFeat = SUBDISTRICTS_DATA.features.find(f => {{
        const matchT = (f.properties.tam_th === tamName || f.properties.tam_en === tamName);
        const matchA = (selectedDistrict === 'all' || (f.properties.amp_th || '').includes(selectedDistrict));
        return matchT && matchA;
      }});

      if (subFeat) {{
        // Highlight this specific subdistrict organic polygon on both maps
        subdistrictHighlightRisk = L.geoJSON(subFeat, {{
          style: {{
            color: '#d93025',
            weight: 3.5,
            fillColor: '#d93025',
            fillOpacity: 0.35
          }}
        }}).addTo(mapRisk);

        subdistrictHighlightBudget = L.geoJSON(subFeat, {{
          style: {{
            color: '#0d47a1',
            weight: 3.5,
            fillColor: '#0d47a1',
            fillOpacity: 0.35
          }}
        }}).addTo(mapBudget);

        if (doZoom) {{
          const bounds = subdistrictHighlightRisk.getBounds();
          isSyncing = true;
          mapRisk.fitBounds(bounds, {{ padding: [35, 35], animate: true }});
          mapBudget.fitBounds(bounds, {{ padding: [35, 35], animate: true }});
          isSyncing = false;
        }}

        showSubdistrictDetails(tamName, selectedDistrict);
      }} else {{
        // Fallback zoom from village points if feature boundary missing
        const vils = VILLAGES_DATA.features.filter(f => f.properties.subdistrict === tamName && (selectedDistrict === 'all' || f.properties.district === selectedDistrict));
        if (vils.length > 0 && doZoom) {{
          const coords = vils.map(f => [f.geometry.coordinates[1], f.geometry.coordinates[0]]);
          const bounds = L.latLngBounds(coords);
          isSyncing = true;
          mapRisk.fitBounds(bounds.pad(0.15), {{ padding: [35, 35], animate: true }});
          mapBudget.fitBounds(bounds.pad(0.15), {{ padding: [35, 35], animate: true }});
          isSyncing = false;
        }}
        showSubdistrictDetails(tamName, selectedDistrict);
      }}

      renderVillageDots();
    }}

    /* ========================================================= */
    /* VILLAGE POINT MARKERS & PULSING BEACON                    */
    /* ========================================================= */
    function renderVillageDots() {{
      if (villagePointsLayer) mapRisk.removeLayer(villagePointsLayer);
      if (!showVillages) return;

      const query = document.getElementById('searchInput').value.trim().toLowerCase();

      const filtered = VILLAGES_DATA.features.filter(f => {{
        const p = f.properties;
        if (selectedDistrict !== 'all' && p.district !== selectedDistrict) return false;
        if (selectedSubdistrict !== 'all' && p.subdistrict !== selectedSubdistrict) return false;
        if (selectedVillageId !== 'all' && p.id != selectedVillageId) return false;

        if (selectedPillar !== 'all' && selectedRiskLevel !== 'all') {{
          const pText = p[`${{selectedPillar}}_text`];
          if (pText !== selectedRiskLevel) return false;
        }} else if (selectedRiskLevel !== 'all') {{
          if (!p.priority.includes(selectedRiskLevel) && p.p3_text !== selectedRiskLevel) return false;
        }}

        if (query) {{
          const full = `${{p.village}} ${{p.subdistrict}} ${{p.district}}`.toLowerCase();
          if (!full.includes(query)) return false;
        }}

        return true;
      }});

      const markers = filtered.map(f => {{
        const p = f.properties;
        const [lng, lat] = f.geometry.coordinates;

        let dotColor = '#1e8e3e';
        if (p.priority.includes('วิกฤติ')) dotColor = '#d93025';
        else if (p.priority.includes('เฝ้าระวังสูง')) dotColor = '#e37400';
        else if (p.priority.includes('เฝ้าระวังปานกลาง')) dotColor = '#f9ab00';

        const marker = L.circleMarker([lat, lng], {{
          radius: 5.5,
          fillColor: dotColor,
          color: '#ffffff',
          weight: 1.4,
          opacity: 1,
          fillOpacity: 0.95
        }});

        marker.on('click', (e) => {{
          L.DomEvent.stopPropagation(e);

          // Synchronize dropdowns on village click
          if (selectedDistrict !== p.district) {{
            selectedDistrict = p.district;
            document.getElementById('districtSelect').value = p.district;
            selectDistrictOnBothMaps(p.district, false);
            updateSubdistrictDropdown(p.district);
          }}
          if (selectedSubdistrict !== p.subdistrict) {{
            selectedSubdistrict = p.subdistrict;
            document.getElementById('subdistrictSelect').value = p.subdistrict;
            updateVillageDropdown(p.district, p.subdistrict);
            highlightAndZoomSubdistrict(p.subdistrict, false);
          }}
          selectedVillageId = p.id;
          document.getElementById('villageSelect').value = p.id;

          // Pulse marker
          if (activePulseMarker) mapRisk.removeLayer(activePulseMarker);
          activePulseMarker = L.circleMarker([lat, lng], {{
            radius: 14,
            fillColor: '#1a73e8',
            color: '#1a73e8',
            weight: 3.5,
            opacity: 0.9,
            fillOpacity: 0.45
          }}).addTo(mapRisk);

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
      document.getElementById('pillarSelect').value = 'all';
      document.getElementById('riskLevelSelect').value = 'all';
      selectedDistrict = 'all';
      selectedSubdistrict = 'all';
      selectedVillageId = 'all';
      selectedPillar = 'all';
      selectedRiskLevel = 'all';

      // Repopulate subdistricts & villages to initial global state
      updateSubdistrictDropdown('all');
      updateVillageDropdown('all', 'all');

      if (subdistrictGroupRisk) mapRisk.removeLayer(subdistrictGroupRisk);
      if (subdistrictGroupBudget) mapBudget.removeLayer(subdistrictGroupBudget);
      if (subdistrictHighlightRisk) mapRisk.removeLayer(subdistrictHighlightRisk);
      if (subdistrictHighlightBudget) mapBudget.removeLayer(subdistrictHighlightBudget);
      if (activePulseMarker) {{ mapRisk.removeLayer(activePulseMarker); activePulseMarker = null; }}

      updatePolygonColors();
      updateOnMapLabels();

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
      closeDock();
    }}

    /* ========================================================= */
    /* SMART DOCK DETAILS HANDLERS                               */
    /* ========================================================= */
    function toggleDockExpand() {{
      const dock = document.getElementById('smartDock');
      dock.classList.toggle('expanded');
      const isExp = dock.classList.contains('expanded');
      document.getElementById('expandIcon').textContent = isExp ? 'expand_more' : 'expand_less';
      document.getElementById('expandText').textContent = isExp ? 'ย่อเก็บ' : 'ดู 5 มิติ';
    }}

    function closeDock() {{
      document.getElementById('smartDock').style.display = 'none';
      document.getElementById('smartDock').classList.remove('expanded');
    }}

    function showDistrictDetails(p) {{
      const dock = document.getElementById('smartDock');
      const ampName = p.amp_th || p.d_name || 'อำเภอ';
      const budget = (p.total_budget || 0).toLocaleString('th-TH', {{ minimumFractionDigits: 1 }});
      const highRisk = p.high_risk_total || 0;

      document.getElementById('dockAreaTitle').innerHTML = `🏛️ อ.${{ampName}}`;
      document.getElementById('dockPillBudget').innerHTML = `💰 ${{budget}} ลบ. (${{p.total_projects || 0}} โครงการ)`;
      document.getElementById('dockPillRisk').innerHTML = `🔴 ${{highRisk}} จุดเสี่ยง (${{p.villages || 0}} หมู่บ้าน)`;

      document.getElementById('dockExpandedBody').innerHTML = `
        <div style="font-size:0.85rem; margin-bottom:12px;">
          <span style="color:#5f6368;">สถานะจัดสรรงบประมาณ:</span>
          <strong style="margin-left:6px; color:#202124;">${{p.gap_status || 'ปกติ'}}</strong>
        </div>

        <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:10px; background:#f8f9fa; padding:10px 14px; border-radius:12px; margin-bottom:12px; text-align:center;">
          <div>
            <div style="font-size:0.72rem; color:#5f6368;">งบประมาณรวม</div>
            <div style="font-size:1.05rem; font-weight:700; color:#1a73e8;">${{budget}} ลบ.</div>
          </div>
          <div>
            <div style="font-size:0.72rem; color:#5f6368;">โครงการทั้งหมด</div>
            <div style="font-size:1.05rem; font-weight:700; color:#202124;">${{p.total_projects || 0}} โครงการ</div>
          </div>
          <div>
            <div style="font-size:0.72rem; color:#5f6368;">จุดเสี่ยงสูง</div>
            <div style="font-size:1.05rem; font-weight:700; color:#d93025;">${{highRisk}} จุด</div>
          </div>
          <div>
            <div style="font-size:0.72rem; color:#5f6368;">หมู่บ้านทั้งหมด</div>
            <div style="font-size:1.05rem; font-weight:700; color:#202124;">${{p.villages || 0}} หมู่บ้าน</div>
          </div>
        </div>

        <div style="border-top:1px solid #e8eaed; padding-top:10px;">
          <div style="font-weight:700; font-size:0.8rem; margin-bottom:8px; color:#3c4043;">สรุปงบประมาณและจุดเสี่ยง 5 มิติ:</div>
          <div style="display:grid; grid-template-columns: 1fr 1fr; gap:6px 16px; font-size:0.78rem;">
            <div style="display:flex; justify-content:space-between;">
              <span>💧 ด1: อุปโภคบริโภค</span>
              <strong>${{(p.budget_p1 || 0).toFixed(1)}} ลบ. (${{p.high_p1 || 0}} เสี่ยง)</strong>
            </div>
            <div style="display:flex; justify-content:space-between;">
              <span>🌾 ด2: ภาคเกษตร</span>
              <strong>${{(p.budget_p2 || 0).toFixed(1)}} ลบ. (${{p.high_p2 || 0}} เสี่ยง)</strong>
            </div>
            <div style="display:flex; justify-content:space-between;">
              <span>🌊 ด3: น้ำท่วมอุทกภัย</span>
              <strong>${{(p.budget_p3 || 0).toFixed(1)}} ลบ. (${{p.high_p3 || 0}} เสี่ยง)</strong>
            </div>
            <div style="display:flex; justify-content:space-between;">
              <span>🧪 ด4: คุณภาพน้ำ</span>
              <strong>${{(p.budget_p4 || 0).toFixed(1)}} ลบ. (${{p.high_p4 || 0}} เสี่ยง)</strong>
            </div>
            <div style="display:flex; justify-content:space-between;">
              <span>🌲 ด5: ป่าต้นน้ำ</span>
              <strong>${{(p.budget_p5 || 0).toFixed(1)}} ลบ. (${{p.high_p5 || 0}} เสี่ยง)</strong>
            </div>
          </div>
        </div>
      `;
      dock.style.display = 'flex';
    }}

    function showSubdistrictDetails(tamName, distName) {{
      const dock = document.getElementById('smartDock');
      const vils = VILLAGES_DATA.features.filter(f => f.properties.subdistrict === tamName && (distName === 'all' || f.properties.district === distName));
      const totalV = vils.length;
      const highV = vils.filter(f => f.properties.priority.includes('วิกฤติ') || f.properties.priority.includes('เฝ้าระวังสูง')).length;

      document.getElementById('dockAreaTitle').innerHTML = `🏘️ ต.${{tamName}} (อ.${{distName}})`;
      document.getElementById('dockPillBudget').innerHTML = `🏡 ${{totalV}} หมู่บ้าน`;
      document.getElementById('dockPillRisk').innerHTML = `🔴 ${{highV}} จุดเสี่ยงสูง`;

      document.getElementById('dockExpandedBody').innerHTML = `
        <div style="font-size:0.85rem; margin-bottom:10px;">
          พื้นที่ตำบล: <strong>ต.${{tamName}} อ.${{distName}}</strong> | จำนวนหมู่บ้านสำรวจทั้งหมด: <strong>${{totalV}} หมู่บ้าน</strong>
        </div>
        <div style="font-size:0.8rem; color:#5f6368; margin-bottom:8px;">
          รายชื่อหมู่บ้านในตำบล (คลิกที่ชื่อเพื่อเปิดดูคะแนน 5 ด้าน):
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:6px; max-height:160px; overflow-y:auto;">
          ${{vils.map(v => `<span onclick="onSubdistrictVillageBadgeClick('${{v.properties.id}}')" style="background:#e8f0fe; color:#1a73e8; padding:4px 10px; border-radius:10px; font-size:0.76rem; font-weight:600; cursor:pointer;">${{v.properties.village}} (${{v.properties.priority.split(' ')[0]}})</span>`).join('')}}
        </div>
      `;
      dock.style.display = 'flex';
    }}

    function onSubdistrictVillageBadgeClick(vId) {{
      document.getElementById('villageSelect').value = vId;
      onVillageChange();
    }}

    function showVillageDetails(p) {{
      const dock = document.getElementById('smartDock');
      document.getElementById('dockAreaTitle').innerHTML = `🏡 ม.${{p.village}} (ต.${{p.subdistrict}} อ.${{p.district}})`;
      document.getElementById('dockPillBudget').innerHTML = `คะแนนรวม: ${{p.total_score}} / 15`;
      document.getElementById('dockPillRisk').innerHTML = `${{p.priority}}`;

      const getBadge = (text, score) => {{
        if (score === 3) return `<span style="background:#fce8e6; color:#d93025; padding:2px 8px; border-radius:10px; font-weight:600; font-size:0.75rem;">เสี่ยงสูง (3)</span>`;
        if (score === 2) return `<span style="background:#fef7e0; color:#b06000; padding:2px 8px; border-radius:10px; font-weight:600; font-size:0.75rem;">ปานกลาง (2)</span>`;
        return `<span style="background:#e6f4ea; color:#137333; padding:2px 8px; border-radius:10px; font-weight:600; font-size:0.75rem;">เสี่ยงน้อย (1)</span>`;
      }};

      document.getElementById('dockExpandedBody').innerHTML = `
        <div style="margin-bottom:10px; font-size:0.85rem;">
          ตำแหน่ง: <strong>หมู่บ้าน${{p.village}} ตำบล${{p.subdistrict}} อำเภอ${{p.district}}</strong>
        </div>
        <div style="border-top:1px solid #e8eaed; padding-top:10px;">
          <div style="font-weight:700; font-size:0.8rem; margin-bottom:8px; color:#3c4043;">คะแนนความเสี่ยง 5 มิติ:</div>
          <div style="display:grid; grid-template-columns: 1fr 1fr; gap:6px 16px; font-size:0.8rem;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span>💧 ด1: น้ำอุปโภคบริโภค</span>
              ${{getBadge(p.p1_text, p.p1_score)}}
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span>🌾 ด2: ภาคเกษตร</span>
              ${{getBadge(p.p2_text, p.p2_score)}}
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span>🌊 ด3: น้ำท่วมอุทกภัย</span>
              ${{getBadge(p.p3_text, p.p3_score)}}
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span>🧪 ด4: คุณภาพน้ำ</span>
              ${{getBadge(p.p4_text, p.p4_score)}}
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span>🌲 ด5: ป่าต้นน้ำ</span>
              ${{getBadge(p.p5_text, p.p5_score)}}
            </div>
          </div>
        </div>
      `;
      dock.style.display = 'flex';
      dock.classList.add('expanded');
      document.getElementById('expandIcon').textContent = 'expand_more';
      document.getElementById('expandText').textContent = 'ย่อเก็บ';
    }}
  </script>
</body>
</html>
"""

with open('ChiangMai_Water_GIS_Dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Flawless Drilldown GIS generated successfully!")
