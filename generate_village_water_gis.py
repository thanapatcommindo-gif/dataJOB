#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Advanced, High-UX Google Maps Styled Web GIS Dashboard for Chiang Mai Water Master Plan
Down to 2,200 Village Points + Multi-pillar Score Filters + Dual Sync Map + Auto Fit Bounds
"""

import json
import os

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
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>ระบบสารสนเทศภูมิศาสตร์ (GIS) แผนแม่บทน้ำ 5 ด้าน จ.เชียงใหม่</title>
  
  <!-- Google Fonts & Material Icons -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
  
  <!-- Leaflet CSS & Plugins -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" />
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" />
  
  <style>
    :root {{
      --primary: #1a73e8;
      --primary-dark: #1557b0;
      --primary-light: #e8f0fe;
      --danger: #d93025;
      --warning: #e37400;
      --yellow: #f9ab00;
      --success: #1e8e3e;
      --bg: #f8fafd;
      --card-bg: #ffffff;
      --text-main: #202124;
      --text-sub: #5f6368;
      --border: #dadce0;
      --shadow: 0 2px 6px 0 rgba(60,64,67,0.15), 0 1px 2px 0 rgba(60,64,67,0.3);
      --shadow-lg: 0 4px 16px rgba(60,64,67, 0.2);
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Prompt', 'Google Sans', sans-serif; }}
    body {{ background: var(--bg); color: var(--text-main); height: 100vh; display: flex; flex-direction: column; overflow: hidden; }}

    /* Top Google Navbar */
    header {{
      height: 60px;
      background: #ffffff;
      border-bottom: 1px solid var(--border);
      padding: 0 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      z-index: 1000;
      box-shadow: 0 1px 3px rgba(60,64,67, 0.08);
    }}
    .header-brand {{ display: flex; align-items: center; gap: 12px; }}
    .brand-icon {{
      width: 38px; height: 38px;
      background: linear-gradient(135deg, #1a73e8, #0d47a1);
      border-radius: 10px;
      display: flex; align-items: center; justify-content: center;
      color: #fff; font-size: 22px;
    }}
    .brand-title {{ font-size: 1.05rem; font-weight: 700; color: #1a73e8; line-height: 1.2; }}
    .brand-sub {{ font-size: 0.72rem; color: var(--text-sub); }}

    .header-kpis {{ display: flex; align-items: center; gap: 14px; }}
    .kpi-chip {{
      background: #f1f3f4;
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 0.8rem;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .kpi-chip strong {{ color: #1a73e8; font-weight: 700; }}

    /* Main Container */
    .app-body {{
      flex: 1;
      display: flex;
      position: relative;
      overflow: hidden;
    }}

    /* Sidebar Filters & Analytics */
    .sidebar {{
      width: 390px;
      background: #ffffff;
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      z-index: 500;
      box-shadow: 2px 0 8px rgba(0,0,0,0.05);
      transition: all 0.3s ease;
      overflow-y: auto;
    }}
    .sidebar.collapsed {{
      margin-left: -390px;
    }}

    .sidebar-section {{
      padding: 14px 18px;
      border-bottom: 1px solid #f1f3f4;
    }}
    .section-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 10px;
    }}
    .section-title {{
      font-size: 0.88rem;
      font-weight: 600;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    /* Active Filter Badges */
    .active-filters-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 10px;
    }}
    .filter-tag {{
      background: #e8f0fe;
      color: #1a73e8;
      padding: 4px 10px;
      border-radius: 14px;
      font-size: 0.74rem;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      cursor: pointer;
    }}
    .filter-tag:hover {{ background: #d2e3fc; }}

    /* Google Style Floating Search */
    .search-box {{
      position: relative;
      margin-bottom: 10px;
    }}
    .search-box input {{
      width: 100%;
      height: 40px;
      padding: 0 16px 0 40px;
      border: 1px solid var(--border);
      border-radius: 20px;
      font-size: 0.85rem;
      outline: none;
      background: #f8fafd;
      transition: all 0.2s;
    }}
    .search-box input:focus {{
      background: #ffffff;
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(26,115,232,0.15);
    }}
    .search-box .material-symbols-outlined {{
      position: absolute;
      left: 12px;
      top: 10px;
      color: var(--text-sub);
      font-size: 20px;
    }}

    /* Filter Form Controls */
    .form-group {{
      margin-bottom: 10px;
    }}
    .form-label {{
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--text-sub);
      margin-bottom: 4px;
      display: flex;
      justify-content: space-between;
    }}
    .form-select {{
      width: 100%;
      height: 36px;
      padding: 0 10px;
      border: 1px solid var(--border);
      border-radius: 8px;
      font-size: 0.82rem;
      background: #ffffff;
      outline: none;
      cursor: pointer;
    }}
    .form-select:focus {{
      border-color: var(--primary);
    }}

    /* Pillar Pill Filters */
    .pillar-filter-card {{
      background: #f8f9fa;
      border: 1px solid #e8eaed;
      border-radius: 10px;
      padding: 8px 10px;
      margin-bottom: 8px;
    }}
    .pillar-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.8rem;
      font-weight: 600;
      margin-bottom: 6px;
    }}
    .pillar-options {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 4px;
    }}
    .pill-btn {{
      padding: 5px 2px;
      font-size: 0.72rem;
      border: 1px solid #dadce0;
      border-radius: 6px;
      background: #fff;
      cursor: pointer;
      text-align: center;
      transition: all 0.15s;
    }}
    .pill-btn.active {{
      background: var(--primary);
      color: #fff;
      border-color: var(--primary);
      font-weight: 600;
    }}
    .pill-btn.active.high {{
      background: var(--danger);
      border-color: var(--danger);
      color: #fff;
    }}
    .pill-btn.active.med {{
      background: var(--warning);
      border-color: var(--warning);
      color: #fff;
    }}
    .pill-btn.active.low {{
      background: var(--success);
      border-color: var(--success);
      color: #fff;
    }}

    /* Score Slider */
    .score-range {{
      width: 100%;
      accent-color: var(--primary);
    }}

    /* Action Buttons */
    .btn-reset {{
      width: 100%;
      height: 38px;
      background: #f1f3f4;
      border: 1px solid #dadce0;
      border-radius: 10px;
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--text-sub);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.2s;
    }}
    .btn-reset:hover {{
      background: #e8eaed;
      color: var(--text-main);
    }}

    /* Map Views Container */
    .map-container {{
      flex: 1;
      position: relative;
      display: flex;
    }}
    .map-pane {{
      flex: 1;
      height: 100%;
      position: relative;
    }}
    .map-divider {{
      width: 6px;
      background: #dadce0;
      cursor: col-resize;
      z-index: 400;
      display: none;
    }}

    /* Floating View Controls */
    .floating-controls {{
      position: absolute;
      top: 14px;
      right: 14px;
      z-index: 800;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .control-card {{
      background: #ffffff;
      border-radius: 28px;
      box-shadow: var(--shadow);
      display: flex;
      padding: 4px;
      border: 1px solid var(--border);
    }}
    .mode-btn {{
      padding: 8px 16px;
      border-radius: 20px;
      border: none;
      background: transparent;
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--text-sub);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }}
    .mode-btn.active {{
      background: var(--primary);
      color: #fff;
      box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    }}

    .toggle-sidebar-btn {{
      position: absolute;
      top: 14px;
      left: 14px;
      z-index: 800;
      width: 42px; height: 42px;
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 50%;
      box-shadow: var(--shadow);
      display: flex; align-items: center; justify-content: center;
      cursor: pointer;
      color: var(--text-main);
    }}

    .btn-fit-bounds {{
      position: absolute;
      top: 66px;
      left: 14px;
      z-index: 800;
      width: 42px; height: 42px;
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 50%;
      box-shadow: var(--shadow);
      display: flex; align-items: center; justify-content: center;
      cursor: pointer;
      color: var(--text-main);
    }}

    /* Legend Overlay */
    .map-legend {{
      position: absolute;
      bottom: 24px;
      left: 14px;
      z-index: 800;
      background: rgba(255,255,255,0.95);
      backdrop-filter: blur(8px);
      padding: 12px 16px;
      border-radius: 14px;
      box-shadow: var(--shadow);
      border: 1px solid var(--border);
      font-size: 0.78rem;
      max-width: 260px;
    }}
    .legend-title {{ font-weight: 700; margin-bottom: 8px; color: var(--text-main); }}
    .legend-item {{ display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }}
    .legend-dot {{ width: 12px; height: 12px; border-radius: 50%; display: inline-block; }}

    /* Detail Card Slide-up */
    .detail-drawer {{
      position: absolute;
      bottom: 24px;
      right: 14px;
      width: 360px;
      max-height: 480px;
      background: #ffffff;
      border-radius: 18px;
      box-shadow: var(--shadow-lg);
      border: 1px solid var(--border);
      z-index: 900;
      display: none;
      flex-direction: column;
      overflow: hidden;
      animation: slideUp 0.25s ease-out;
    }}
    @keyframes slideUp {{
      from {{ transform: translateY(20px); opacity: 0; }}
      to {{ transform: translateY(0); opacity: 1; }}
    }}
    .drawer-header {{
      padding: 14px 18px;
      background: #f8fafd;
      border-bottom: 1px solid #e8eaed;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .drawer-header h4 {{ font-size: 0.95rem; font-weight: 700; color: #1a73e8; }}
    .drawer-close {{ background: none; border: none; cursor: pointer; color: var(--text-sub); }}
    .drawer-content {{ padding: 16px 18px; overflow-y: auto; font-size: 0.85rem; }}

    /* Custom Leaflet Tooltip & Pill Styles */
    .district-pill {{
      background: #ffffff;
      border: 1.5px solid #1a73e8;
      border-radius: 16px;
      padding: 2px 8px;
      font-size: 11px;
      font-weight: 600;
      color: #1a73e8;
      box-shadow: 0 1px 4px rgba(0,0,0,0.15);
      white-space: nowrap;
    }}
  </style>
</head>
<body>

  <!-- Top Navigation Header -->
  <header>
    <div class="header-brand">
      <div class="brand-icon">
        <span class="material-symbols-outlined">water_drop</span>
      </div>
      <div>
        <div class="brand-title">ระบบสารสนเทศภูมิศาสตร์ (GIS) แผนแม่บทน้ำ 5 ด้าน จ.เชียงใหม่</div>
        <div class="brand-sub">Chiang Mai Provincial Water Master Plan & 2,200 Village Risk Spatial Intelligence</div>
      </div>
    </div>

    <div class="header-kpis">
      <div class="kpi-chip">
        <span class="material-symbols-outlined" style="color:#1a73e8; font-size:18px;">payments</span>
        งบประมาณ: <strong>35,094.77 ลบ.</strong>
      </div>
      <div class="kpi-chip">
        <span class="material-symbols-outlined" style="color:#1a73e8; font-size:18px;">construction</span>
        โครงการ: <strong>6,312 โครงการ</strong>
      </div>
      <div class="kpi-chip">
        <span class="material-symbols-outlined" style="color:#d93025; font-size:18px;">warning</span>
        จุดเสี่ยง: <strong>2,200 หมู่บ้าน</strong>
      </div>
      <div class="kpi-chip" id="filter-count-badge" style="background:#e8f0fe; color:#1a73e8; font-weight:600;">
        แสดงผล: <span id="filtered-villages-count">2,200</span> หมู่บ้าน
      </div>
    </div>
  </header>

  <div class="app-body">
    
    <!-- Sidebar: Multi-level Filters & Pillar Scoring -->
    <aside class="sidebar" id="sidebar">
      
      <!-- Instant Search & District/Subdistrict Filter -->
      <div class="sidebar-section">
        <div class="section-title">
          <span class="material-symbols-outlined" style="color:var(--primary);">search</span>
          ค้นหาพื้นที่ (อำเภอ / ตำบล / หมู่บ้าน)
        </div>
        <div class="search-box">
          <span class="material-symbols-outlined">search</span>
          <input type="text" id="searchInput" placeholder="พิมพ์ชื่อหมู่บ้าน, ตำบล หรืออำเภอ..." oninput="applyAllFilters()">
        </div>

        <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 8px;">
          <div class="form-group">
            <label class="form-label">เลือกอำเภอ</label>
            <select class="form-select" id="districtSelect" onchange="onDistrictChange()">
              <option value="all">ทุกอำเภอ (25 อำเภอ)</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">เลือกตำบล</label>
            <select class="form-select" id="subdistrictSelect" onchange="applyAllFilters()">
              <option value="all">ทุกตำบล</option>
            </select>
          </div>
        </div>

        <div class="active-filters-bar" id="active-tags-container"></div>
      </div>

      <!-- Priority & Total Score Filter -->
      <div class="sidebar-section">
        <div class="section-header">
          <div class="section-title">
            <span class="material-symbols-outlined" style="color:#d93025;">priority_high</span>
            ระดับความสำคัญ & คะแนนรวม
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">ระดับความสำคัญ</label>
          <select class="form-select" id="prioritySelect" onchange="applyAllFilters()">
            <option value="all">ทุกระดับความสำคัญ</option>
            <option value="วิกฤติเร่งด่วน">🚨 วิกฤติเร่งด่วน (เสี่ยงสูง 2+ ด้าน)</option>
            <option value="เฝ้าระวังสูง">⚠️ เฝ้าระวังสูง (เสี่ยงสูง 1 ด้าน)</option>
            <option value="เฝ้าระวังปานกลาง">🟡 เฝ้าระวังปานกลาง (เสี่ยงกลาง 3+ ด้าน)</option>
            <option value="เสี่ยงต่ำ">🟢 เสี่ยงต่ำ/ทั่วไป</option>
          </select>
        </div>

        <div class="form-group">
          <div class="form-label">
            <span>คะแนนความเสี่ยงรวมขั้นต่ำ</span>
            <strong id="minScoreLabel" style="color:var(--primary);">5 คะแนน</strong>
          </div>
          <input type="range" class="score-range" id="minScoreRange" min="5" max="15" value="5" step="1" oninput="onScoreRangeInput(this.value)">
          <div style="display:flex; justify-content:space-between; font-size:0.7rem; color:var(--text-sub);">
            <span>5 (ต่ำสุด)</span>
            <span>10 (กลาง)</span>
            <span>15 (สูงสุด)</span>
          </div>
        </div>
      </div>

      <!-- 5 Pillars Individual Score Filter -->
      <div class="sidebar-section">
        <div class="section-header">
          <div class="section-title">
            <span class="material-symbols-outlined" style="color:#1a73e8;">tune</span>
            ตัวกรองคะแนนความเสี่ยงรายด้าน (5 มิติ)
          </div>
        </div>

        <!-- Pillar 1 -->
        <div class="pillar-filter-card">
          <div class="pillar-header">
            <span>💧 ด1: จัดการน้ำอุปโภคบริโภค</span>
          </div>
          <div class="pillar-options" data-pillar="p1">
            <div class="pill-btn active" onclick="setPillarFilter('p1', 'all', this)">ทั้งหมด</div>
            <div class="pill-btn high" onclick="setPillarFilter('p1', 'เสี่ยงสูง', this)">เสี่ยงสูง (3)</div>
            <div class="pill-btn med" onclick="setPillarFilter('p1', 'เสี่ยงปานกลาง', this)">ปานกลาง (2)</div>
            <div class="pill-btn low" onclick="setPillarFilter('p1', 'เสี่ยงน้อย', this)">เสี่ยงน้อย (1)</div>
          </div>
        </div>

        <!-- Pillar 2 -->
        <div class="pillar-filter-card">
          <div class="pillar-header">
            <span>🌾 ด2: ความมั่นคงน้ำภาคเกษตร/ผลิต</span>
          </div>
          <div class="pillar-options" data-pillar="p2">
            <div class="pill-btn active" onclick="setPillarFilter('p2', 'all', this)">ทั้งหมด</div>
            <div class="pill-btn high" onclick="setPillarFilter('p2', 'เสี่ยงสูง', this)">เสี่ยงสูง (3)</div>
            <div class="pill-btn med" onclick="setPillarFilter('p2', 'เสี่ยงปานกลาง', this)">ปานกลาง (2)</div>
            <div class="pill-btn low" onclick="setPillarFilter('p2', 'เสี่ยงน้อย', this)">เสี่ยงน้อย (1)</div>
          </div>
        </div>

        <!-- Pillar 3 -->
        <div class="pillar-filter-card">
          <div class="pillar-header">
            <span>🌊 ด3: จัดการน้ำท่วมและอุทกภัย</span>
          </div>
          <div class="pillar-options" data-pillar="p3">
            <div class="pill-btn active" onclick="setPillarFilter('p3', 'all', this)">ทั้งหมด</div>
            <div class="pill-btn high" onclick="setPillarFilter('p3', 'เสี่ยงสูง', this)">เสี่ยงสูง (3)</div>
            <div class="pill-btn med" onclick="setPillarFilter('p3', 'เสี่ยงปานกลาง', this)">ปานกลาง (2)</div>
            <div class="pill-btn low" onclick="setPillarFilter('p3', 'เสี่ยงน้อย', this)">เสี่ยงน้อย (1)</div>
          </div>
        </div>

        <!-- Pillar 4 -->
        <div class="pillar-filter-card">
          <div class="pillar-header">
            <span>🧪 ด4: คุณภาพน้ำและการอนุรักษ์</span>
          </div>
          <div class="pillar-options" data-pillar="p4">
            <div class="pill-btn active" onclick="setPillarFilter('p4', 'all', this)">ทั้งหมด</div>
            <div class="pill-btn high" onclick="setPillarFilter('p4', 'เสี่ยงสูง', this)">เสี่ยงสูง (3)</div>
            <div class="pill-btn med" onclick="setPillarFilter('p4', 'เสี่ยงปานกลาง', this)">ปานกลาง (2)</div>
            <div class="pill-btn low" onclick="setPillarFilter('p4', 'เสี่ยงน้อย', this)">เสี่ยงน้อย (1)</div>
          </div>
        </div>

        <!-- Pillar 5 -->
        <div class="pillar-filter-card">
          <div class="pillar-header">
            <span>🌲 ด5: อนุรักษ์ฟื้นฟูป่าต้นน้ำ</span>
          </div>
          <div class="pillar-options" data-pillar="p5">
            <div class="pill-btn active" onclick="setPillarFilter('p5', 'all', this)">ทั้งหมด</div>
            <div class="pill-btn high" onclick="setPillarFilter('p5', 'เสี่ยงสูง', this)">เสี่ยงสูง (3)</div>
            <div class="pill-btn med" onclick="setPillarFilter('p5', 'เสี่ยงปานกลาง', this)">ปานกลาง (2)</div>
            <div class="pill-btn low" onclick="setPillarFilter('p5', 'เสี่ยงน้อย', this)">เสี่ยงน้อย (1)</div>
          </div>
        </div>

        <button class="btn-reset" onclick="resetAllFilters()" style="margin-top:10px;">
          <span class="material-symbols-outlined">restart_alt</span>
          ล้างตัวกรองทั้งหมด (Reset)
        </button>
      </div>

    </aside>

    <!-- Map View Container -->
    <main class="map-container">
      
      <!-- Toggle Sidebar Button -->
      <button class="toggle-sidebar-btn" onclick="toggleSidebar()" title="ซ่อน/แสดงแถบตัวกรอง">
        <span class="material-symbols-outlined">menu_open</span>
      </button>

      <!-- Center / Fit Bounds Button -->
      <button class="btn-fit-bounds" onclick="fitChiangMaiBounds()" title="จัดกึ่งกลางแผนที่เชียงใหม่">
        <span class="material-symbols-outlined">crop_free</span>
      </button>

      <!-- Floating View Controls (Single Map vs Dual Comparison) -->
      <div class="floating-controls">
        <div class="control-card">
          <button class="mode-btn active" id="btn-single-mode" onclick="setMapMode('single')">
            <span class="material-symbols-outlined">map</span>
            แผนที่จุดเสี่ยง 2,200 หมู่บ้าน
          </button>
          <button class="mode-btn" id="btn-dual-mode" onclick="setMapMode('dual')">
            <span class="material-symbols-outlined">compare</span>
            เปรียบเทียบงบประมาณ (Dual Map)
          </button>
        </div>
      </div>

      <!-- Left Map (Village Risk & Pillars) -->
      <div class="map-pane" id="map-risk"></div>
      
      <div class="map-divider" id="map-divider"></div>

      <!-- Right Map (Budget & Projects) -->
      <div class="map-pane" id="map-budget" style="display:none;"></div>

      <!-- Map Legend -->
      <div class="map-legend">
        <div class="legend-title">ระดับความเสี่ยงรายหมู่บ้าน</div>
        <div class="legend-item"><span class="legend-dot" style="background:#d93025;"></span> 🚨 วิกฤติเร่งด่วน (เสี่ยงสูง 2+ ด้าน)</div>
        <div class="legend-item"><span class="legend-dot" style="background:#e37400;"></span> ⚠️ เฝ้าระวังสูง (เสี่ยงสูง 1 ด้าน)</div>
        <div class="legend-item"><span class="legend-dot" style="background:#f9ab00;"></span> 🟡 เฝ้าระวังปานกลาง (เสี่ยงกลาง 3+ ด้าน)</div>
        <div class="legend-item"><span class="legend-dot" style="background:#1e8e3e;"></span> 🟢 เสี่ยงต่ำ/ทั่วไป</div>
      </div>

      <!-- Detail Slide-up Drawer -->
      <div class="detail-drawer" id="detail-drawer">
        <div class="drawer-header">
          <h4 id="drawer-title">ข้อมูลหมู่บ้าน</h4>
          <button class="drawer-close" onclick="closeDrawer()">
            <span class="material-symbols-outlined">close</span>
          </button>
        </div>
        <div class="drawer-content" id="drawer-body"></div>
      </div>

    </main>

  </div>

  <!-- Leaflet JS & MarkerCluster -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  <script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>

  <script>
    // Injected Datasets
    const DISTRICTS_DATA = {districts_json_str};
    const VILLAGES_DATA = {villages_json_str};
    const SUMMARY_DATA = {dash_data_json_str};

    let mapRisk, mapBudget;
    let districtLayerRisk, districtLayerBudget;
    let villageClusterGroup;
    let currentMapMode = 'single';
    let isSyncing = false;
    let cmBounds;

    // Filter States
    let pillarFilters = {{
      p1: 'all', p2: 'all', p3: 'all', p4: 'all', p5: 'all'
    }};
    let minScore = 5;

    // Initialize Application
    window.addEventListener('DOMContentLoaded', () => {{
      initMaps();
      populateDropdowns();
      renderDistrictPolygons();
      renderVillagePoints(VILLAGES_DATA.features);
      fitChiangMaiBounds();
    }});

    function initMaps() {{
      const cmCenter = [18.7883, 98.9853];
      const initialZoom = 9;

      // Google Maps Tile URL in Thai
      const googleMapsUrl = 'https://mt1.google.com/vt/lyrs=m&hl=th&x={{x}}&y={{y}}&z={{z}}';

      mapRisk = L.map('map-risk', {{
        center: cmCenter,
        zoom: initialZoom,
        zoomControl: false
      }});

      L.tileLayer(googleMapsUrl, {{
        maxZoom: 19,
        attribution: '© Google Maps'
      }}).addTo(mapRisk);

      L.control.zoom({{ position: 'bottomright' }}).addTo(mapRisk);

      // Right Map for Budget
      mapBudget = L.map('map-budget', {{
        center: cmCenter,
        zoom: initialZoom,
        zoomControl: false
      }});

      L.tileLayer(googleMapsUrl, {{
        maxZoom: 19,
        attribution: '© Google Maps'
      }}).addTo(mapBudget);

      L.control.zoom({{ position: 'bottomright' }}).addTo(mapBudget);

      // Synchronize Dual Maps
      mapRisk.on('move', () => {{
        if (!isSyncing && currentMapMode === 'dual') {{
          isSyncing = true;
          mapBudget.setView(mapRisk.getCenter(), mapRisk.getZoom(), {{ animate: false }});
          isSyncing = false;
        }}
      }});

      mapBudget.on('move', () => {{
        if (!isSyncing && currentMapMode === 'dual') {{
          isSyncing = true;
          mapRisk.setView(mapBudget.getCenter(), mapBudget.getZoom(), {{ animate: false }});
          isSyncing = false;
        }}
      }});

      villageClusterGroup = L.markerClusterGroup({{
        maxClusterRadius: 35,
        spiderfyOnMaxZoom: true,
        showCoverageOnHover: false,
        zoomToBoundsOnClick: true
      }}).addTo(mapRisk);
    }}

    function populateDropdowns() {{
      const distSelect = document.getElementById('districtSelect');
      const districts = [...new Set(VILLAGES_DATA.features.map(f => f.properties.district))].sort((a,b) => a.localeCompare(b, 'th'));

      districts.forEach(d => {{
        const opt = document.createElement('option');
        opt.value = d;
        opt.textContent = d;
        distSelect.appendChild(opt);
      }});
    }}

    function onDistrictChange() {{
      const dist = document.getElementById('districtSelect').value;
      const subSelect = document.getElementById('subdistrictSelect');
      subSelect.innerHTML = '<option value="all">ทุกตำบล</option>';

      if (dist !== 'all') {{
        const subdistricts = [...new Set(
          VILLAGES_DATA.features
            .filter(f => f.properties.district === dist)
            .map(f => f.properties.subdistrict)
        )].sort((a,b) => a.localeCompare(b, 'th'));

        subdistricts.forEach(s => {{
          const opt = document.createElement('option');
          opt.value = s;
          opt.textContent = s;
          subSelect.appendChild(opt);
        }});
      }}

      applyAllFilters();
    }}

    function renderDistrictPolygons() {{
      // Risk Map District Polygons (Clean outlines)
      districtLayerRisk = L.geoJSON(DISTRICTS_DATA, {{
        style: (feature) => ({{
          fillColor: '#1a73e8',
          weight: 1.8,
          opacity: 0.85,
          color: '#1a73e8',
          fillOpacity: 0.04
        }}),
        onEachFeature: (feature, layer) => {{
          const p = feature.properties;
          const ampName = p.amp_th || p.d_name || 'อำเภอ';
          layer.bindTooltip(`<div class="district-pill">${{ampName}}</div>`, {{
            permanent: false,
            direction: 'center',
            className: 'custom-tooltip'
          }});
          layer.on('click', () => showDistrictDetails(p));
        }}
      }}).addTo(mapRisk);

      cmBounds = districtLayerRisk.getBounds();

      // Budget Map District Polygons with Chloropleth
      districtLayerBudget = L.geoJSON(DISTRICTS_DATA, {{
        style: (feature) => {{
          const b = feature.properties.total_budget || 0;
          let color = '#e8f0fe';
          if (b > 3000) color = '#0d47a1';
          else if (b > 1500) color = '#1976d2';
          else if (b > 800) color = '#42a5f5';
          else if (b > 400) color = '#90caf9';

          return {{
            fillColor: color,
            weight: 1.5,
            opacity: 0.9,
            color: '#1557b0',
            fillOpacity: 0.6
          }};
        }},
        onEachFeature: (feature, layer) => {{
          const p = feature.properties;
          const ampName = p.amp_th || p.d_name || 'อำเภอ';
          const budget = (p.total_budget || 0).toLocaleString('th-TH', {{ minimumFractionDigits: 1 }});
          layer.bindPopup(`
            <div style="font-size:0.9rem; padding:4px;">
              <strong style="color:#1a73e8; font-size:1rem;">${{ampName}}</strong>
              <div style="margin-top:6px; color:#5f6368;">งบประมาณ: <strong style="color:#202124;">${{budget}} ล้านบาท</strong></div>
              <div style="color:#5f6368;">โครงการ: <strong style="color:#202124;">${{p.total_projects || 0}} โครงการ</strong></div>
              <div style="color:#5f6368;">จุดเสี่ยงสูง: <strong style="color:#d93025;">${{p.high_risk_total || 0}} จุด</strong></div>
            </div>
          `);
        }}
      }}).addTo(mapBudget);
    }}

    function getVillageColor(props) {{
      if (props.priority.includes('วิกฤติ')) return '#d93025';
      if (props.priority.includes('เฝ้าระวังสูง')) return '#e37400';
      if (props.priority.includes('เฝ้าระวังปานกลาง')) return '#f9ab00';
      return '#1e8e3e';
    }}

    function renderVillagePoints(features) {{
      villageClusterGroup.clearLayers();

      const markers = features.map(f => {{
        const p = f.properties;
        const color = getVillageColor(p);
        const [lng, lat] = f.geometry.coordinates;

        const marker = L.circleMarker([lat, lng], {{
          radius: 6,
          fillColor: color,
          color: '#ffffff',
          weight: 1.5,
          opacity: 1,
          fillOpacity: 0.95
        }});

        marker.on('click', () => showVillageDetails(p));
        return marker;
      }});

      villageClusterGroup.addLayers(markers);
      document.getElementById('filtered-villages-count').textContent = features.length.toLocaleString('th-TH');
      updateActiveFilterTags();
    }}

    function setPillarFilter(pillar, val, el) {{
      pillarFilters[pillar] = val;
      const container = el.parentElement;
      container.querySelectorAll('.pill-btn').forEach(btn => btn.classList.remove('active'));
      el.classList.add('active');
      applyAllFilters();
    }}

    function onScoreRangeInput(val) {{
      minScore = parseInt(val);
      document.getElementById('minScoreLabel').textContent = `${{minScore}} คะแนน`;
      applyAllFilters();
    }}

    function applyAllFilters() {{
      const searchText = document.getElementById('searchInput').value.trim().toLowerCase();
      const dist = document.getElementById('districtSelect').value;
      const sub = document.getElementById('subdistrictSelect').value;
      const priority = document.getElementById('prioritySelect').value;

      const filtered = VILLAGES_DATA.features.filter(f => {{
        const p = f.properties;

        // Search match
        if (searchText) {{
          const target = `${{p.village}} ${{p.subdistrict}} ${{p.district}}`.toLowerCase();
          if (!target.includes(searchText)) return false;
        }}

        // District & Subdistrict match
        if (dist !== 'all' && p.district !== dist) return false;
        if (sub !== 'all' && p.subdistrict !== sub) return false;

        // Priority match
        if (priority !== 'all' && !p.priority.includes(priority)) return false;

        // Total Score match
        if (p.total_score < minScore) return false;

        // 5 Pillars Match
        if (pillarFilters.p1 !== 'all' && p.p1_text !== pillarFilters.p1) return false;
        if (pillarFilters.p2 !== 'all' && p.p2_text !== pillarFilters.p2) return false;
        if (pillarFilters.p3 !== 'all' && p.p3_text !== pillarFilters.p3) return false;
        if (pillarFilters.p4 !== 'all' && p.p4_text !== pillarFilters.p4) return false;
        if (pillarFilters.p5 !== 'all' && p.p5_text !== pillarFilters.p5) return false;

        return true;
      }});

      renderVillagePoints(filtered);

      // Auto zoom to filtered bounds
      if (filtered.length > 0) {{
        if (dist !== 'all' || sub !== 'all' || searchText) {{
          const group = L.featureGroup(filtered.map(f => L.marker([f.geometry.coordinates[1], f.geometry.coordinates[0]])));
          mapRisk.fitBounds(group.getBounds().pad(0.12));
        }}
      }}
    }}

    function updateActiveFilterTags() {{
      const container = document.getElementById('active-tags-container');
      container.innerHTML = '';

      const dist = document.getElementById('districtSelect').value;
      const sub = document.getElementById('subdistrictSelect').value;
      const priority = document.getElementById('prioritySelect').value;

      if (dist !== 'all') {{
        addTag(`อ.${{dist}}`, () => {{ document.getElementById('districtSelect').value = 'all'; onDistrictChange(); }});
      }}
      if (sub !== 'all') {{
        addTag(`ต.${{sub}}`, () => {{ document.getElementById('subdistrictSelect').value = 'all'; applyAllFilters(); }});
      }}
      if (priority !== 'all') {{
        addTag(priority, () => {{ document.getElementById('prioritySelect').value = 'all'; applyAllFilters(); }});
      }}
      if (minScore > 5) {{
        addTag(`คะแนน ≥ ${{minScore}}`, () => {{
          minScore = 5;
          document.getElementById('minScoreRange').value = 5;
          document.getElementById('minScoreLabel').textContent = '5 คะแนน';
          applyAllFilters();
        }});
      }}

      const pillarNames = {{ p1: 'ด1', p2: 'ด2', p3: 'ด3', p4: 'ด4', p5: 'ด5' }};
      for (const [k, v] of Object.entries(pillarFilters)) {{
        if (v !== 'all') {{
          addTag(`${{pillarNames[k]}}: ${{v}}`, () => {{
            const card = document.querySelector(`.pillar-options[data-pillar="${{k}}"]`);
            card.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('active'));
            card.querySelector('.pill-btn').classList.add('active');
            pillarFilters[k] = 'all';
            applyAllFilters();
          }});
        }}
      }}
    }}

    function addTag(text, onRemove) {{
      const tag = document.createElement('span');
      tag.className = 'filter-tag';
      tag.innerHTML = `${{text}} <span class="material-symbols-outlined" style="font-size:14px;">close</span>`;
      tag.onclick = onRemove;
      document.getElementById('active-tags-container').appendChild(tag);
    }}

    function fitChiangMaiBounds() {{
      if (cmBounds) {{
        mapRisk.fitBounds(cmBounds.pad(0.05));
        if (mapBudget) mapBudget.fitBounds(cmBounds.pad(0.05));
      }} else {{
        mapRisk.setView([18.7883, 98.9853], 9);
      }}
    }}

    function resetAllFilters() {{
      document.getElementById('searchInput').value = '';
      document.getElementById('districtSelect').value = 'all';
      document.getElementById('subdistrictSelect').innerHTML = '<option value="all">ทุกตำบล</option>';
      document.getElementById('prioritySelect').value = 'all';
      document.getElementById('minScoreRange').value = 5;
      document.getElementById('minScoreLabel').textContent = '5 คะแนน';
      minScore = 5;

      pillarFilters = {{ p1: 'all', p2: 'all', p3: 'all', p4: 'all', p5: 'all' }};
      document.querySelectorAll('.pillar-options').forEach(c => {{
        c.querySelectorAll('.pill-btn').forEach(btn => btn.classList.remove('active'));
        c.querySelector('.pill-btn').classList.add('active');
      }});

      renderVillagePoints(VILLAGES_DATA.features);
      fitChiangMaiBounds();
      closeDrawer();
    }}

    function showVillageDetails(p) {{
      const drawer = document.getElementById('detail-drawer');
      document.getElementById('drawer-title').innerHTML = `📍 ${{p.village}}`;

      const p1Badge = getScoreBadge(p.p1_text, p.p1_score);
      const p2Badge = getScoreBadge(p.p2_text, p.p2_score);
      const p3Badge = getScoreBadge(p.p3_text, p.p3_score);
      const p4Badge = getScoreBadge(p.p4_text, p.p4_score);
      const p5Badge = getScoreBadge(p.p5_text, p.p5_score);

      document.getElementById('drawer-body').innerHTML = `
        <div style="margin-bottom:12px; font-size:0.9rem;">
          <div style="color:#5f6368;">พื้นที่: <strong>ต.${{p.subdistrict}} อ.${{p.district}}</strong></div>
          <div style="margin-top:4px;">ระดับความสำคัญ: <strong>${{p.priority}}</strong></div>
          <div style="margin-top:4px;">คะแนนความเสี่ยงรวม: <strong style="font-size:1.1rem; color:#1a73e8;">${{p.total_score}} / 15</strong></div>
        </div>

        <div style="border-top:1px solid #e8eaed; padding-top:10px;">
          <strong style="font-size:0.82rem; color:#202124;">คะแนนรายด้าน 5 มิติ:</strong>
          
          <div style="display:flex; justify-content:space-between; margin-top:8px; font-size:0.8rem;">
            <span>💧 ด1: น้ำอุปโภคบริโภค</span>
            ${{p1Badge}}
          </div>
          <div style="display:flex; justify-content:space-between; margin-top:6px; font-size:0.8rem;">
            <span>🌾 ด2: ความมั่นคงน้ำภาคเกษตร</span>
            ${{p2Badge}}
          </div>
          <div style="display:flex; justify-content:space-between; margin-top:6px; font-size:0.8rem;">
            <span>🌊 ด3: น้ำท่วมและอุทกภัย</span>
            ${{p3Badge}}
          </div>
          <div style="display:flex; justify-content:space-between; margin-top:6px; font-size:0.8rem;">
            <span>🧪 ด4: คุณภาพน้ำและอนุรักษ์</span>
            ${{p4Badge}}
          </div>
          <div style="display:flex; justify-content:space-between; margin-top:6px; font-size:0.8rem;">
            <span>🌲 ด5: ป่าต้นน้ำ/ดินพังทลาย</span>
            ${{p5Badge}}
          </div>
        </div>
      `;

      drawer.style.display = 'flex';
    }}

    function showDistrictDetails(p) {{
      const drawer = document.getElementById('detail-drawer');
      const ampName = p.amp_th || p.d_name || 'อำเภอ';
      document.getElementById('drawer-title').innerHTML = `🏛️ อำเภอ${{ampName}}`;

      document.getElementById('drawer-body').innerHTML = `
        <div style="margin-bottom:12px; font-size:0.9rem;">
          <div style="color:#5f6368;">สถานะจัดสรร: <strong>${{p.gap_status || 'ปกติ'}}</strong></div>
          <div style="margin-top:6px; font-size:1.1rem; color:#1a73e8; font-weight:700;">
            งบประมาณ: ${{Number(p.total_budget || 0).toLocaleString('th-TH', {{ minimumFractionDigits: 1 }})}} ลบ.
          </div>
          <div style="color:#5f6368;">จำนวนโครงการ: <strong>${{p.total_projects || 0}} โครงการ</strong></div>
          <div style="color:#d93025; margin-top:4px;">จุดเสี่ยงสูง: <strong>${{p.high_risk_total || 0}} จุด</strong></div>
          <div style="color:#5f6368;">หมู่บ้านทั้งหมด: <strong>${{p.villages || 0}} หมู่บ้าน</strong></div>
        </div>
      `;
      drawer.style.display = 'flex';
    }}

    function getScoreBadge(text, score) {{
      if (score === 3) return `<span style="background:#fce8e6; color:#d93025; padding:2px 8px; border-radius:10px; font-weight:600; font-size:0.75rem;">เสี่ยงสูง (3)</span>`;
      if (score === 2) return `<span style="background:#fef7e0; color:#b06000; padding:2px 8px; border-radius:10px; font-weight:600; font-size:0.75rem;">ปานกลาง (2)</span>`;
      return `<span style="background:#e6f4ea; color:#137333; padding:2px 8px; border-radius:10px; font-weight:600; font-size:0.75rem;">เสี่ยงน้อย (1)</span>`;
    }}

    function closeDrawer() {{
      document.getElementById('detail-drawer').style.display = 'none';
    }}

    function toggleSidebar() {{
      document.getElementById('sidebar').classList.toggle('collapsed');
      setTimeout(() => {{
        mapRisk.invalidateSize();
        if (mapBudget) mapBudget.invalidateSize();
      }}, 350);
    }}

    function setMapMode(mode) {{
      currentMapMode = mode;
      const singleBtn = document.getElementById('btn-single-mode');
      const dualBtn = document.getElementById('btn-dual-mode');
      const budgetPane = document.getElementById('map-budget');
      const divider = document.getElementById('map-divider');

      if (mode === 'dual') {{
        singleBtn.classList.remove('active');
        dualBtn.classList.add('active');
        budgetPane.style.display = 'block';
        divider.style.display = 'block';
        setTimeout(() => {{
          mapRisk.invalidateSize();
          mapBudget.invalidateSize();
          fitChiangMaiBounds();
        }}, 100);
      }} else {{
        dualBtn.classList.remove('active');
        singleBtn.classList.add('active');
        budgetPane.style.display = 'none';
        divider.style.display = 'none';
        setTimeout(() => {{
          mapRisk.invalidateSize();
          fitChiangMaiBounds();
        }}, 100);
      }}
    }}
  </script>
</body>
</html>
"""

# Write to ChiangMai_Water_GIS_Dashboard.html and index.html
with open('ChiangMai_Water_GIS_Dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("High-UX Water GIS Dashboard & index.html updated successfully!")
