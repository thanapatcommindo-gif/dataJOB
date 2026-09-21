import json

# Load merged GeoJSON
with open('chiangmai_districts_gis.geojson', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# Load summary stats
with open('dashboard_data.json', 'r', encoding='utf-8') as f:
    stats_data = json.load(f)

geojson_str = json.dumps(geojson_data, ensure_ascii=False)
stats_str = json.dumps(stats_data, ensure_ascii=False)

html_template = """<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ระบบสารสนเทศภูมิศาสตร์ (GIS) และแดชบอร์ดเปรียบเทียบแผนน้ำเชียงใหม่</title>
  
  <!-- Tailwind CSS -->
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  
  <!-- Leaflet CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  
  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  
  <style>
    body { font-family: 'Sarabun', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
    .leaflet-container { background: #f8fafc; font-family: inherit; }
    .map-container { height: calc(100vh - 210px); min-height: 520px; }
    .map-container-dual { height: calc(100vh - 250px); min-height: 500px; }
    
    /* Custom Scrollbars */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

    /* Custom Tooltip */
    .leaflet-tooltip-custom {
      background: rgba(15, 23, 42, 0.92) !important;
      color: #ffffff !important;
      border: none !important;
      border-radius: 8px !important;
      padding: 8px 12px !important;
      font-size: 12px !important;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3) !important;
      font-family: 'Sarabun', sans-serif !important;
    }
    .leaflet-tooltip-custom:before {
      border-top-color: rgba(15, 23, 42, 0.92) !important;
    }
  </style>
</head>
<body class="bg-slate-100 text-slate-800 antialiased min-h-screen flex flex-col">

  <!-- Top Navigation Header -->
  <header class="bg-slate-900 text-white border-b border-slate-800 sticky top-0 z-50 shadow-md">
    <div class="max-w-7xl mx-auto px-4 py-3 flex flex-col md:flex-row md:items-center justify-between gap-3">
      
      <!-- Brand & Title -->
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-cyan-400 flex items-center justify-center text-xl shadow-inner">
          🗺️
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="font-bold text-lg text-white tracking-wide">ระบบแผนที่ GIS บริหารจัดการทรัพยากรน้ำ เชียงใหม่</h1>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-blue-500/20 text-blue-300 border border-blue-400/30">GIS Interactive 2.0</span>
          </div>
          <p class="text-xs text-slate-400">เปรียบเทียบระดับความเสี่ยง 5 ด้าน vs งบประมาณที่ได้รับจัดสรร 65-70 (35,094.77 ล้านบาท)</p>
        </div>
      </div>

      <!-- Navigation Tabs -->
      <div class="flex items-center bg-slate-800/90 p-1 rounded-xl border border-slate-700/60 overflow-x-auto">
        <button onclick="navigateView('view-compare')" id="nav-btn-compare" class="nav-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-2 transition bg-blue-600 text-white shadow">
          <span>🔄 GIS เปรียบเทียบ 2 แผนที่ (Side-by-Side)</span>
        </button>
        <button onclick="navigateView('view-explorer')" id="nav-btn-explorer" class="nav-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-2 transition text-slate-400 hover:text-white hover:bg-slate-700/50">
          <span>🔍 GIS สำรวจเชิงลึก (Single Map)</span>
        </button>
        <button onclick="navigateView('view-table')" id="nav-btn-table" class="nav-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-2 transition text-slate-400 hover:text-white hover:bg-slate-700/50">
          <span>📊 สรุปตารางวิเคราะห์ & Export</span>
        </button>
      </div>

    </div>
  </header>

  <!-- ========================================================================= -->
  <!-- VIEW 1: DUAL SYNCED GIS COMPARISON (หน้า GIS เปรียบเทียบสองฝั่ง) -->
  <!-- ========================================================================= -->
  <section id="view-compare" class="flex-1 max-w-7xl w-full mx-auto p-4 flex flex-col space-y-3">
    
    <!-- Comparison Control Bar -->
    <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex flex-col lg:flex-row lg:items-center justify-between gap-4">
      
      <div class="flex items-center gap-3">
        <span class="text-xl">⚖️</span>
        <div>
          <h2 class="font-bold text-slate-900 text-sm md:text-base">โหมดเปรียบเทียบเชิงภูมิสารสนเทศ (Dual Synchronized GIS)</h2>
          <p class="text-xs text-slate-500">ซูมหรือเลื่อนแผนที่ฝั่งใดฝั่งหนึ่ง ทั้งสองแผนที่จะขยับตามกันแบบ Real-time พร้อมชี้เป้าความไม่สอดคล้อง</p>
        </div>
      </div>

      <!-- Pillar Filter for Both Maps -->
      <div class="flex flex-wrap items-center gap-2">
        <label class="text-xs font-bold text-slate-600">กรองด้านแผนแม่บท:</label>
        <select id="dual-pillar-select" onchange="updateDualMaps()" class="px-3 py-1.5 text-xs font-semibold bg-slate-50 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
          <option value="all">🌟 รวม 5 ด้านแผนแม่บท</option>
          <option value="1">ด1: การจัดการน้ำอุปโภคบริโภค</option>
          <option value="2">ด2: การสร้างความมั่นคงน้ำภาคการผลิต (เกษตร)</option>
          <option value="3">ด3: การจัดการน้ำท่วมและอุทกภัย</option>
          <option value="4">ด4: การจัดการคุณภาพน้ำและอนุรักษ์</option>
          <option value="5">ด5: การฟื้นฟูป่าต้นน้ำและชะล้างดิน</option>
        </select>

        <button onclick="resetDualView()" class="px-3 py-1.5 text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg border border-slate-300 transition font-medium">
          🎯 รีเซ็ตมุมมอง
        </button>
      </div>

    </div>

    <!-- Active Hover / Inspector Diff Card -->
    <div id="dual-inspector-card" class="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 text-white p-3.5 rounded-xl shadow flex flex-col md:flex-row md:items-center justify-between gap-3">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 rounded-lg bg-white/10 flex items-center justify-center text-lg">📌</div>
        <div>
          <span class="text-xs text-blue-300">คลิกหรือวางเมาส์บนอำเภอเพื่อเปรียบเทียบ:</span>
          <div id="dual-ins-title" class="font-bold text-base text-white">ชี้เป้าที่อำเภอ (ตัวอย่าง: อ.สารภี vs อ.แม่แตง)</div>
        </div>
      </div>
      <div id="dual-ins-metrics" class="flex flex-wrap items-center gap-4 text-xs">
        <div class="bg-rose-500/20 border border-rose-400/40 px-3 py-1.5 rounded-lg">
          <span class="text-rose-200">จุดเสี่ยงสูง:</span> <strong id="dual-ins-risk" class="text-white text-sm">185 จุด (อันดับ 1)</strong>
        </div>
        <div class="bg-emerald-500/20 border border-emerald-400/40 px-3 py-1.5 rounded-lg">
          <span class="text-emerald-200">งบประมาณจัดสรร:</span> <strong id="dual-ins-budget" class="text-white text-sm">558.60 ลบ. (อันดับ 20)</strong>
        </div>
        <div class="bg-amber-500/20 border border-amber-400/40 px-3 py-1.5 rounded-lg">
          <span class="text-amber-200">สถานะ Gap:</span> <strong id="dual-ins-gap" class="text-amber-300 text-sm">🚨 เสี่ยงสูงแต่งบน้อย</strong>
        </div>
      </div>
    </div>

    <!-- Dual Map Canvas Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 flex-1">
      
      <!-- LEFT MAP: RISK MAP -->
      <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden flex flex-col relative">
        <!-- Map Header -->
        <div class="px-4 py-2.5 bg-gradient-to-r from-rose-50 to-orange-50 border-b border-rose-100 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-3 h-3 rounded-full bg-rose-500 animate-pulse"></span>
            <span class="font-bold text-xs md:text-sm text-rose-950">1. แผนที่ระดับความเสี่ยง (Risk Map)</span>
          </div>
          <span id="label-left-metric" class="text-[11px] font-semibold text-rose-800 bg-rose-200/60 px-2 py-0.5 rounded">
            จุดเสี่ยงสูงรวม (2,200 หมู่บ้าน)
          </span>
        </div>
        <!-- Leaflet Map Div -->
        <div id="map-risk" class="map-container-dual flex-1"></div>
        <!-- Bottom Legend -->
        <div class="p-2.5 bg-slate-50 border-t border-slate-200 flex items-center justify-between text-[11px] text-slate-600">
          <span>ความเสี่ยงต่ำ (0-10 จุด)</span>
          <div class="flex items-center gap-1">
            <span class="w-4 h-3 bg-[#fef0d9] rounded-sm"></span>
            <span class="w-4 h-3 bg-[#fdd49e] rounded-sm"></span>
            <span class="w-4 h-3 bg-[#fdbb84] rounded-sm"></span>
            <span class="w-4 h-3 bg-[#fc8d59] rounded-sm"></span>
            <span class="w-4 h-3 bg-[#e34a33] rounded-sm"></span>
            <span class="w-4 h-3 bg-[#b30000] rounded-sm"></span>
          </div>
          <span class="font-bold text-rose-700">วิกฤติสูงสุด (180+ จุด)</span>
        </div>
      </div>

      <!-- RIGHT MAP: BUDGET MAP -->
      <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden flex flex-col relative">
        <!-- Map Header -->
        <div class="px-4 py-2.5 bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-blue-100 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-3 h-3 rounded-full bg-blue-600"></span>
            <span class="font-bold text-xs md:text-sm text-blue-950">2. แผนที่การจัดสรรงบประมาณ (Budget Map)</span>
          </div>
          <span id="label-right-metric" class="text-[11px] font-semibold text-blue-800 bg-blue-200/60 px-2 py-0.5 rounded">
            งบประมาณรวม (ล้านบาท)
          </span>
        </div>
        <!-- Leaflet Map Div -->
        <div id="map-budget" class="map-container-dual flex-1"></div>
        <!-- Bottom Legend -->
        <div class="p-2.5 bg-slate-50 border-t border-slate-200 flex items-center justify-between text-[11px] text-slate-600">
          <span>งบน้อย (<300 ลบ.)</span>
          <div class="flex items-center gap-1">
            <span class="w-4 h-3 bg-[#f1eef6] rounded-sm"></span>
            <span class="w-4 h-3 bg-[#d0d1e6] rounded-sm"></span>
            <span class="w-4 h-3 bg-[#a6bddb] rounded-sm"></span>
            <span class="w-4 h-3 bg-[#67a9cf] rounded-sm"></span>
            <span class="w-4 h-3 bg-[#1c9099] rounded-sm"></span>
            <span class="w-4 h-3 bg-[#016c59] rounded-sm"></span>
          </div>
          <span class="font-bold text-emerald-800">งบสูงสุด (4,000+ ลบ.)</span>
        </div>
      </div>

    </div>

  </section>

  <!-- ========================================================================= -->
  <!-- VIEW 2: SINGLE GIS EXPLORER (หน้าสำรวจเชิงลึก) -->
  <!-- ========================================================================= -->
  <section id="view-explorer" class="flex-1 max-w-7xl w-full mx-auto p-4 hidden flex flex-col space-y-3">
    
    <!-- Controls & Layer Switcher -->
    <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
      
      <div class="flex items-center gap-3">
        <span class="text-xl">🔍</span>
        <div>
          <h2 class="font-bold text-slate-900 text-sm">แผนที่สารสนเทศภูมิศาสตร์เชิงสำรวจ (GIS Explorer)</h2>
          <p class="text-xs text-slate-500">เลือกชั้นข้อมูลและตัวแปรเพื่อแสดงการกระจายตัวเชิงพื้นที่แบบ Choropleth</p>
        </div>
      </div>

      <div class="flex flex-wrap items-center gap-3">
        <!-- Metric Mode -->
        <div class="flex items-center gap-1.5">
          <label class="text-xs font-bold text-slate-600">แสดงผล:</label>
          <select id="explorer-metric" onchange="updateExplorerMap()" class="px-3 py-1.5 text-xs font-semibold bg-slate-50 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
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

        <!-- Basemap Switcher -->
        <div class="flex items-center gap-1.5">
          <label class="text-xs font-bold text-slate-600">แผนที่ฐาน:</label>
          <select id="explorer-basemap" onchange="switchBasemap()" class="px-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
            <option value="osm">OpenStreetMap</option>
            <option value="carto_light">Carto Light (เรียบง่าย)</option>
            <option value="carto_dark">Carto Dark (มืด)</option>
          </select>
        </div>
      </div>

    </div>

    <!-- Explorer Map Layout with Sidebar -->
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-4 flex-1">
      
      <!-- Map Area (3 Cols) -->
      <div class="lg:col-span-3 bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden relative">
        <div id="map-explorer" class="map-container w-full"></div>
      </div>

      <!-- Detail Info Panel (1 Col) -->
      <div class="lg:col-span-1 bg-white rounded-2xl border border-slate-200 shadow-sm p-4 flex flex-col justify-between overflow-y-auto max-h-[600px]">
        <div>
          <div class="flex items-center justify-between pb-3 border-b border-slate-100">
            <h3 class="font-bold text-slate-900 text-sm flex items-center gap-1.5">
              <span>📍 รายละเอียดอำเภอ</span>
            </h3>
            <span id="exp-badge-gap" class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">-</span>
          </div>

          <div class="mt-3">
            <div id="exp-district-name" class="text-xl font-bold text-blue-900">เลือกอำเภอจากแผนที่</div>
            <div id="exp-sub-title" class="text-xs text-slate-500 mt-0.5">คลิกบนพื้นที่อำเภอในแผนที่เพื่อดูข้อมูล</div>
          </div>

          <!-- Metrics List -->
          <div class="mt-4 space-y-2.5 text-xs">
            <div class="flex justify-between p-2 rounded-lg bg-slate-50 border border-slate-100">
              <span class="text-slate-500">จำนวนหมู่บ้านทั้งหมด:</span>
              <strong id="exp-stat-villages" class="text-slate-800">-</strong>
            </div>
            <div class="flex justify-between p-2 rounded-lg bg-rose-50 border border-rose-100">
              <span class="text-rose-700 font-medium">จุดเสี่ยงสูงรวม (5 ด้าน):</span>
              <strong id="exp-stat-high" class="text-rose-800">-</strong>
            </div>
            <div class="flex justify-between p-2 rounded-lg bg-blue-50 border border-blue-100">
              <span class="text-blue-700 font-medium">งบประมาณที่ได้รับ:</span>
              <strong id="exp-stat-budget" class="text-blue-900">-</strong>
            </div>
            <div class="flex justify-between p-2 rounded-lg bg-emerald-50 border border-emerald-100">
              <span class="text-emerald-700 font-medium">จำนวนโครงการรวม:</span>
              <strong id="exp-stat-projects" class="text-emerald-900">-</strong>
            </div>
          </div>

          <!-- Pillar Breakdown Mini Grid -->
          <div class="mt-4">
            <div class="text-[11px] font-bold text-slate-700 uppercase tracking-wider mb-2">จุดเสี่ยงสูงแยกตาม 5 ด้าน</div>
            <div class="grid grid-cols-5 gap-1 text-center" id="exp-pillar-mini-grid">
              <div class="bg-slate-50 p-1.5 rounded border text-[10px]">
                <div class="text-slate-400">ด1</div>
                <div id="exp-p1" class="font-bold text-slate-700">-</div>
              </div>
              <div class="bg-slate-50 p-1.5 rounded border text-[10px]">
                <div class="text-slate-400">ด2</div>
                <div id="exp-p2" class="font-bold text-slate-700">-</div>
              </div>
              <div class="bg-slate-50 p-1.5 rounded border text-[10px]">
                <div class="text-slate-400">ด3</div>
                <div id="exp-p3" class="font-bold text-slate-700">-</div>
              </div>
              <div class="bg-slate-50 p-1.5 rounded border text-[10px]">
                <div class="text-slate-400">ด4</div>
                <div id="exp-p4" class="font-bold text-slate-700">-</div>
              </div>
              <div class="bg-slate-50 p-1.5 rounded border text-[10px]">
                <div class="text-slate-400">ด5</div>
                <div id="exp-p5" class="font-bold text-slate-700">-</div>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-4 pt-3 border-t border-slate-100 text-[11px] text-slate-400 text-center">
          คลิกที่อำเภออื่นบนแผนที่เพื่อสลับดูข้อมูล
        </div>
      </div>

    </div>

  </section>

  <!-- ========================================================================= -->
  <!-- VIEW 3: GAP ANALYSIS SUMMARY & EXPORT (หน้าสรุปตารางและส่งออก) -->
  <!-- ========================================================================= -->
  <section id="view-table" class="flex-1 max-w-7xl w-full mx-auto p-4 hidden flex flex-col space-y-4">
    
    <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h2 class="font-bold text-slate-900 text-base">ตารางประเมินช่องว่างเชิงนโยบาย (25 อำเภอในเชียงใหม่)</h2>
        <p class="text-xs text-slate-500 mt-0.5">วิเคราะห์เปรียบเทียบงบประมาณที่ได้รับกับระดับความเสี่ยงเพื่อจัดลำดับความสำคัญในการจัดสรรงบประมาณรอบถัดไป</p>
      </div>

      <div class="flex items-center gap-2">
        <a href="ChiangMai_Water_Risk_Budget_Dashboard.xlsx" download class="px-3.5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold flex items-center gap-1.5 shadow transition">
          <span>📥 ดาวน์โหลด Excel (1.3 MB)</span>
        </a>
      </div>
    </div>

    <!-- Table Container -->
    <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
      <div class="overflow-x-auto max-h-[600px]">
        <table class="w-full text-left text-xs border-collapse">
          <thead class="sticky top-0 bg-slate-100 z-10 text-slate-700 border-b border-slate-200">
            <tr>
              <th class="p-3 font-bold">อำเภอ</th>
              <th class="p-3 font-bold text-center">จำนวนหมู่บ้าน</th>
              <th class="p-3 font-bold text-center text-rose-600">เสี่ยงสูงรวม</th>
              <th class="p-3 font-bold">สถานะการจัดสรร (Gap Status)</th>
              <th class="p-3 font-bold text-right">งบประมาณรวม (ลบ.)</th>
              <th class="p-3 font-bold text-right">โครงการ</th>
              <th class="p-3 font-bold text-center">ด1 อุปโภค</th>
              <th class="p-3 font-bold text-center">ด2 เกษตร</th>
              <th class="p-3 font-bold text-center">ด3 น้ำท่วม</th>
              <th class="p-3 font-bold text-center">ด4 คุณภาพ</th>
              <th class="p-3 font-bold text-center">ด5 ป่าต้นน้ำ</th>
            </tr>
          </thead>
          <tbody id="gap-table-body" class="divide-y divide-slate-100">
            <!-- Populated by JS -->
          </tbody>
        </table>
      </div>
    </div>

  </section>

  <!-- Data Payload Script -->
  <script>
    const geojsonData = __GEOJSON_DATA__;
    const statsData = __STATS_DATA__;

    // View Navigation
    function navigateView(viewId) {
      document.querySelectorAll('section').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.nav-tab').forEach(btn => {
        btn.classList.remove('bg-blue-600', 'text-white', 'shadow');
        btn.classList.add('text-slate-400', 'hover:text-white', 'hover:bg-slate-700/50');
      });

      document.getElementById(viewId).classList.remove('hidden');
      const activeBtn = document.getElementById(viewId.replace('view-', 'nav-btn-'));
      if (activeBtn) {
        activeBtn.classList.remove('text-slate-400', 'hover:text-white', 'hover:bg-slate-700/50');
        activeBtn.classList.add('bg-blue-600', 'text-white', 'shadow');
      }

      // Invalidate map sizes
      setTimeout(() => {
        if (viewId === 'view-compare') {
          if (mapRisk) mapRisk.invalidateSize();
          if (mapBudget) mapBudget.invalidateSize();
        } else if (viewId === 'view-explorer') {
          if (mapExplorer) mapExplorer.invalidateSize();
        }
      }, 100);
    }

    // =========================================================================
    // COLOR SCALES
    // =========================================================================
    function getRiskColor(val, maxVal = 185) {
      const ratio = Math.min(val / maxVal, 1);
      return ratio > 0.8 ? '#800026' :
             ratio > 0.6 ? '#bd0026' :
             ratio > 0.4 ? '#e31a1c' :
             ratio > 0.25? '#fc4e2a' :
             ratio > 0.15? '#fd8d3c' :
             ratio > 0.05? '#feb24c' :
             ratio > 0   ? '#fed976' :
                           '#ffeda0';
    }

    function getBudgetColor(val, maxVal = 4836) {
      const ratio = Math.min(val / maxVal, 1);
      return ratio > 0.75 ? '#014636' :
             ratio > 0.50 ? '#016c59' :
             ratio > 0.30 ? '#02818a' :
             ratio > 0.20 ? '#3690c0' :
             ratio > 0.10 ? '#67a9cf' :
             ratio > 0.04 ? '#a6bddb' :
             ratio > 0    ? '#d0d1e6' :
                            '#f1eef6';
    }

    // =========================================================================
    // DUAL MAP SETUP (LEAFLET SYNCED)
    // =========================================================================
    let mapRisk, mapBudget;
    let layerRisk, layerBudget;
    let isSyncing = false;

    const CHIANGMAI_CENTER = [18.7883, 98.9853];
    const DEFAULT_ZOOM = 8;

    function initDualMaps() {
      // Map 1: Risk
      mapRisk = L.map('map-risk', {
        zoomControl: true,
        attributionControl: false
      }).setView(CHIANGMAI_CENTER, DEFAULT_ZOOM);

      L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        maxZoom: 18
      }).addTo(mapRisk);

      // Map 2: Budget
      mapBudget = L.map('map-budget', {
        zoomControl: true,
        attributionControl: false
      }).setView(CHIANGMAI_CENTER, DEFAULT_ZOOM);

      L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        maxZoom: 18
      }).addTo(mapBudget);

      // Synced Navigation
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

    function getPillarPropertyNames(pillarId) {
      if (pillarId === 'all') return { riskProp: 'high_risk_total', budgetProp: 'total_budget' };
      return { riskProp: 'high_p' + pillarId, budgetProp: 'budget_p' + pillarId };
    }

    function renderDualLayers(pillarId) {
      if (layerRisk) mapRisk.removeLayer(layerRisk);
      if (layerBudget) mapBudget.removeLayer(layerBudget);

      const { riskProp, budgetProp } = getPillarPropertyNames(pillarId);

      // Calc maximums for dynamic color scale
      const maxRisk = Math.max(...geojsonData.features.map(f => f.properties[riskProp] || 0), 1);
      const maxBudget = Math.max(...geojsonData.features.map(f => f.properties[budgetProp] || 0), 1);

      // Left Map: Risk Layer
      layerRisk = L.geoJSON(geojsonData, {
        style: (feature) => ({
          fillColor: getRiskColor(feature.properties[riskProp] || 0, maxRisk),
          weight: 1.5,
          opacity: 1,
          color: '#ffffff',
          fillOpacity: 0.85
        }),
        onEachFeature: (feature, layer) => {
          layer.bindTooltip(`<strong>อ.${feature.properties.amp_th}</strong><br>เสี่ยงสูง: ${feature.properties[riskProp] || 0} จุด`, {
            className: 'leaflet-tooltip-custom',
            direction: 'center'
          });

          layer.on('mouseover', () => highlightBoth(feature.properties.amp_th));
          layer.on('mouseout', () => resetBothHighlight());
          layer.on('click', () => selectDistrictInspector(feature.properties));
        }
      }).addTo(mapRisk);

      // Right Map: Budget Layer
      layerBudget = L.geoJSON(geojsonData, {
        style: (feature) => ({
          fillColor: getBudgetColor(feature.properties[budgetProp] || 0, maxBudget),
          weight: 1.5,
          opacity: 1,
          color: '#ffffff',
          fillOpacity: 0.85
        }),
        onEachFeature: (feature, layer) => {
          const bVal = (feature.properties[budgetProp] || 0).toLocaleString(undefined, {minimumFractionDigits: 1, maximumFractionDigits: 1});
          layer.bindTooltip(`<strong>อ.${feature.properties.amp_th}</strong><br>งบประมาณ: ${bVal} ลบ.`, {
            className: 'leaflet-tooltip-custom',
            direction: 'center'
          });

          layer.on('mouseover', () => highlightBoth(feature.properties.amp_th));
          layer.on('mouseout', () => resetBothHighlight());
          layer.on('click', () => selectDistrictInspector(feature.properties));
        }
      }).addTo(mapBudget);
    }

    function highlightBoth(ampName) {
      if (layerRisk) {
        layerRisk.eachLayer(l => {
          if (l.feature.properties.amp_th === ampName) {
            l.setStyle({ weight: 3, color: '#000000', fillOpacity: 1 });
            l.bringToFront();
          }
        });
      }
      if (layerBudget) {
        layerBudget.eachLayer(l => {
          if (l.feature.properties.amp_th === ampName) {
            l.setStyle({ weight: 3, color: '#000000', fillOpacity: 1 });
            l.bringToFront();
          }
        });
      }
    }

    function resetBothHighlight() {
      if (layerRisk) layerRisk.resetStyle();
      if (layerBudget) layerBudget.resetStyle();
    }

    function selectDistrictInspector(props) {
      document.getElementById('dual-ins-title').innerText = `อำเภอ${props.amp_th} (ทั้งหมด ${props.villages} หมู่บ้าน)`;
      document.getElementById('dual-ins-risk').innerText = `${props.high_risk_total} จุดเสี่ยงสูง`;
      document.getElementById('dual-ins-budget').innerText = `${Number(props.total_budget).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})} ล้านบาท (${props.total_projects} โครงการ)`;
      document.getElementById('dual-ins-gap').innerText = props.gap_status;
    }

    function updateDualMaps() {
      const p = document.getElementById('dual-pillar-select').value;
      renderDualLayers(p);
      
      const pNames = {
        'all': 'รวม 5 ด้าน',
        '1': 'ด1 อุปโภค',
        '2': 'ด2 เกษตร/ผลิต',
        '3': 'ด3 น้ำท่วม',
        '4': 'ด4 คุณภาพน้ำ',
        '5': 'ด5 ป่าต้นน้ำ'
      };
      document.getElementById('label-left-metric').innerText = `ความเสี่ยงสูง (${pNames[p]})`;
      document.getElementById('label-right-metric').innerText = `งบประมาณจัดสรร (${pNames[p]})`;
    }

    function resetDualView() {
      mapRisk.setView(CHIANGMAI_CENTER, DEFAULT_ZOOM);
      mapBudget.setView(CHIANGMAI_CENTER, DEFAULT_ZOOM);
    }

    // =========================================================================
    // SINGLE GIS EXPLORER SETUP
    // =========================================================================
    let mapExplorer, layerExplorer, currentTileLayer;

    function initExplorerMap() {
      mapExplorer = L.map('map-explorer', {
        attributionControl: false
      }).setView(CHIANGMAI_CENTER, DEFAULT_ZOOM);

      currentTileLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(mapExplorer);
      updateExplorerMap();
    }

    function switchBasemap() {
      const b = document.getElementById('explorer-basemap').value;
      if (currentTileLayer) mapExplorer.removeLayer(currentTileLayer);

      let tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
      if (b === 'carto_light') tileUrl = 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png';
      if (b === 'carto_dark') tileUrl = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';

      currentTileLayer = L.tileLayer(tileUrl).addTo(mapExplorer);
    }

    function updateExplorerMap() {
      if (layerExplorer) mapExplorer.removeLayer(layerExplorer);

      const metric = document.getElementById('explorer-metric').value;
      const isBudget = metric.includes('budget');
      const maxVal = Math.max(...geojsonData.features.map(f => f.properties[metric] || 0), 1);

      layerExplorer = L.geoJSON(geojsonData, {
        style: (feature) => {
          const val = feature.properties[metric] || 0;
          return {
            fillColor: isBudget ? getBudgetColor(val, maxVal) : getRiskColor(val, maxVal),
            weight: 1.5,
            opacity: 1,
            color: '#ffffff',
            fillOpacity: 0.85
          };
        },
        onEachFeature: (feature, layer) => {
          const val = feature.properties[metric] || 0;
          const displayVal = isBudget ? Number(val).toLocaleString(undefined, {minimumFractionDigits: 1, maximumFractionDigits: 1}) + ' ลบ.' : val + ' แห่ง';
          
          layer.bindTooltip(`<strong>อ.${feature.properties.amp_th}</strong><br>${displayVal}`, {
            className: 'leaflet-tooltip-custom',
            direction: 'center'
          });

          layer.on('click', () => populateExplorerSidebar(feature.properties));
        }
      }).addTo(mapExplorer);
    }

    function populateExplorerSidebar(props) {
      document.getElementById('exp-district-name').innerText = `อ.${props.amp_th}`;
      document.getElementById('exp-sub-title').innerText = `รหัสอำเภอ: ${props.amp_code} | พื้นที่: ${Number(props.area_sqkm).toFixed(1)} ตร.กม.`;
      document.getElementById('exp-badge-gap').innerText = props.gap_status;
      
      document.getElementById('exp-stat-villages').innerText = `${props.villages} หมู่บ้าน`;
      document.getElementById('exp-stat-high').innerText = `${props.high_risk_total} จุด`;
      document.getElementById('exp-stat-budget').innerText = `${Number(props.total_budget).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})} ลบ.`;
      document.getElementById('exp-stat-projects').innerText = `${props.total_projects}} โครงการ`;

      document.getElementById('exp-p1').innerText = props.high_p1 || 0;
      document.getElementById('exp-p2').innerText = props.high_p2 || 0;
      document.getElementById('exp-p3').innerText = props.high_p3 || 0;
      document.getElementById('exp-p4').innerText = props.high_p4 || 0;
      document.getElementById('exp-p5').innerText = props.high_p5 || 0;
    }

    // =========================================================================
    // TABLE VIEW POPULATION
    // =========================================================================
    function populateGapTable() {
      const tbody = document.getElementById('gap-table-body');
      let html = '';

      statsData.districts.forEach(d => {
        if (d['อำเภอ'] === 'โครงการระดับจังหวัด/ไม่ระบุอำเภอ') return;

        let badgeClass = 'bg-emerald-100 text-emerald-800 border border-emerald-300';
        if (d['สถานะการจัดสรร (Gap Status)'].includes('วิกฤติ')) badgeClass = 'bg-rose-100 text-rose-800 border border-rose-300 font-bold';
        else if (d['สถานะการจัดสรร (Gap Status)'].includes('เสี่ยงสูง') || d['สถานะการจัดสรร (Gap Status)'].includes('ควรเพิ่ม')) badgeClass = 'bg-amber-100 text-amber-800 border border-amber-300';

        html += `
          <tr class="hover:bg-slate-50 transition">
            <td class="p-3 font-bold text-slate-900">${d['อำเภอ']}</td>
            <td class="p-3 text-center text-slate-600">${d['จำนวนหมู่บ้าน']}</td>
            <td class="p-3 text-center font-bold text-rose-600 bg-rose-50/40">${d['จำนวนเสี่ยงสูง_รวมทุกด้าน']}</td>
            <td class="p-3"><span class="px-2 py-0.5 rounded-full text-[11px] ${badgeClass}">${d['สถานะการจัดสรร (Gap Status)']}</span></td>
            <td class="p-3 text-right font-bold text-slate-900">${Number(d['งบประมาณรวม (ล้านบาท)']).toLocaleString(undefined, {minimumFractionDigits: 1, maximumFractionDigits: 1})}</td>
            <td class="p-3 text-right font-medium">${d['จำนวนโครงการรวม']}</td>
            <td class="p-3 text-center text-slate-600">${d['เสี่ยงสูง_ด1_อุปโภค'] > 0 ? '<span class="text-rose-600 font-bold">' + d['เสี่ยงสูง_ด1_อุปโภค'] + '</span>' : '-'}</td>
            <td class="p-3 text-center text-slate-600">${d['เสี่ยงสูง_ด2_เกษตร'] > 0 ? '<span class="text-rose-600 font-bold">' + d['เสี่ยงสูง_ด2_เกษตร'] + '</span>' : '-'}</td>
            <td class="p-3 text-center text-slate-600">${d['เสี่ยงสูง_ด3_น้ำท่วม'] > 0 ? '<span class="text-rose-600 font-bold">' + d['เสี่ยงสูง_ด3_น้ำท่วม'] + '</span>' : '-'}</td>
            <td class="p-3 text-center text-slate-600">${d['เสี่ยงสูง_ด4_คุณภาพน้ำ'] > 0 ? '<span class="text-rose-600 font-bold">' + d['เสี่ยงสูง_ด4_คุณภาพน้ำ'] + '</span>' : '-'}</td>
            <td class="p-3 text-center text-slate-600">${d['เสี่ยงสูง_ด5_ป่าต้นน้ำ'] > 0 ? '<span class="text-rose-600 font-bold">' + d['เสี่ยงสูง_ด5_ป่าต้นน้ำ'] + '</span>' : '-'}</td>
          </tr>
        `;
      });

      tbody.innerHTML = html;
    }

    // =========================================================================
    // INITIALIZATION
    // =========================================================================
    window.addEventListener('DOMContentLoaded', () => {
      initDualMaps();
      initExplorerMap();
      populateGapTable();
    });
  </script>
</body>
</html>"""

full_html = html_template.replace('__GEOJSON_DATA__', geojson_str).replace('__STATS_DATA__', stats_str)

with open('ChiangMai_Water_GIS_Dashboard.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

artifact_gis_path = '/Users/commindo/.gemini/antigravity/brain/e2040493-6043-4283-af0a-d3d6adad8d8d/water_gis_dashboard.html'
with open(artifact_gis_path, 'w', encoding='utf-8') as f:
    f.write(full_html)

print('GIS Dashboard HTML successfully created!')
