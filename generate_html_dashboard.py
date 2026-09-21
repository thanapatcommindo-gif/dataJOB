import json

with open('dashboard_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

json_str = json.dumps(data, ensure_ascii=False)

html_content = f'''<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ระบบวิเคราะห์และแดชบอร์ดแผนน้ำเชียงใหม่ (2565-2570)</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    body {{ font-family: 'Sarabun', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
    .badge-crisis {{ background-color: #FEE2E2; color: #991B1B; border: 1px solid #FCA5A5; }}
    .badge-warn {{ background-color: #FEF3C7; color: #92400E; border: 1px solid #FCD34D; }}
    .badge-ok {{ background-color: #D1FAE5; color: #065F46; border: 1px solid #6EE7B7; }}
    .badge-blue {{ background-color: #DBEAFE; color: #1E40AF; border: 1px solid #93C5FD; }}
  </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased min-h-screen p-4 md:p-6">

  <!-- Header -->
  <header class="max-w-7xl mx-auto bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 text-white rounded-2xl p-6 shadow-xl mb-6">
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <div>
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-800/60 border border-blue-400/30 text-blue-200 text-xs font-semibold mb-2">
          <span>🌊 แผนแม่บทการบริหารจัดการทรัพยากรน้ำ 5 ด้าน</span>
          <span>•</span>
          <span>จังหวัดเชียงใหม่ (2565 - 2570)</span>
        </div>
        <h1 class="text-2xl md:text-3xl font-bold tracking-tight">แดชบอร์ดวิเคราะห์งบประมาณ vs พื้นที่เสี่ยงภัยน้ำ</h1>
        <p class="text-blue-200 text-sm mt-1">
          การวิเคราะห์เชิงเปรียบเทียบระหว่างความเสี่ยง 2,200 หมู่บ้าน และการจัดสรรงบประมาณ 6,312 โครงการ (วงเงิน 35,094.77 ล้านบาท)
        </p>
      </div>
      <div class="flex flex-wrap gap-2">
        <div class="bg-white/10 backdrop-blur rounded-xl p-3 border border-white/10 text-center min-w-[120px]">
          <div class="text-xs text-blue-200">งบประมาณรวม</div>
          <div class="text-xl font-bold text-amber-300">35.09 พันล้าน</div>
        </div>
        <div class="bg-white/10 backdrop-blur rounded-xl p-3 border border-white/10 text-center min-w-[120px]">
          <div class="text-xs text-blue-200">โครงการทั้งหมด</div>
          <div class="text-xl font-bold text-emerald-300">6,312 โครงการ</div>
        </div>
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <main class="max-w-7xl mx-auto space-y-6">

    <!-- KPI Metric Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- KPI 1 -->
      <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm hover:shadow-md transition">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-blue-600 uppercase tracking-wider">งบประมาณจัดสรร</span>
          <span class="p-2 bg-blue-50 text-blue-600 rounded-xl text-lg">💰</span>
        </div>
        <div class="mt-2 text-2xl font-bold text-slate-900">35,094.77 <span class="text-sm font-normal text-slate-500">ลบ.</span></div>
        <div class="mt-1 text-xs text-slate-500">ครอบคลุม 6 ปีงบประมาณ (65-70)</div>
      </div>

      <!-- KPI 2 -->
      <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm hover:shadow-md transition">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-emerald-600 uppercase tracking-wider">ความครอบคลุมพื้นที่</span>
          <span class="p-2 bg-emerald-50 text-emerald-600 rounded-xl text-lg">📍</span>
        </div>
        <div class="mt-2 text-2xl font-bold text-slate-900">25 <span class="text-sm font-normal text-slate-500">อำเภอ</span> / 204 <span class="text-sm font-normal text-slate-500">ตำบล</span></div>
        <div class="mt-1 text-xs text-slate-500">ประเมินความเสี่ยง 2,200 หมู่บ้าน</div>
      </div>

      <!-- KPI 3 -->
      <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm hover:shadow-md transition">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-rose-600 uppercase tracking-wider">หมู่บ้านเสี่ยงสูง (≥1 ด้าน)</span>
          <span class="p-2 bg-rose-50 text-rose-600 rounded-xl text-lg">🚨</span>
        </div>
        <div class="mt-2 text-2xl font-bold text-rose-600">885 <span class="text-sm font-normal text-slate-500">หมู่บ้าน</span></div>
        <div class="mt-1 text-xs text-rose-500 font-medium">คิดเป็น 40.2% ของทั้งจังหวัด</div>
      </div>

      <!-- KPI 4 -->
      <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm hover:shadow-md transition">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-amber-600 uppercase tracking-wider">จุดวิกฤติเร่งด่วน (≥2 ด้าน)</span>
          <span class="p-2 bg-amber-50 text-amber-600 rounded-xl text-lg">⚡</span>
        </div>
        <div class="mt-2 text-2xl font-bold text-amber-600">142 <span class="text-sm font-normal text-slate-500">หมู่บ้าน</span></div>
        <div class="mt-1 text-xs text-amber-700 font-medium">ต้องการแผนเร่งด่วนบูรณาการ</div>
      </div>
    </div>

    <!-- Alert Banner: Key Finding -->
    <div class="bg-gradient-to-r from-rose-50 to-amber-50 border-l-4 border-rose-500 p-4 rounded-xl shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-3">
      <div class="flex items-start gap-3">
        <span class="text-2xl mt-0.5">💡</span>
        <div>
          <h4 class="font-bold text-slate-900 text-sm md:text-base">ข้อค้นพบสำคัญจากการวิเคราะห์ช่องว่าง (Key Gap Analysis Finding)</h4>
          <p class="text-slate-600 text-xs md:text-sm mt-0.5">
            <strong>อ.สารภี</strong> มีจำนวนจุดเสี่ยงสูงมากที่สุดในจังหวัด (185 จุด โดยเฉพาะด้านน้ำท่วม คุณภาพน้ำ และดินพังทลาย) แต่ได้รับงบประมาณรวมเพียง <strong>558.60 ลบ.</strong> (อันดับ 20 ของจังหวัด) ในขณะที่ <strong>อ.แม่แตง</strong> ได้รับงบสูงสุด <strong>4,836.09 ลบ.</strong> แต่มีจุดเสี่ยงสูงเพียง 10 จุด
          </p>
        </div>
      </div>
    </div>

    <!-- Tab Navigation -->
    <div class="flex border-b border-slate-200 space-x-2 overflow-x-auto pb-1">
      <button onclick="switchTab('tab-pillar')" id="btn-tab-pillar" class="tab-btn px-4 py-2 text-sm font-semibold rounded-t-xl bg-white text-blue-700 border-t-2 border-blue-600 shadow-sm">
        📊 5 ด้านแผนแม่บทน้ำ
      </button>
      <button onclick="switchTab('tab-district')" id="btn-tab-district" class="tab-btn px-4 py-2 text-sm font-semibold rounded-t-xl text-slate-600 hover:text-slate-900 hover:bg-slate-100">
        🎯 วิเคราะห์รายอำเภอ (Gap Analysis)
      </button>
      <button onclick="switchTab('tab-year-agency')" id="btn-tab-year-agency" class="tab-btn px-4 py-2 text-sm font-semibold rounded-t-xl text-slate-600 hover:text-slate-900 hover:bg-slate-100">
        📅 รายปี & หน่วยงาน
      </button>
      <button onclick="switchTab('tab-guide')" id="btn-tab-guide" class="tab-btn px-4 py-2 text-sm font-semibold rounded-t-xl text-slate-600 hover:text-slate-900 hover:bg-slate-100">
        🚀 คู่มือ Google Sheets
      </button>
    </div>

    <!-- TAB 1: 5 PILLARS -->
    <div id="tab-pillar" class="tab-content space-y-6">
      <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-5">
        <h3 class="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
          <span>สรุปเปรียบเทียบ 5 ด้านแผนแม่บทน้ำ (งบประมาณ vs ระดับความเสี่ยง)</span>
        </h3>
        
        <div class="overflow-x-auto">
          <table class="w-full text-left text-sm border-collapse">
            <thead>
              <tr class="bg-slate-100 text-slate-700 border-b border-slate-200">
                <th class="p-3 font-bold text-center">ด้าน</th>
                <th class="p-3 font-bold">ชื่อแผนแม่บท</th>
                <th class="p-3 font-bold text-right">โครงการ</th>
                <th class="p-3 font-bold text-right">งบประมาณ (ลบ.)</th>
                <th class="p-3 font-bold text-right">สัดส่วนงบ</th>
                <th class="p-3 font-bold text-center text-rose-600">เสี่ยงสูง (แห่ง)</th>
                <th class="p-3 font-bold text-center text-amber-600">เสี่ยงปานกลาง</th>
                <th class="p-3 font-bold text-center text-emerald-600">เสี่ยงน้อย</th>
                <th class="p-3 font-bold text-right">งบเฉลี่ย/โครงการ</th>
              </tr>
            </thead>
            <tbody id="pillar-table-body" class="divide-y divide-slate-100">
              <!-- Rendered by JS -->
            </tbody>
            <tfoot>
              <tr class="bg-slate-50 font-bold text-slate-900 border-t-2 border-slate-300">
                <td colspan="2" class="p-3 text-center">รวมทั้งสิ้น</td>
                <td class="p-3 text-right">6,312</td>
                <td class="p-3 text-right">35,094.77</td>
                <td class="p-3 text-right">100.0%</td>
                <td class="p-3 text-center text-rose-600">1,040*</td>
                <td class="p-3 text-center text-amber-600">4,197*</td>
                <td class="p-3 text-center text-emerald-600">5,767*</td>
                <td class="p-3 text-right">5.56</td>
              </tr>
            </tfoot>
          </table>
          <div class="text-[11px] text-slate-400 mt-2">* หมายเหตุ: จำนวนระดับความเสี่ยงในแถวรวมเป็นการนับผลรวมจุดเสี่ยงในแต่ละด้าน (2,200 หมู่บ้าน x 5 ด้าน = 11,000 จุดประเมิน)</div>
        </div>
      </div>

      <!-- Pillar Visual Progress Cards -->
      <div class="grid grid-cols-1 md:grid-cols-5 gap-4" id="pillar-cards-grid">
        <!-- Rendered by JS -->
      </div>
    </div>

    <!-- TAB 2: DISTRICT GAP ANALYSIS -->
    <div id="tab-district" class="tab-content hidden space-y-6">
      <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-5">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
          <div>
            <h3 class="text-lg font-bold text-slate-900">ตารางวิเคราะห์ช่องว่างรายอำเภอ (25 อำเภอในเชียงใหม่)</h3>
            <p class="text-xs text-slate-500 mt-0.5">เปรียบเทียบจุดเสี่ยงสูงกับงบประมาณที่ได้รับการจัดสรรเพื่อชี้เป้าพื้นที่ที่ควรได้รับการจัดสรรเพิ่มเติม</p>
          </div>
          <div class="flex items-center gap-2">
            <input type="text" id="district-search" oninput="filterDistricts()" placeholder="🔍 ค้นหาอำเภอ..." class="px-3 py-1.5 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
            <select id="district-sort" onchange="filterDistricts()" class="px-3 py-1.5 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option value="high_risk_desc">เรียงตาม: จุดเสี่ยงสูง (มาก-น้อย)</option>
              <option value="budget_desc">เรียงตาม: งบประมาณ (มาก-น้อย)</option>
              <option value="budget_asc">เรียงตาม: งบประมาณ (น้อย-มาก)</option>
              <option value="name_asc">เรียงตาม: ชื่ออำเภอ (ก-ฮ)</option>
            </select>
          </div>
        </div>

        <div class="overflow-x-auto max-h-[600px]">
          <table class="w-full text-left text-sm border-collapse">
            <thead class="sticky top-0 bg-slate-100 z-10">
              <tr class="text-slate-700 border-b border-slate-200 text-xs">
                <th class="p-2.5 font-bold">อำเภอ</th>
                <th class="p-2.5 font-bold text-center">หมู่บ้าน</th>
                <th class="p-2.5 font-bold text-center text-rose-600">เสี่ยงสูงรวม</th>
                <th class="p-2.5 font-bold">สถานะการจัดสรร (Gap)</th>
                <th class="p-2.5 font-bold text-right">งบรวม (ลบ.)</th>
                <th class="p-2.5 font-bold text-right">โครงการ</th>
                <th class="p-2.5 font-bold text-center">ด1 (อุปโภค)</th>
                <th class="p-2.5 font-bold text-center">ด2 (เกษตร)</th>
                <th class="p-2.5 font-bold text-center">ด3 (น้ำท่วม)</th>
                <th class="p-2.5 font-bold text-center">ด4 (คุณภาพ)</th>
                <th class="p-2.5 font-bold text-center">ด5 (ป่าต้นน้ำ)</th>
              </tr>
            </thead>
            <tbody id="district-table-body" class="divide-y divide-slate-100 text-xs">
              <!-- Rendered by JS -->
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 3: YEAR & AGENCY -->
    <div id="tab-year-agency" class="tab-content hidden space-y-6">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- Yearly Breakdown -->
        <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-5">
          <h3 class="text-base font-bold text-slate-900 mb-3">📅 แผนการจัดสรรงบประมาณรายปี (2565 - 2570)</h3>
          <div class="space-y-3" id="yearly-bars">
            <!-- Rendered by JS -->
          </div>
        </div>

        <!-- Top Agencies Breakdown -->
        <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-5">
          <h3 class="text-base font-bold text-slate-900 mb-3">🏢 10 หน่วยงานหลักที่ได้รับจัดสรรงบประมาณ</h3>
          <div class="space-y-3" id="agency-bars">
            <!-- Rendered by JS -->
          </div>
        </div>

      </div>
    </div>

    <!-- TAB 4: GOOGLE SHEETS GUIDE -->
    <div id="tab-guide" class="tab-content hidden space-y-6">
      <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-6">
        <div>
          <h3 class="text-lg font-bold text-slate-900">🚀 ขั้นตอนการนำไฟล์ขึ้น Google Sheets และทำแดชบอร์ด</h3>
          <p class="text-sm text-slate-500 mt-1">ไฟล์ Master Workbook ถูกจัดระเบียบและปรับปรุงขนาดจาก 265 MB เหลือเพียง 1.3 MB พร้อมสูตรและการจัดรูปแบบที่รองรับ Google Sheets 100%</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="p-4 rounded-xl bg-blue-50 border border-blue-200">
            <div class="text-blue-700 font-bold text-base mb-1">ขั้นตอนที่ 1: อัปโหลด</div>
            <p class="text-xs text-slate-600">เปิด Google Drive แล้วลากไฟล์ <code class="bg-white px-1 py-0.5 rounded border">ChiangMai_Water_Risk_Budget_Dashboard.xlsx</code> ขึ้นไป แล้วคลิกขวาเลือก <strong>"เปิดด้วย Google สเปรดชีต"</strong></p>
          </div>
          <div class="p-4 rounded-xl bg-emerald-50 border border-emerald-200">
            <div class="text-emerald-700 font-bold text-base mb-1">ขั้นตอนที่ 2: สร้าง Pivot Table</div>
            <p class="text-xs text-slate-600">ใช้ชีต <code>💰 Data_โครงการและงบประมาณ</code> หรือ <code>🔄 Data_Risk_Long</code> ในการแทรก Pivot Table และ Chart เพื่อสร้าง Visual แบบ Interactive</p>
          </div>
          <div class="p-4 rounded-xl bg-purple-50 border border-purple-200">
            <div class="text-purple-700 font-bold text-base mb-1">ขั้นตอนที่ 3: เชื่อมต่อ Looker Studio</div>
            <p class="text-xs text-slate-600">เข้า <a href="https://lookerstudio.google.com" target="_blank" class="text-purple-600 underline font-semibold">Looker Studio</a> เลือก Data Source เป็น Google Sheets เพื่อสร้าง Interactive Map & Executive Dashboard ได้ทันที</p>
          </div>
        </div>

        <!-- Formulas reference -->
        <div class="p-4 rounded-xl bg-slate-50 border border-slate-200">
          <h4 class="font-bold text-slate-900 text-sm mb-2">💡 สูตรคำนวณสำเร็จรูปสำหรับ Google Sheets:</h4>
          <div class="space-y-2 text-xs font-mono">
            <div class="bg-white p-2.5 rounded border border-slate-200">
              <span class="text-blue-600 font-bold">// รวมงบประมาณตามอำเภอ:</span><br>
              <code>=SUMIFS('💰 Data_โครงการและงบประมาณ'!M:M, '💰 Data_โครงการและงบประมาณ'!J:J, "สารภี")</code>
            </div>
            <div class="bg-white p-2.5 rounded border border-slate-200">
              <span class="text-emerald-600 font-bold">// ดึงโครงการความเสี่ยงสูงด้วย QUERY:</span><br>
              <code>=QUERY('💰 Data_โครงการและงบประมาณ'!A:M, "SELECT B, D, G, J, L, M WHERE J='สารภี' AND D=3 ORDER BY M DESC", 1)</code>
            </div>
          </div>
        </div>
      </div>
    </div>

  </main>

  <script>
    const data = {json_str};

    // Tab switching
    function switchTab(tabId) {{
      document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.tab-btn').forEach(btn => {{
        btn.classList.remove('bg-white', 'text-blue-700', 'border-t-2', 'border-blue-600', 'shadow-sm');
        btn.classList.add('text-slate-600', 'hover:bg-slate-100');
      }});
      
      document.getElementById(tabId).classList.remove('hidden');
      const activeBtn = document.getElementById('btn-' + tabId);
      activeBtn.classList.remove('text-slate-600', 'hover:bg-slate-100');
      activeBtn.classList.add('bg-white', 'text-blue-700', 'border-t-2', 'border-blue-600', 'shadow-sm');
    }}

    // Render Pillar Table & Cards
    function renderPillars() {{
      const tbody = document.getElementById('pillar-table-body');
      const grid = document.getElementById('pillar-cards-grid');
      const totalBudget = data.kpis.total_budget;
      
      let tbodyHtml = '';
      let cardsHtml = '';

      data.pillars.forEach(p => {{
        const pct = ((p.budget / totalBudget) * 100).toFixed(1);
        const avg = (p.budget / p.projects).toFixed(2);
        
        tbodyHtml += `
          <tr class="hover:bg-slate-50 transition">
            <td class="p-3 text-center font-bold text-slate-500">${{p.id}}</td>
            <td class="p-3 font-medium text-slate-800">${{p.name}}</td>
            <td class="p-3 text-right font-medium">${{p.projects.toLocaleString()}}</td>
            <td class="p-3 text-right font-bold text-slate-900">${{p.budget.toLocaleString(undefined, {{minimumFractionDigits: 2, maximumFractionDigits: 2}})}}</td>
            <td class="p-3 text-right text-blue-600 font-semibold">${{pct}}%</td>
            <td class="p-3 text-center font-bold text-rose-600 bg-rose-50/50">${{p.high_risk.toLocaleString()}}</td>
            <td class="p-3 text-center text-amber-600">${{p.med_risk.toLocaleString()}}</td>
            <td class="p-3 text-center text-emerald-600">${{p.low_risk.toLocaleString()}}</td>
            <td class="p-3 text-right text-slate-600">${{avg}}</td>
          </tr>
        `;

        cardsHtml += `
          <div class="bg-white rounded-xl border border-slate-200 p-4 shadow-sm flex flex-col justify-between">
            <div>
              <div class="text-xs font-bold text-slate-400 uppercase">ด้านที่ ${{p.id}}</div>
              <div class="text-sm font-bold text-slate-800 line-clamp-2 mt-1" title="${{p.name}}">${{p.name.replace(/ด้านที่ \\d+ /, '')}}</div>
              <div class="mt-3 text-xl font-bold text-blue-900">${{p.budget.toLocaleString(undefined, {{minimumFractionDigits: 1, maximumFractionDigits: 1}})}} <span class="text-xs font-normal text-slate-500">ลบ.</span></div>
              <div class="text-xs text-slate-500 mt-0.5">${{p.projects.toLocaleString()}} โครงการ (${{pct}}%)</div>
            </div>
            <div class="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
              <span class="text-rose-600 font-semibold">🚨 เสี่ยงสูง: ${{p.high_risk}}</span>
              <span class="text-slate-400">กลาง: ${{p.med_risk}}</span>
            </div>
          </div>
        `;
      }});

      tbody.innerHTML = tbodyHtml;
      grid.innerHTML = cardsHtml;
    }}

    // Render Districts Table
    function renderDistricts(districtsList) {{
      const tbody = document.getElementById('district-table-body');
      let html = '';

      districtsList.forEach(d => {{
        if (d['อำเภอ'] === 'โครงการระดับจังหวัด/ไม่ระบุอำเภอ') return;

        let badgeClass = 'badge-ok';
        if (d['สถานะการจัดสรร (Gap Status)'].includes('วิกฤติ')) badgeClass = 'badge-crisis';
        else if (d['สถานะการจัดสรร (Gap Status)'].includes('เสี่ยงสูง') || d['สถานะการจัดสรร (Gap Status)'].includes('ควรเพิ่ม')) badgeClass = 'badge-warn';
        else if (d['สถานะการจัดสรร (Gap Status)'].includes('งบประมาณสูง')) badgeClass = 'badge-blue';

        html += `
          <tr class="hover:bg-slate-50 transition">
            <td class="p-2.5 font-bold text-slate-900">${{d['อำเภอ']}}</td>
            <td class="p-2.5 text-center text-slate-600">${{d['จำนวนหมู่บ้าน']}}</td>
            <td class="p-2.5 text-center font-bold text-rose-600 bg-rose-50/50">${{d['จำนวนเสี่ยงสูง_รวมทุกด้าน']}}</td>
            <td class="p-2.5"><span class="px-2 py-0.5 rounded-full text-[11px] font-semibold ${{badgeClass}}">${{d['สถานะการจัดสรร (Gap Status)']}}</span></td>
            <td class="p-2.5 text-right font-bold text-slate-900">${{Number(d['งบประมาณรวม (ล้านบาท)']).toLocaleString(undefined, {{minimumFractionDigits: 1, maximumFractionDigits: 1}})}}</td>
            <td class="p-2.5 text-right font-medium text-slate-700">${{d['จำนวนโครงการรวม']}}</td>
            <td class="p-2.5 text-center text-slate-600">${{d['เสี่ยงสูง_ด1_อุปโภค'] > 0 ? '<span class="text-rose-600 font-bold">' + d['เสี่ยงสูง_ด1_อุปโภค'] + '</span>' : '-'}}</td>
            <td class="p-2.5 text-center text-slate-600">${{d['เสี่ยงสูง_ด2_เกษตร'] > 0 ? '<span class="text-rose-600 font-bold">' + d['เสี่ยงสูง_ด2_เกษตร'] + '</span>' : '-'}}</td>
            <td class="p-2.5 text-center text-slate-600">${{d['เสี่ยงสูง_ด3_น้ำท่วม'] > 0 ? '<span class="text-rose-600 font-bold">' + d['เสี่ยงสูง_ด3_น้ำท่วม'] + '</span>' : '-'}}</td>
            <td class="p-2.5 text-center text-slate-600">${{d['เสี่ยงสูง_ด4_คุณภาพน้ำ'] > 0 ? '<span class="text-rose-600 font-bold">' + d['เสี่ยงสูง_ด4_คุณภาพน้ำ'] + '</span>' : '-'}}</td>
            <td class="p-2.5 text-center text-slate-600">${{d['เสี่ยงสูง_ด5_ป่าต้นน้ำ'] > 0 ? '<span class="text-rose-600 font-bold">' + d['เสี่ยงสูง_ด5_ป่าต้นน้ำ'] + '</span>' : '-'}}</td>
          </tr>
        `;
      }});

      tbody.innerHTML = html;
    }}

    function filterDistricts() {{
      const q = document.getElementById('district-search').value.trim().toLowerCase();
      const sort = document.getElementById('district-sort').value;
      
      let list = data.districts.filter(d => d['อำเภอ'].toLowerCase().includes(q));
      
      if (sort === 'high_risk_desc') {{
        list.sort((a, b) => b['จำนวนเสี่ยงสูง_รวมทุกด้าน'] - a['จำนวนเสี่ยงสูง_รวมทุกด้าน']);
      }} else if (sort === 'budget_desc') {{
        list.sort((a, b) => b['งบประมาณรวม (ล้านบาท)'] - a['งบประมาณรวม (ล้านบาท)']);
      }} else if (sort === 'budget_asc') {{
        list.sort((a, b) => a['งบประมาณรวม (ล้านบาท)'] - b['งบประมาณรวม (ล้านบาท)']);
      }} else if (sort === 'name_asc') {{
        list.sort((a, b) => a['อำเภอ'].localeCompare(b['อำเภอ'], 'th'));
      }}
      
      renderDistricts(list);
    }}

    // Render Year & Agency
    function renderYearAndAgency() {{
      const yContainer = document.getElementById('yearly-bars');
      const maxYearBudget = Math.max(...data.years.map(y => y.budget));
      let yHtml = '';

      data.years.forEach(y => {{
        const pctWidth = ((y.budget / maxYearBudget) * 100).toFixed(0);
        yHtml += `
          <div>
            <div class="flex justify-between text-xs font-semibold text-slate-700 mb-1">
              <span>ปีงบประมาณ ${{y.year}}</span>
              <span>${{y.budget.toLocaleString(undefined, {{minimumFractionDigits: 1, maximumFractionDigits: 1}})}} ลบ. (${{y.projects.toLocaleString()}} โครงการ)</span>
            </div>
            <div class="w-full bg-slate-100 rounded-full h-3 overflow-hidden">
              <div class="bg-gradient-to-r from-blue-500 to-indigo-600 h-3 rounded-full" style="width: ${{pctWidth}}%"></div>
            </div>
          </div>
        `;
      }});
      yContainer.innerHTML = yHtml;

      const aContainer = document.getElementById('agency-bars');
      const maxAgencyBudget = Math.max(...data.agencies.map(a => a['งบประมาณ_ล้านบาท']));
      let aHtml = '';

      data.agencies.forEach(a => {{
        const pctWidth = ((a['งบประมาณ_ล้านบาท'] / maxAgencyBudget) * 100).toFixed(0);
        aHtml += `
          <div>
            <div class="flex justify-between text-xs font-semibold text-slate-700 mb-1">
              <span class="truncate max-w-[200px]" title="${{a['หน่วยงานรับผิดชอบ']}}">${{a['หน่วยงานรับผิดชอบ']}}</span>
              <span>${{a['งบประมาณ_ล้านบาท'].toLocaleString(undefined, {{minimumFractionDigits: 1, maximumFractionDigits: 1}})}} ลบ. (${{a['จำนวนโครงการ']}} โครงการ)</span>
            </div>
            <div class="w-full bg-slate-100 rounded-full h-3 overflow-hidden">
              <div class="bg-gradient-to-r from-emerald-500 to-teal-600 h-3 rounded-full" style="width: ${{pctWidth}}%"></div>
            </div>
          </div>
        `;
      }});
      aContainer.innerHTML = aHtml;
    }}

    // Initialize
    renderPillars();
    filterDistricts();
    renderYearAndAgency();
  </script>
</body>
</html>'''

with open('ChiangMai_Water_Dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

artifact_path = '/Users/commindo/.gemini/antigravity/brain/e2040493-6043-4283-af0a-d3d6adad8d8d/water_dashboard.html'
with open(artifact_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Dashboard HTML files generated successfully.')
