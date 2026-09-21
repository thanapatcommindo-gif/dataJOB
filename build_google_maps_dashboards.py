import json
import os

print("Building Google Maps styled GIS Dashboards for both datasets...")

# -----------------------------------------------------------------------------
# 1. BUILD CHIANG MAI WATER GIS DASHBOARD (DISTRICT & DUAL COMPARISON)
# -----------------------------------------------------------------------------
with open('chiangmai_districts_gis.geojson', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

with open('dashboard_data.json', 'r', encoding='utf-8') as f:
    stats_data = json.load(f)

geojson_str = json.dumps(geojson_data, ensure_ascii=False)
stats_str = json.dumps(stats_data, ensure_ascii=False)

html_water_template = """<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>แผนที่ Google Maps แผนบริหารจัดการน้ำ จ.เชียงใหม่ (2565-2570)</title>
  
  <!-- Tailwind CSS -->
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  
  <!-- Leaflet CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  
  <!-- Google Fonts: Prompt & Sarabun -->
  <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@400;500;600;700&family=Sarabun:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <style>
    body { font-family: 'Prompt', 'Sarabun', -apple-system, BlinkMacSystemFont, sans-serif; background-color: #f8f9fa; }
    .map-frame { height: calc(100vh - 145px); min-height: 520px; border-radius: 16px; }
    .map-frame-dual { height: calc(100vh - 180px); min-height: 480px; border-radius: 16px; }
    
    /* Google Maps Label Bubble */
    .gmap-label {
      background: rgba(255, 255, 255, 0.95) !important;
      border: 1px solid #dadce0 !important;
      border-radius: 20px !important;
      box-shadow: 0 2px 6px rgba(60,64,67,0.15) !important;
      color: #202124 !important;
      font-size: 11px !important;
      font-weight: 600 !important;
      padding: 3px 8px !important;
      font-family: 'Prompt', sans-serif !important;
      white-space: nowrap !important;
    }
    .gmap-label:before { border-top-color: #ffffff !important; }
    
    /* Google Card Shadows */
    .g-card {
      background: #ffffff;
      border: 1px solid #e8eaed;
      border-radius: 16px;
      box-shadow: 0 1px 3px rgba(60,64,67,0.12), 0 4px 8px rgba(60,64,67,0.06);
    }
    
    .g-btn-active {
      background-color: #1a73e8 !important;
      color: #ffffff !important;
      box-shadow: 0 1px 3px rgba(26,115,232,0.3) !important;
    }

    /* Custom Leaflet Controls */
    .leaflet-bar { border: none !important; box-shadow: 0 2px 6px rgba(60,64,67,0.2) !important; border-radius: 8px !important; overflow: hidden; }
    .leaflet-bar a { background: #ffffff !important; color: #3c4043 !important; border-bottom: 1px solid #f1f3f4 !important; }
  </style>
</head>
<body class="antialiased text-slate-800 flex flex-col min-h-screen">

  <!-- Top Google-style Navigation Bar -->
  <nav class="bg-white border-b border-slate-200 sticky top-0 z-50 px-4 py-2.5 shadow-sm">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-3">
      
      <!-- Brand & Search -->
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-full bg-blue-50 border border-blue-200 flex items-center justify-center text-blue-600 text-lg shadow-sm">
          📍
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-base font-bold text-slate-900 leading-tight">แผนที่น้ำเชียงใหม่ (Google Maps)</h1>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-blue-100 text-blue-800">25 อำเภอ 6,312 โครงการ</span>
          </div>
          <p class="text-xs text-slate-500">เปรียบเทียบระดับความเสี่ยง 5 ด้าน vs งบประมาณแผนน้ำ 35,094.77 ล้านบาท</p>
        </div>
      </div>

      <!-- Navigation Tabs -->
      <div class="flex items-center bg-slate-100 p-1 rounded-full border border-slate-200 overflow-x-auto text-xs">
        <button onclick="switchView('view-dual')" id="btn-dual" class="nav-btn px-4 py-1.5 rounded-full font-semibold transition g-btn-active">
          🔄 แผนที่เปรียบเทียบ 2 ฝั่ง (ความเสี่ยง vs งบประมาณ)
        </button>
        <button onclick="switchView('view-single')" id="btn-single" class="nav-btn px-4 py-1.5 rounded-full font-semibold transition text-slate-600 hover:text-slate-900">
          🔍 แผนที่สำรวจรายอำเภอ (Single View)
        </button>
        <button onclick="switchView('view-summary')" id="btn-summary" class="nav-btn px-4 py-1.5 rounded-full font-semibold transition text-slate-600 hover:text-slate-900">
          📊 ตารางสรุป 25 อำเภอ & ดาวน์โหลด
        </button>
      </div>

    </div>
  </nav>

  <!-- ========================================================================= -->
  <!-- VIEW 1: DUAL SYNCED GOOGLE MAPS (เปรียบเทียบ 2 แผนที่) -->
  <!-- ========================================================================= -->
  <main id="view-dual" class="flex-1 max-w-7xl w-full mx-auto p-3 md:p-4 flex flex-col space-y-3">
    
    <!-- Filter Chips & Floating Inspector -->
    <div class="g-card p-3 flex flex-col lg:flex-row lg:items-center justify-between gap-3">
      
      <!-- Filter Chips -->
      <div class="flex flex-wrap items-center gap-1.5 text-xs">
        <span class="font-bold text-slate-700 mr-1">เลือกด้าน:</span>
        <button onclick="filterPillar('all')" id="chip-all" class="pillar-chip px-3 py-1 rounded-full border border-blue-600 bg-blue-600 text-white font-semibold shadow-sm">🌟 รวม 5 ด้าน</button>
        <button onclick="filterPillar('1')" id="chip-1" class="pillar-chip px-3 py-1 rounded-full border border-slate-300 bg-white text-slate-700 hover:bg-slate-50 font-medium">ด1 อุปโภคบริโภค</button>
        <button onclick="filterPillar('2')" id="chip-2" class="pillar-chip px-3 py-1 rounded-full border border-slate-300 bg-white text-slate-700 hover:bg-slate-50 font-medium">ด2 น้ำภาคการผลิต (เกษตร)</button>
        <button onclick="filterPillar('3')" id="chip-3" class="pillar-chip px-3 py-1 rounded-full border border-slate-300 bg-white text-slate-700 hover:bg-slate-50 font-medium">ด3 น้ำท่วมอุทกภัย</button>
        <button onclick="filterPillar('4')" id="chip-4" class="pillar-chip px-3 py-1 rounded-full border border-slate-300 bg-white text-slate-700 hover:bg-slate-50 font-medium">ด4 คุณภาพน้ำ</button>
        <button onclick="filterPillar('5')" id="chip-5" class="pillar-chip px-3 py-1 rounded-full border border-slate-300 bg-white text-slate-700 hover:bg-slate-50 font-medium">ด5 ป่าต้นน้ำ/ดิน</button>
      </div>

      <!-- Reset & Tip -->
      <div class="flex items-center gap-2 text-xs">
        <span class="text-slate-500">💡 เลื่อนหรือซูมแผนที่ใด อีกฝั่งจะขยับตามกันอัตโนมัติ</span>
        <button onclick="resetDualMaps()" class="px-3 py-1 rounded-lg border border-slate-300 bg-white hover:bg-slate-50 font-medium">🎯 กึ่งกลาง</button>
      </div>

    </div>

    <!-- Active Comparison Result Banner -->
    <div id="inspector-bar" class="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 text-white p-3 rounded-xl shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs">
      <div class="flex items-center gap-2.5">
        <span class="text-base">📌</span>
        <div>
          <span class="text-blue-300 text-[11px]">ข้อมูลเปรียบเทียบเชิงพื้นที่ (คลิกบนแผนที่เพื่อเลือกอำเภอ):</span>
          <div id="ins-name" class="font-bold text-sm text-white">อำเภอสารภี (106 หมู่บ้าน)</div>
        </div>
      </div>

      <div class="flex flex-wrap items-center gap-3">
        <div class="bg-white/10 px-3 py-1 rounded-lg border border-white/10">
          <span class="text-rose-300">จุดเสี่ยงสูง:</span> <strong id="ins-risk" class="text-white text-sm font-bold">185 จุด (อันดับ 1)</strong>
        </div>
        <div class="bg-white/10 px-3 py-1 rounded-lg border border-white/10">
          <span class="text-blue-300">งบประมาณ:</span> <strong id="ins-budget" class="text-white text-sm font-bold">558.60 ลบ. (103 โครงการ)</strong>
        </div>
        <div class="bg-amber-400/20 px-3 py-1 rounded-lg border border-amber-300/30">
          <span class="text-amber-200">สถานะ:</span> <strong id="ins-gap" class="text-amber-300 text-sm font-bold">🚨 เสี่ยงสูงวิกฤติ - งบไม่เพียงพอ</strong>
        </div>
      </div>
    </div>

    <!-- Dual Maps Container -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-3 flex-1">
      
      <!-- LEFT: RISK MAP -->
      <div class="g-card overflow-hidden flex flex-col relative shadow-sm">
        <div class="px-4 py-2 bg-rose-50/80 border-b border-rose-100 flex items-center justify-between text-xs">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
            <span class="font-bold text-rose-950">1. แผนที่ระดับความเสี่ยงภัยน้ำ (Risk Map)</span>
          </div>
          <span id="txt-left-metric" class="font-semibold text-rose-700 bg-rose-100 px-2 py-0.5 rounded-full">จุดเสี่ยงสูง (2,200 หมู่บ้าน)</span>
        </div>
        <div id="map-risk" class="map-frame-dual flex-1"></div>
        <!-- Clean Google Maps Legend -->
        <div class="p-2 bg-white border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
          <span>เสี่ยงต่ำ (0-10 จุด)</span>
          <div class="flex items-center gap-1">
            <span class="w-5 h-2.5 rounded-sm" style="background:#fee2e2"></span>
            <span class="w-5 h-2.5 rounded-sm" style="background:#fca5a5"></span>
            <span class="w-5 h-2.5 rounded-sm" style="background:#f87171"></span>
            <span class="w-5 h-2.5 rounded-sm" style="background:#ef4444"></span>
            <span class="w-5 h-2.5 rounded-sm" style="background:#b91c1c"></span>
          </div>
          <span class="font-bold text-rose-700">วิกฤติสูงสุด (180+ จุด)</span>
        </div>
      </div>

      <!-- RIGHT: BUDGET MAP -->
      <div class="g-card overflow-hidden flex flex-col relative shadow-sm">
        <div class="px-4 py-2 bg-blue-50/80 border-b border-blue-100 flex items-center justify-between text-xs">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-blue-600"></span>
            <span class="font-bold text-blue-950">2. แผนที่การจัดสรรงบประมาณ (Budget Map)</span>
          </div>
          <span id="txt-right-metric" class="font-semibold text-blue-700 bg-blue-100 px-2 py-0.5 rounded-full">งบประมาณรวม (ล้านบาท)</span>
        </div>
        <div id="map-budget" class="map-frame-dual flex-1"></div>
        <!-- Clean Google Maps Legend -->
        <div class="p-2 bg-white border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
          <span>งบน้อย (&lt;400 ลบ.)</span>
          <div class="flex items-center gap-1">
            <span class="w-5 h-2.5 rounded-sm" style="background:#e0f2fe"></span>
            <span class="w-5 h-2.5 rounded-sm" style="background:#bae6fd"></span>
            <span class="w-5 h-2.5 rounded-sm" style="background:#38bdf8"></span>
            <span class="w-5 h-2.5 rounded-sm" style="background:#0284c7"></span>
            <span class="w-5 h-2.5 rounded-sm" style="background:#0369a1"></span>
          </div>
          <span class="font-bold text-blue-800">งบสูงสุด (4,000+ ลบ.)</span>
        </div>
      </div>

    </div>

  </main>

  <!-- ========================================================================= -->
  <!-- VIEW 2: SINGLE GIS EXPLORER (หน้าสำรวจเดี่ยว) -->
  <!-- ========================================================================= -->
  <main id="view-single" class="flex-1 max-w-7xl w-full mx-auto p-3 md:p-4 hidden flex flex-col space-y-3">
    
    <div class="g-card p-3 flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs">
      <div class="flex items-center gap-2">
        <input type="text" id="gmap-search" oninput="searchDistrict()" placeholder="🔍 พิมพ์ชื่ออำเภอ (เช่น สารภี, แม่แตง, เมือง)..." class="px-3 py-1.5 border border-slate-300 rounded-lg w-64 focus:ring-2 focus:ring-blue-500 outline-none">
        
        <select id="single-metric" onchange="updateSingleMap()" class="px-3 py-1.5 font-semibold bg-slate-50 border border-slate-300 rounded-lg outline-none">
          <option value="high_risk_total">🚨 จุดเสี่ยงสูงรวมทุกด้าน</option>
          <option value="total_budget">💰 งบประมาณรวม (ล้านบาท)</option>
          <option value="total_projects">📋 จำนวนโครงการรวม</option>
          <option value="high_p1">🌊 เสี่ยงสูง ด้าน 1 (อุปโภค)</option>
          <option value="high_p2">🌾 เสี่ยงสูง ด้าน 2 (เกษตร/ผลิต)</option>
          <option value="high_p3">⛈️ เสี่ยงสูง ด้าน 3 (น้ำท่วม)</option>
          <option value="high_p4">💧 เสี่ยงสูง ด้าน 4 (คุณภาพน้ำ)</option>
          <option value="high_p5">🌲 เสี่ยงสูง ด้าน 5 (ป่าต้นน้ำ/ดิน)</option>
        </select>
      </div>

      <!-- Basemap Type -->
      <div class="flex items-center gap-1.5">
        <span class="text-slate-500 font-medium">รูปแบบแผนที่ Google:</span>
        <button onclick="setGoogleLayer('streets')" id="btn-layer-m" class="px-2.5 py-1 rounded bg-blue-600 text-white font-semibold">แผนที่ถนน</button>
        <button onclick="setGoogleLayer('hybrid')" id="btn-layer-y" class="px-2.5 py-1 rounded bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium">ดาวเทียม</button>
        <button onclick="setGoogleLayer('terrain')" id="btn-layer-p" class="px-2.5 py-1 rounded bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium">ภูมิประเทศ</button>
      </div>
    </div>

    <!-- Map & Google Detail Panel -->
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-3 flex-1">
      <div class="lg:col-span-3 g-card overflow-hidden relative">
        <div id="map-single" class="map-frame w-full"></div>
      </div>

      <!-- Right Detail Panel (Google Place Style) -->
      <div class="lg:col-span-1 g-card p-4 flex flex-col justify-between overflow-y-auto max-h-[600px] text-xs">
        <div>
          <div class="flex items-center justify-between pb-3 border-b border-slate-100">
            <span class="text-[10px] font-bold text-slate-400 uppercase">ข้อมูลอำเภอ</span>
            <span id="single-badge-gap" class="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700">-</span>
          </div>

          <div class="mt-3">
            <h2 id="single-title" class="text-xl font-bold text-slate-900">อำเภอสารภี</h2>
            <p id="single-subtitle" class="text-slate-500 mt-0.5">จังหวัดเชียงใหม่ • 106 หมู่บ้าน (พื้นที่ 104.9 ตร.กม.)</p>
          </div>

          <div class="mt-4 space-y-2">
            <div class="p-2.5 rounded-xl bg-rose-50 border border-rose-100 flex justify-between items-center">
              <span class="text-rose-800 font-medium">จุดเสี่ยงสูงรวม (5 ด้าน):</span>
              <strong id="single-val-risk" class="text-rose-900 text-sm font-bold">185 จุด</strong>
            </div>

            <div class="p-2.5 rounded-xl bg-blue-50 border border-blue-100 flex justify-between items-center">
              <span class="text-blue-800 font-medium">งบประมาณที่ได้รับ:</span>
              <strong id="single-val-budget" class="text-blue-900 text-sm font-bold">558.60 ลบ.</strong>
            </div>

            <div class="p-2.5 rounded-xl bg-emerald-50 border border-emerald-100 flex justify-between items-center">
              <span class="text-emerald-800 font-medium">จำนวนโครงการรวม:</span>
              <strong id="single-val-proj" class="text-emerald-900 text-sm font-bold">103 โครงการ</strong>
            </div>
          </div>

          <!-- 5 Pillars Mini Grid -->
          <div class="mt-4">
            <div class="font-bold text-slate-700 mb-2">จุดเสี่ยงสูงแยกตาม 5 ด้าน:</div>
            <div class="grid grid-cols-5 gap-1 text-center" id="single-pillar-boxes">
              <div class="p-1.5 rounded bg-slate-50 border"><div class="text-[10px] text-slate-400">ด1</div><div id="sp-1" class="font-bold text-slate-800">0</div></div>
              <div class="p-1.5 rounded bg-slate-50 border"><div class="text-[10px] text-slate-400">ด2</div><div id="sp-2" class="font-bold text-slate-800">62</div></div>
              <div class="p-1.5 rounded bg-slate-50 border"><div class="text-[10px] text-slate-400">ด3</div><div id="sp-3" class="font-bold text-slate-800">0</div></div>
              <div class="p-1.5 rounded bg-slate-50 border"><div class="text-[10px] text-slate-400">ด4</div><div id="sp-4" class="font-bold text-slate-800">52</div></div>
              <div class="p-1.5 rounded bg-slate-50 border"><div class="text-[10px] text-slate-400">ด5</div><div id="sp-5" class="font-bold text-slate-800">71</div></div>
            </div>
          </div>
        </div>

        <div class="mt-4 pt-3 border-t border-slate-100 text-center text-slate-400 text-[11px]">
          คลิกที่อำเภออื่นบนแผนที่เพื่อดูข้อมูล
        </div>
      </div>
    </div>

  </main>

  <!-- ========================================================================= -->
  <!-- VIEW 3: SUMMARY TABLE & DOWNLOAD -->
  <!-- ========================================================================= -->
  <main id="view-summary" class="flex-1 max-w-7xl w-full mx-auto p-3 md:p-4 hidden flex flex-col space-y-3 text-xs">
    <div class="g-card p-4 flex items-center justify-between">
      <div>
        <h2 class="text-base font-bold text-slate-900">ตารางวิเคราะห์ช่องว่างรายอำเภอ (25 อำเภอในเชียงใหม่)</h2>
        <p class="text-slate-500 mt-0.5">เปรียบเทียบระดับความเสี่ยงกับงบประมาณที่ได้รับจัดสรร</p>
      </div>
      <a href="ChiangMai_Water_Risk_Budget_Dashboard.xlsx" download class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold shadow-sm transition flex items-center gap-1.5">
        <span>📥 ดาวน์โหลด Excel สะอาด (1.3 MB)</span>
      </a>
    </div>

    <div class="g-card overflow-hidden">
      <div class="overflow-x-auto max-h-[600px]">
        <table class="w-full text-left border-collapse">
          <thead class="sticky top-0 bg-slate-100 text-slate-700 border-b border-slate-200">
            <tr>
              <th class="p-2.5 font-bold">อำเภอ</th>
              <th class="p-2.5 font-bold text-center">หมู่บ้าน</th>
              <th class="p-2.5 font-bold text-center text-rose-600">เสี่ยงสูงรวม</th>
              <th class="p-2.5 font-bold">สถานะจัดสรร (Gap)</th>
              <th class="p-2.5 font-bold text-right">งบรวม (ลบ.)</th>
              <th class="p-2.5 font-bold text-right">โครงการ</th>
              <th class="p-2.5 font-bold text-center">ด1 อุปโภค</th>
              <th class="p-2.5 font-bold text-center">ด2 เกษตร</th>
              <th class="p-2.5 font-bold text-center">ด3 น้ำท่วม</th>
              <th class="p-2.5 font-bold text-center">ด4 คุณภาพ</th>
              <th class="p-2.5 font-bold text-center">ด5 ป่าต้นน้ำ</th>
            </tr>
          </thead>
          <tbody id="tbl-summary-body" class="divide-y divide-slate-100">
            <!-- Populated by JS -->
          </tbody>
        </table>
      </div>
    </div>
  </main>

  <!-- Logic Script -->
  <script>
    const geojsonData = __GEOJSON_DATA__;
    const statsData = __STATS_DATA__;

    function switchView(viewId) {
      document.querySelectorAll('main').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('g-btn-active');
        btn.classList.add('text-slate-600');
      });

      document.getElementById(viewId).classList.remove('hidden');
      const activeBtn = document.getElementById(viewId.replace('view-', 'btn-'));
      if (activeBtn) {
        activeBtn.classList.add('g-btn-active');
        activeBtn.classList.remove('text-slate-600');
      }

      setTimeout(() => {
        if (mapRisk) mapRisk.invalidateSize();
        if (mapBudget) mapBudget.invalidateSize();
        if (mapSingle) mapSingle.invalidateSize();
      }, 100);
    }

    const GOOGLE_STREETS = 'https://mt1.google.com/vt/lyrs=m&hl=th&x={x}&y={y}&z={z}';
    const GOOGLE_HYBRID = 'https://mt1.google.com/vt/lyrs=y&hl=th&x={x}&y={y}&z={z}';
    const GOOGLE_TERRAIN = 'https://mt1.google.com/vt/lyrs=p&hl=th&x={x}&y={y}&z={z}';

    const CHIANGMAI_CENTER = [18.7883, 98.9853];
    const DEFAULT_ZOOM = 8;

    function getSoftRiskColor(val, maxVal = 185) {
      const r = Math.min(val / maxVal, 1);
      return r > 0.75 ? '#b91c1c' :
             r > 0.50 ? '#ef4444' :
             r > 0.30 ? '#f87171' :
             r > 0.15 ? '#fca5a5' :
             r > 0    ? '#fee2e2' :
                        '#ffffff';
    }

    function getSoftBudgetColor(val, maxVal = 4836) {
      const r = Math.min(val / maxVal, 1);
      return r > 0.75 ? '#0369a1' :
             r > 0.50 ? '#0284c7' :
             r > 0.30 ? '#38bdf8' :
             r > 0.15 ? '#bae6fd' :
             r > 0    ? '#e0f2fe' :
                        '#ffffff';
    }

    let mapRisk, mapBudget, layerRisk, layerBudget, isSyncing = false;

    function initDualMaps() {
      mapRisk = L.map('map-risk', { zoomControl: true, attributionControl: false }).setView(CHIANGMAI_CENTER, DEFAULT_ZOOM);
      L.tileLayer(GOOGLE_STREETS, { maxZoom: 18 }).addTo(mapRisk);

      mapBudget = L.map('map-budget', { zoomControl: true, attributionControl: false }).setView(CHIANGMAI_CENTER, DEFAULT_ZOOM);
      L.tileLayer(GOOGLE_STREETS, { maxZoom: 18 }).addTo(mapBudget);

      mapRisk.on('move', () => {
        if (!isSyncing) {
          isSyncing = true;
          mapBudget.setView(mapRisk.getCenter(), mapRisk.getZoom(), { animate: false });
          isSyncing = false;
        }
      });
      mapBudget.on('move', () => {
        if (!isSyncing) {
          isSyncing = true;
          mapRisk.setView(mapBudget.getCenter(), mapBudget.getZoom(), { animate: false });
          isSyncing = false;
        }
      });

      renderDualLayers('all');
    }

    function renderDualLayers(pillarId) {
      if (layerRisk) mapRisk.removeLayer(layerRisk);
      if (layerBudget) mapBudget.removeLayer(layerBudget);

      const riskProp = pillarId === 'all' ? 'high_risk_total' : 'high_p' + pillarId;
      const budgetProp = pillarId === 'all' ? 'total_budget' : 'budget_p' + pillarId;

      const maxRisk = Math.max(...geojsonData.features.map(f => f.properties[riskProp] || 0), 1);
      const maxBudget = Math.max(...geojsonData.features.map(f => f.properties[budgetProp] || 0), 1);

      layerRisk = L.geoJSON(geojsonData, {
        style: (feature) => ({
          fillColor: getSoftRiskColor(feature.properties[riskProp] || 0, maxRisk),
          weight: 2,
          opacity: 1,
          color: '#ffffff',
          fillOpacity: 0.70
        }),
        onEachFeature: (feature, layer) => {
          const val = feature.properties[riskProp] || 0;
          layer.bindTooltip(`📍 อ.${feature.properties.amp_th} : ${val} จุด`, {
            permanent: true,
            direction: 'center',
            className: 'gmap-label'
          });

          layer.on('click', () => updateInspectorCard(feature.properties));
          layer.on('mouseover', () => highlightBoth(feature.properties.amp_th));
          layer.on('mouseout', () => resetBothHighlight());
        }
      }).addTo(mapRisk);

      layerBudget = L.geoJSON(geojsonData, {
        style: (feature) => ({
          fillColor: getSoftBudgetColor(feature.properties[budgetProp] || 0, maxBudget),
          weight: 2,
          opacity: 1,
          color: '#ffffff',
          fillOpacity: 0.70
        }),
        onEachFeature: (feature, layer) => {
          const bVal = (feature.properties[budgetProp] || 0).toLocaleString(undefined, {minimumFractionDigits: 1, maximumFractionDigits: 1});
          layer.bindTooltip(`📍 อ.${feature.properties.amp_th} : ${bVal} ลบ.`, {
            permanent: true,
            direction: 'center',
            className: 'gmap-label'
          });

          layer.on('click', () => updateInspectorCard(feature.properties));
          layer.on('mouseover', () => highlightBoth(feature.properties.amp_th));
          layer.on('mouseout', () => resetBothHighlight());
        }
      }).addTo(mapBudget);
    }

    function highlightBoth(ampName) {
      if (layerRisk) {
        layerRisk.eachLayer(l => {
          if (l.feature.properties.amp_th === ampName) {
            l.setStyle({ weight: 3, color: '#1a73e8', fillOpacity: 0.9 });
            l.bringToFront();
          }
        });
      }
      if (layerBudget) {
        layerBudget.eachLayer(l => {
          if (l.feature.properties.amp_th === ampName) {
            l.setStyle({ weight: 3, color: '#1a73e8', fillOpacity: 0.9 });
            l.bringToFront();
          }
        });
      }
    }

    function resetBothHighlight() {
      if (layerRisk) layerRisk.resetStyle();
      if (layerBudget) layerBudget.resetStyle();
    }

    function updateInspectorCard(p) {
      document.getElementById('ins-name').innerText = `อำเภอ${p.amp_th} (${p.villages} หมู่บ้าน)`;
      document.getElementById('ins-risk').innerText = `${p.high_risk_total} จุดเสี่ยงสูง`;
      document.getElementById('ins-budget').innerText = `${Number(p.total_budget).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})} ลบ. (${p.total_projects} โครงการ)`;
      document.getElementById('ins-gap').innerText = p.gap_status;
    }

    function filterPillar(pId) {
      document.querySelectorAll('.pillar-chip').forEach(c => {
        c.classList.remove('bg-blue-600', 'text-white', 'border-blue-600');
        c.classList.add('bg-white', 'text-slate-700', 'border-slate-300');
      });
      const activeChip = document.getElementById('chip-' + pId);
      if (activeChip) {
        activeChip.classList.add('bg-blue-600', 'text-white', 'border-blue-600');
        activeChip.classList.remove('bg-white', 'text-slate-700');
      }

      const pNames = {
        'all': 'รวม 5 ด้าน', '1': 'ด1 อุปโภค', '2': 'ด2 เกษตร/ผลิต', '3': 'ด3 น้ำท่วม', '4': 'ด4 คุณภาพน้ำ', '5': 'ด5 ป่าต้นน้ำ'
      };
      document.getElementById('txt-left-metric').innerText = `ความเสี่ยง (${pNames[pId]})`;
      document.getElementById('txt-right-metric').innerText = `งบประมาณ (${pNames[pId]})`;

      renderDualLayers(pId);
    }

    function resetDualMaps() {
      mapRisk.setView(CHIANGMAI_CENTER, DEFAULT_ZOOM);
      mapBudget.setView(CHIANGMAI_CENTER, DEFAULT_ZOOM);
    }

    let mapSingle, layerSingle, singleGoogleTile;

    function initSingleMap() {
      mapSingle = L.map('map-single', { attributionControl: false }).setView(CHIANGMAI_CENTER, DEFAULT_ZOOM);
      singleGoogleTile = L.tileLayer(GOOGLE_STREETS, { maxZoom: 18 }).addTo(mapSingle);
      updateSingleMap();
    }

    function setGoogleLayer(type) {
      document.getElementById('btn-layer-m').className = 'px-2.5 py-1 rounded bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium';
      document.getElementById('btn-layer-y').className = 'px-2.5 py-1 rounded bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium';
      document.getElementById('btn-layer-p').className = 'px-2.5 py-1 rounded bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium';
      
      let url = GOOGLE_STREETS;
      if (type === 'streets') {
        url = GOOGLE_STREETS;
        document.getElementById('btn-layer-m').className = 'px-2.5 py-1 rounded bg-blue-600 text-white font-semibold';
      } else if (type === 'hybrid') {
        url = GOOGLE_HYBRID;
        document.getElementById('btn-layer-y').className = 'px-2.5 py-1 rounded bg-blue-600 text-white font-semibold';
      } else if (type === 'terrain') {
        url = GOOGLE_TERRAIN;
        document.getElementById('btn-layer-p').className = 'px-2.5 py-1 rounded bg-blue-600 text-white font-semibold';
      }

      if (singleGoogleTile) mapSingle.removeLayer(singleGoogleTile);
      singleGoogleTile = L.tileLayer(url, { maxZoom: 18 }).addTo(mapSingle);
    }

    function updateSingleMap() {
      if (layerSingle) mapSingle.removeLayer(layerSingle);

      const metric = document.getElementById('single-metric').value;
      const isBudget = metric.includes('budget');
      const maxVal = Math.max(...geojsonData.features.map(f => f.properties[metric] || 0), 1);

      layerSingle = L.geoJSON(geojsonData, {
        style: (f) => {
          const val = f.properties[metric] || 0;
          return {
            fillColor: isBudget ? getSoftBudgetColor(val, maxVal) : getSoftRiskColor(val, maxVal),
            weight: 2,
            opacity: 1,
            color: '#ffffff',
            fillOpacity: 0.70
          };
        },
        onEachFeature: (feature, layer) => {
          const val = feature.properties[metric] || 0;
          const labelText = isBudget ? `${val.toLocaleString(undefined, {minimumFractionDigits: 1, maximumFractionDigits: 1})} ลบ.` : `${val} จุด`;
          
          layer.bindTooltip(`📍 อ.${feature.properties.amp_th} : ${labelText}`, {
            permanent: true,
            direction: 'center',
            className: 'gmap-label'
          });

          layer.on('click', () => populateSingleDrawer(feature.properties));
        }
      }).addTo(mapSingle);
    }

    function populateSingleDrawer(p) {
      document.getElementById('single-title').innerText = `อำเภอ${p.amp_th}`;
      document.getElementById('single-subtitle').innerText = `จังหวัดเชียงใหม่ • ${p.villages} หมู่บ้าน (พื้นที่ ${Number(p.area_sqkm).toFixed(1)} ตร.กม.)`;
      document.getElementById('single-badge-gap').innerText = p.gap_status;
      
      document.getElementById('single-val-risk').innerText = `${p.high_risk_total} จุด`;
      document.getElementById('single-val-budget').innerText = `${Number(p.total_budget).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})} ลบ.`;
      document.getElementById('single-val-proj').innerText = `${p.total_projects} โครงการ`;

      document.getElementById('sp-1').innerText = p.high_p1 || 0;
      document.getElementById('sp-2').innerText = p.high_p2 || 0;
      document.getElementById('sp-3').innerText = p.high_p3 || 0;
      document.getElementById('sp-4').innerText = p.high_p4 || 0;
      document.getElementById('sp-5').innerText = p.high_p5 || 0;
    }

    function searchDistrict() {
      const q = document.getElementById('gmap-search').value.trim().toLowerCase();
      if (!q) return;

      const feat = geojsonData.features.find(f => f.properties.amp_th.toLowerCase().includes(q));
      if (feat && layerSingle) {
        populateSingleDrawer(feat.properties);
        layerSingle.eachLayer(l => {
          if (l.feature.properties.amp_th === feat.properties.amp_th) {
            mapSingle.fitBounds(l.getBounds(), { maxZoom: 11, padding: [40, 40] });
            l.setStyle({ weight: 3, color: '#1a73e8', fillOpacity: 0.9 });
          }
        });
      }
    }

    function populateSummaryTable() {
      const tbody = document.getElementById('tbl-summary-body');
      let html = '';

      statsData.districts.forEach(d => {
        if (d['อำเภอ'] === 'โครงการระดับจังหวัด/ไม่ระบุอำเภอ') return;

        let badgeStyle = 'background:#dcfce7; color:#15803d; border:1px solid #bbf7d0';
        if (d['สถานะการจัดสรร (Gap Status)'].includes('วิกฤติ')) badgeStyle = 'background:#fee2e2; color:#b91c1c; border:1px solid #fca5a5; font-weight:bold';
        else if (d['สถานะการจัดสรร (Gap Status)'].includes('เสี่ยงสูง') || d['สถานะการจัดสรร (Gap Status)'].includes('ควรเพิ่ม')) badgeStyle = 'background:#fef3c7; color:#b45309; border:1px solid #fde68a';

        html += `
          <tr class="hover:bg-slate-50 transition">
            <td class="p-2.5 font-bold text-slate-900">${d['อำเภอ']}</td>
            <td class="p-2.5 text-center text-slate-600">${d['จำนวนหมู่บ้าน']}</td>
            <td class="p-2.5 text-center font-bold text-rose-600 bg-rose-50/50">${d['จำนวนเสี่ยงสูง_รวมทุกด้าน']}</td>
            <td class="p-2.5"><span class="px-2.5 py-0.5 rounded-full text-[10px]" style="${badgeStyle}">${d['สถานะการจัดสรร (Gap Status)']}</span></td>
            <td class="p-2.5 text-right font-bold text-slate-900">${Number(d['งบประมาณรวม (ล้านบาท)']).toLocaleString(undefined, {minimumFractionDigits: 1, maximumFractionDigits: 1})}</td>
            <td class="p-2.5 text-right font-medium">${d['จำนวนโครงการรวม']}</td>
            <td class="p-2.5 text-center">${d['เสี่ยงสูง_ด1_อุปโภค'] > 0 ? '<strong class="text-rose-600">' + d['เสี่ยงสูง_ด1_อุปโภค'] + '</strong>' : '-'}</td>
            <td class="p-2.5 text-center">${d['เสี่ยงสูง_ด2_เกษตร'] > 0 ? '<strong class="text-rose-600">' + d['เสี่ยงสูง_ด2_เกษตร'] + '</strong>' : '-'}</td>
            <td class="p-2.5 text-center">${d['เสี่ยงสูง_ด3_น้ำท่วม'] > 0 ? '<strong class="text-rose-600">' + d['เสี่ยงสูง_ด3_น้ำท่วม'] + '</strong>' : '-'}</td>
            <td class="p-2.5 text-center">${d['เสี่ยงสูง_ด4_คุณภาพน้ำ'] > 0 ? '<strong class="text-rose-600">' + d['เสี่ยงสูง_ด4_คุณภาพน้ำ'] + '</strong>' : '-'}</td>
            <td class="p-2.5 text-center">${d['เสี่ยงสูง_ด5_ป่าต้นน้ำ'] > 0 ? '<strong class="text-rose-600">' + d['เสี่ยงสูง_ด5_ป่าต้นน้ำ'] + '</strong>' : '-'}</td>
          </tr>
        `;
      });

      tbody.innerHTML = html;
    }

    window.addEventListener('DOMContentLoaded', () => {
      initDualMaps();
      initSingleMap();
      populateSummaryTable();
    });
  </script>
</body>
</html>"""

full_water_html = html_water_template.replace('__GEOJSON_DATA__', geojson_str).replace('__STATS_DATA__', stats_str)
with open('ChiangMai_Water_GIS_Dashboard.html', 'w', encoding='utf-8') as f:
    f.write(full_water_html)

with open('/Users/commindo/.gemini/antigravity/brain/e2040493-6043-4283-af0a-d3d6adad8d8d/water_gis_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(full_water_html)

# -----------------------------------------------------------------------------
# 2. BUILD HOUSEHOLD POINT GIS DASHBOARD (GOOGLE MAPS STYLE)
# -----------------------------------------------------------------------------
with open('chiangmai_flood_households_gis.geojson', 'r', encoding='utf-8') as f:
    geo_hh = json.load(f)

geo_hh_str = json.dumps(geo_hh, ensure_ascii=False)

html_hh_template = """<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Google Maps พิกัดบ้านผู้ประสบภัยน้ำท่วม 2567 (เชียงใหม่)</title>
  
  <!-- Tailwind CSS -->
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  
  <!-- Leaflet CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  
  <!-- Leaflet MarkerCluster -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" />
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" />
  <script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>

  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@400;500;600;700&family=Sarabun:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <style>
    body { font-family: 'Prompt', 'Sarabun', -apple-system, BlinkMacSystemFont, sans-serif; background-color: #f8f9fa; }
    .map-frame { height: calc(100vh - 145px); min-height: 520px; border-radius: 16px; }
    .map-frame-dual { height: calc(100vh - 180px); min-height: 480px; border-radius: 16px; }
    
    .g-card {
      background: #ffffff;
      border: 1px solid #e8eaed;
      border-radius: 16px;
      box-shadow: 0 1px 3px rgba(60,64,67,0.12), 0 4px 8px rgba(60,64,67,0.06);
    }
    .g-btn-active {
      background-color: #1a73e8 !important;
      color: #ffffff !important;
      box-shadow: 0 1px 3px rgba(26,115,232,0.3) !important;
    }
  </style>
</head>
<body class="antialiased text-slate-800 flex flex-col min-h-screen">

  <!-- Header -->
  <nav class="bg-white border-b border-slate-200 sticky top-0 z-50 px-4 py-2.5 shadow-sm">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-3">
      
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-full bg-rose-50 border border-rose-200 flex items-center justify-center text-rose-600 text-lg shadow-sm">
          🏠
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-base font-bold text-slate-900 leading-tight">Google Maps พิกัดบ้านผู้ประสบภัยน้ำท่วม 2567</h1>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-rose-100 text-rose-800">4,450 หลังคาเรือน</span>
          </div>
          <p class="text-xs text-slate-500">ทต.หนองหอย • ทน.เชียงใหม่ • ทต.ท่าวังตาล • ทต.หนองผึ้ง</p>
        </div>
      </div>

      <!-- Navigation Tabs -->
      <div class="flex items-center bg-slate-100 p-1 rounded-full border border-slate-200 overflow-x-auto text-xs">
        <button onclick="switchView('view-map')" id="btn-map" class="nav-btn px-4 py-1.5 rounded-full font-semibold transition g-btn-active">
          📍 แผนที่พิกัดบ้าน (Google Maps)
        </button>
        <button onclick="switchView('view-dual')" id="btn-dual" class="nav-btn px-4 py-1.5 rounded-full font-semibold transition text-slate-600 hover:text-slate-900">
          🔄 แผนที่คู่ (กลุ่มเปราะบาง vs ความเสียหาย)
        </button>
        <button onclick="switchView('view-summary')" id="btn-summary" class="nav-btn px-4 py-1.5 rounded-full font-semibold transition text-slate-600 hover:text-slate-900">
          📊 สรุป 4 เทศบาล & ดาวน์โหลด
        </button>
      </div>

    </div>
  </nav>

  <!-- ========================================================================= -->
  <!-- VIEW 1: SINGLE HOUSEHOLD POINT MAP WITH GOOGLE STREETS -->
  <!-- ========================================================================= -->
  <main id="view-map" class="flex-1 max-w-7xl w-full mx-auto p-3 md:p-4 flex flex-col space-y-3">
    
    <!-- Controls Bar -->
    <div class="g-card p-3 flex flex-col lg:flex-row lg:items-center justify-between gap-3 text-xs">
      
      <div class="flex flex-wrap items-center gap-2">
        <input type="text" id="hh-search" oninput="filterPoints()" placeholder="🔍 ค้นหาบ้านเลขที่ / ชื่อ / ชุมชน..." class="px-3 py-1.5 border border-slate-300 rounded-lg w-60 focus:ring-2 focus:ring-blue-500 outline-none">
        
        <select id="hh-muni" onchange="filterPoints()" class="px-3 py-1.5 font-semibold bg-slate-50 border border-slate-300 rounded-lg outline-none">
          <option value="all">🏢 ทุกเทศบาล (4,450 หลัง)</option>
          <option value="ท่าวังตาล">ทต.ท่าวังตาล (2,230 หลัง)</option>
          <option value="หนองหอย">ทต.หนองหอย (957 หลัง)</option>
          <option value="นครเชียงใหม่">ทน.เชียงใหม่ (771 หลัง)</option>
          <option value="หนองผึ้ง">ทต.หนองผึ้ง (492 หลัง)</option>
        </select>

        <select id="hh-vuln" onchange="filterPoints()" class="px-3 py-1.5 font-semibold bg-slate-50 border border-slate-300 rounded-lg outline-none">
          <option value="all">⚡ ทุกสถานะกลุ่มเปราะบาง</option>
          <option value="bedridden">🚨 ผู้ป่วยติดเตียง / คนพิการ</option>
          <option value="elderly">👴 มีผู้สูงอายุในบ้าน</option>
          <option value="deep_water">🌊 น้ำท่วมสูง (> 1.2 เมตร)</option>
          <option value="critical">🚨 วิกฤติด่วนที่สุด</option>
        </select>

        <button onclick="resetFilters()" class="px-2.5 py-1.5 rounded-lg border border-slate-300 bg-white hover:bg-slate-50 font-medium">รีเซ็ต</button>
      </div>

      <!-- Quick Stats Counter -->
      <div class="flex items-center gap-2">
        <span class="text-slate-500">แสดงผล:</span>
        <strong id="hh-counter" class="text-blue-600 font-bold text-sm">4,450 หลังคาเรือน</strong>
      </div>

    </div>

    <!-- Map & Google Detail Panel -->
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-3 flex-1">
      <div class="lg:col-span-3 g-card overflow-hidden relative">
        <div id="map-point" class="map-frame w-full"></div>
      </div>

      <!-- Google Place Style Household Drawer -->
      <div class="lg:col-span-1 g-card p-4 flex flex-col justify-between overflow-y-auto max-h-[600px] text-xs">
        <div>
          <div class="flex items-center justify-between pb-3 border-b border-slate-100">
            <span class="text-[10px] font-bold text-slate-400 uppercase">ข้อมูลหลังคาเรือน</span>
            <span id="dossier-urgency" class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-700">-</span>
          </div>

          <div class="mt-3">
            <span id="dossier-code" class="text-blue-600 font-bold text-xs">คลิกที่หมุดบ้านบนแผนที่</span>
            <h2 id="dossier-name" class="text-lg font-bold text-slate-900 mt-0.5">เลือกหลังคาเรือนเพื่อดูข้อมูล</h2>
            <p id="dossier-address" class="text-slate-500 mt-0.5">-</p>
          </div>

          <!-- Cards -->
          <div class="mt-4 space-y-2">
            <div class="p-2.5 rounded-xl bg-rose-50 border border-rose-100">
              <div class="text-rose-800 font-bold mb-1">🌊 ระดับน้ำและผลกระทบ</div>
              <div class="flex justify-between text-slate-700">
                <span>ระดับน้ำท่วม:</span>
                <strong id="dossier-depth" class="text-rose-900 font-bold">-</strong>
              </div>
              <div class="flex justify-between text-slate-700 mt-0.5">
                <span>การตัดสินใจ:</span>
                <strong id="dossier-decision">-</strong>
              </div>
            </div>

            <div class="p-2.5 rounded-xl bg-amber-50 border border-amber-100">
              <div class="text-amber-800 font-bold mb-1">🚨 กลุ่มเปราะบางในบ้าน</div>
              <div class="flex justify-between text-slate-700">
                <span>ผู้ป่วยติดเตียง:</span>
                <strong id="dossier-bedridden" class="text-amber-900 font-bold">-</strong>
              </div>
              <div class="flex justify-between text-slate-700 mt-0.5">
                <span>ผู้สูงอายุ:</span>
                <strong id="dossier-elderly">-</strong>
              </div>
              <div class="flex justify-between text-slate-700 mt-0.5">
                <span>คนพิการ:</span>
                <strong id="dossier-disabled">-</strong>
              </div>
            </div>

            <div class="p-2.5 rounded-xl bg-emerald-50 border border-emerald-100">
              <div class="text-emerald-800 font-bold mb-1">💰 มูลค่าความเสียหาย</div>
              <div class="flex justify-between text-slate-700">
                <span>เสียหายรวม:</span>
                <strong id="dossier-damage" class="text-emerald-900 font-bold text-sm">-</strong>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-4 pt-3 border-t border-slate-100 text-center">
          <span class="text-slate-500 text-[11px]">📞 เบอร์ติดต่อฉุกเฉิน:</span>
          <div id="dossier-phone" class="text-sm font-bold text-slate-900 mt-0.5">-</div>
        </div>
      </div>
    </div>

  </main>

  <!-- ========================================================================= -->
  <!-- VIEW 2: DUAL SYNCED MAP (เปรียบเทียบ 2 แผนที่) -->
  <!-- ========================================================================= -->
  <main id="view-dual" class="flex-1 max-w-7xl w-full mx-auto p-3 md:p-4 hidden flex flex-col space-y-3">
    <div class="g-card p-3 flex items-center justify-between text-xs">
      <div class="flex items-center gap-2">
        <span class="text-base">⚖️</span>
        <span class="font-bold text-slate-800">เปรียบเทียบเชิงพื้นที่: ซ้าย (ตำแหน่งกลุ่มเปราะบาง) vs ขวา (มูลค่าความเสียหาย)</span>
      </div>
      <span class="text-slate-500">ซูมหรือเลื่อนแผนที่ทั้ง 2 ฝั่งจะขยับตามกันอัตโนมัติบน Google Maps</span>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-3 flex-1">
      <div class="g-card overflow-hidden flex flex-col">
        <div class="px-4 py-2 bg-rose-50 border-b border-rose-100 text-xs font-bold text-rose-950 flex justify-between">
          <span>1. แผนที่ตำแหน่งกลุ่มเปราะบาง (แดง=ติดเตียง/พิการ, ส้ม=คนชรา, ฟ้า=ทั่วไป)</span>
        </div>
        <div id="map-dual-left" class="map-frame-dual flex-1"></div>
      </div>

      <div class="g-card overflow-hidden flex flex-col">
        <div class="px-4 py-2 bg-emerald-50 border-b border-emerald-100 text-xs font-bold text-emerald-950 flex justify-between">
          <span>2. แผนที่มูลค่าความเสียหาย (ขนาดหมุดแปรผันตามจำนวนเงิน)</span>
        </div>
        <div id="map-dual-right" class="map-frame-dual flex-1"></div>
      </div>
    </div>
  </main>

  <!-- ========================================================================= -->
  <!-- VIEW 3: SUMMARY & EXPORT -->
  <!-- ========================================================================= -->
  <main id="view-summary" class="flex-1 max-w-7xl w-full mx-auto p-3 md:p-4 hidden flex flex-col space-y-4 text-xs">
    <div class="g-card p-4 flex items-center justify-between">
      <div>
        <h2 class="text-base font-bold text-slate-900">สรุปผลสำรวจน้ำท่วม 2567 รายเทศบาล (4,450 ครัวเรือน)</h2>
        <p class="text-slate-500 mt-0.5">ดาวน์โหลดข้อมูลฉบับสมบูรณ์สำหรับ Google Sheets หรือโปรแกรม GIS</p>
      </div>
      <a href="ChiangMai_Flood_Household_Survey_Dashboard.xlsx" download class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold shadow-sm transition flex items-center gap-1.5">
        <span>📥 ดาวน์โหลด Excel สำรวจครัวเรือน (1.1 MB)</span>
      </a>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-4 gap-3">
      <div class="g-card p-4">
        <div class="font-bold text-blue-600">ทต.ท่าวังตาล (อ.สารภี)</div>
        <div class="text-xl font-bold text-slate-900 mt-1">2,230 ครัวเรือน</div>
        <div class="text-slate-500 mt-1">เสียหาย 172.93 ลบ. (เฉลี่ย 77,547 บ.)</div>
      </div>
      <div class="g-card p-4">
        <div class="font-bold text-emerald-600">ทต.หนองหอย (อ.เมือง)</div>
        <div class="text-xl font-bold text-slate-900 mt-1">957 ครัวเรือน</div>
        <div class="text-slate-500 mt-1">เสียหาย 68.27 ลบ. (เฉลี่ย 71,338 บ.)</div>
      </div>
      <div class="g-card p-4">
        <div class="font-bold text-purple-600">ทน.เชียงใหม่ (อ.เมือง)</div>
        <div class="text-xl font-bold text-slate-900 mt-1">771 ครัวเรือน</div>
        <div class="text-slate-500 mt-1">เสียหาย 52.12 ลบ. (เฉลี่ย 67,601 บ.)</div>
      </div>
      <div class="g-card p-4">
        <div class="font-bold text-amber-600">ทต.หนองผึ้ง (อ.สารภี)</div>
        <div class="text-xl font-bold text-slate-900 mt-1">492 ครัวเรือน</div>
        <div class="text-slate-500 mt-1">เสียหาย 35.16 ลบ. (น้ำท่วมลึก 1.82 ม.)</div>
      </div>
    </div>
  </main>

  <!-- Script Logic -->
  <script>
    const geojsonData = __GEOJSON_DATA__;

    function switchView(viewId) {
      document.querySelectorAll('main').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('g-btn-active');
        btn.classList.add('text-slate-600');
      });

      document.getElementById(viewId).classList.remove('hidden');
      const activeBtn = document.getElementById(viewId.replace('view-', 'btn-'));
      if (activeBtn) {
        activeBtn.classList.add('g-btn-active');
        activeBtn.classList.remove('text-slate-600');
      }

      setTimeout(() => {
        if (mapPoint) mapPoint.invalidateSize();
        if (mapDualLeft) mapDualLeft.invalidateSize();
        if (mapDualRight) mapDualRight.invalidateSize();
      }, 100);
    }

    const GOOGLE_STREETS = 'https://mt1.google.com/vt/lyrs=m&hl=th&x={x}&y={y}&z={z}';
    const CENTER_COORD = [18.7500, 99.0050];

    let mapPoint, clusterGroup;
    let mapDualLeft, mapDualRight, isDualSyncing = false;

    function initPointMap() {
      mapPoint = L.map('map-point').setView(CENTER_COORD, 12);
      L.tileLayer(GOOGLE_STREETS, { maxZoom: 18 }).addTo(mapPoint);

      clusterGroup = L.markerClusterGroup({
        chunkedLoading: true,
        maxClusterRadius: 35,
        spiderfyOnMaxZoom: true
      });

      renderMarkers(geojsonData.features);
      mapPoint.addLayer(clusterGroup);
    }

    function getMarkerColor(p) {
      if (p.bedridden > 0 || p.disabled > 0) return '#dc2626'; // Red
      if (p.elderly > 0) return '#f59e0b'; // Amber
      if (p.depth_m >= 1.2) return '#ea580c'; // Orange
      return '#2563eb'; // Blue
    }

    function renderMarkers(featuresList) {
      clusterGroup.clearLayers();
      
      featuresList.forEach(f => {
        const p = f.properties;
        const color = getMarkerColor(p);
        
        const marker = L.circleMarker([f.geometry.coordinates[1], f.geometry.coordinates[0]], {
          radius: 6,
          fillColor: color,
          color: '#ffffff',
          weight: 1.5,
          opacity: 1,
          fillOpacity: 0.9
        });

        marker.bindTooltip(`📍 <strong>${p.name}</strong> (${p.id})<br>บ้านเลขที่: ${p.house_no} ม.${p.village}<br>น้ำท่วม: ${p.depth_lvl}`, {
          direction: 'top'
        });

        marker.on('click', () => populateDossier(p));
        clusterGroup.addLayer(marker);
      });

      document.getElementById('hh-counter').innerText = `${featuresList.length.toLocaleString()} หลังคาเรือน`;
    }

    function populateDossier(p) {
      document.getElementById('dossier-code').innerText = `${p.id} • ${p.muni}`;
      document.getElementById('dossier-name').innerText = p.name;
      document.getElementById('dossier-address').innerText = `บ้านเลขที่ ${p.house_no} หมู่ ${p.village} ต.${p.subdist} อ.${p.dist}`;
      document.getElementById('dossier-urgency').innerText = p.urgency.split(' ')[0] + ' ' + (p.urgency.includes('วิกฤติ') ? 'วิกฤติ' : 'เฝ้าระวัง');
      
      document.getElementById('dossier-depth').innerText = `${p.depth_m > 0 ? p.depth_m + ' ม. ' : ''}(${p.depth_lvl})`;
      document.getElementById('dossier-decision').innerText = p.decision;
      
      document.getElementById('dossier-bedridden').innerText = `${p.bedridden} คน`;
      document.getElementById('dossier-elderly').innerText = `${p.elderly} คน`;
      document.getElementById('dossier-disabled').innerText = `${p.disabled} คน`;
      
      document.getElementById('dossier-damage').innerText = `${Number(p.damage_thb).toLocaleString()} บาท`;
      document.getElementById('dossier-phone').innerText = p.phone || '-';
    }

    function filterPoints() {
      const q = document.getElementById('hh-search').value.trim().toLowerCase();
      const muni = document.getElementById('hh-muni').value;
      const vuln = document.getElementById('hh-vuln').value;

      const filtered = geojsonData.features.filter(f => {
        const p = f.properties;
        const matchSearch = !q || p.name.toLowerCase().includes(q) || p.house_no.toLowerCase().includes(q) || p.id.toLowerCase().includes(q) || p.village.toLowerCase().includes(q);
        const matchMuni = (muni === 'all') || p.muni.includes(muni);
        
        let matchVuln = true;
        if (vuln === 'bedridden') matchVuln = (p.bedridden > 0 || p.disabled > 0);
        else if (vuln === 'elderly') matchVuln = (p.elderly > 0);
        else if (vuln === 'deep_water') matchVuln = (p.depth_m >= 1.2 || p.depth_lvl.includes('อก') || p.depth_lvl.includes('มิด'));
        else if (vuln === 'critical') matchVuln = p.urgency.includes('วิกฤติ');

        return matchSearch && matchMuni && matchVuln;
      });

      renderMarkers(filtered);
    }

    function resetFilters() {
      document.getElementById('hh-search').value = '';
      document.getElementById('hh-muni').value = 'all';
      document.getElementById('hh-vuln').value = 'all';
      renderMarkers(geojsonData.features);
    }

    function initDualMaps() {
      mapDualLeft = L.map('map-dual-left', { zoomControl: true, attributionControl: false }).setView(CENTER_COORD, 12);
      L.tileLayer(GOOGLE_STREETS, { maxZoom: 18 }).addTo(mapDualLeft);

      mapDualRight = L.map('map-dual-right', { zoomControl: true, attributionControl: false }).setView(CENTER_COORD, 12);
      L.tileLayer(GOOGLE_STREETS, { maxZoom: 18 }).addTo(mapDualRight);

      mapDualLeft.on('move', () => {
        if (!isDualSyncing) {
          isDualSyncing = true;
          mapDualRight.setView(mapDualLeft.getCenter(), mapDualLeft.getZoom(), { animate: false });
          isDualSyncing = false;
        }
      });
      mapDualRight.on('move', () => {
        if (!isDualSyncing) {
          isDualSyncing = true;
          mapDualLeft.setView(mapDualRight.getCenter(), mapDualRight.getZoom(), { animate: false });
          isDualSyncing = false;
        }
      });

      geojsonData.features.forEach(f => {
        const p = f.properties;
        L.circleMarker([f.geometry.coordinates[1], f.geometry.coordinates[0]], {
          radius: 5,
          fillColor: getMarkerColor(p),
          color: '#ffffff',
          weight: 1,
          fillOpacity: 0.85
        }).bindTooltip(`${p.name}<br>${p.urgency}`).addTo(mapDualLeft);

        const radius = Math.min(Math.max(Math.sqrt(p.damage_thb) / 40, 4), 18);
        L.circleMarker([f.geometry.coordinates[1], f.geometry.coordinates[0]], {
          radius: radius,
          fillColor: '#059669',
          color: '#ffffff',
          weight: 1,
          fillOpacity: 0.75
        }).bindTooltip(`${p.name}<br>เสียหาย: ${Number(p.damage_thb).toLocaleString()} บาท`).addTo(mapDualRight);
      });
    }

    window.addEventListener('DOMContentLoaded', () => {
      initPointMap();
      initDualMaps();
    });
  </script>
</body>
</html>"""

full_hh_html = html_hh_template.replace('__GEOJSON_DATA__', geo_hh_str)
with open('ChiangMai_Flood_Household_GIS_Dashboard.html', 'w', encoding='utf-8') as f:
    f.write(full_hh_html)

with open('/Users/commindo/.gemini/antigravity/brain/e2040493-6043-4283-af0a-d3d6adad8d8d/flood_household_gis_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(full_hh_html)

print("Both Google Maps styled Dashboards generated successfully!")
