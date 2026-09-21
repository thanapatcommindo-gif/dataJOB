import os
import json
import pandas as pd
import numpy as np
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

print("Building Master Excel, Interactive Point GIS Dashboard, and QGIS assets for Household Flood Survey...")

df_hh = pd.read_csv('data_clean_csv/08_ข้อมูลสำรวจน้ำท่วมรายครัวเรือน_Clean.csv')

# -----------------------------------------------------------------------------
# 1. BUILD MASTER EXCEL WORKBOOK
# -----------------------------------------------------------------------------
wb = openpyxl.Workbook()
wb.remove(wb.active)

FONT_NAME = 'Sarabun'
title_font = Font(name=FONT_NAME, size=15, bold=True, color='1E3A8A')
subtitle_font = Font(name=FONT_NAME, size=10, italic=True, color='475569')
section_font = Font(name=FONT_NAME, size=12, bold=True, color='0F172A')
header_font = Font(name=FONT_NAME, size=10, bold=True, color='FFFFFF')

header_fill_navy = PatternFill(start_color='1E3A8A', end_color='1E3A8A', fill_type='solid')
header_fill_rose = PatternFill(start_color='BE123C', end_color='BE123C', fill_type='solid')
header_fill_teal = PatternFill(start_color='0F766E', end_color='0F766E', fill_type='solid')
header_fill_slate = PatternFill(start_color='334155', end_color='334155', fill_type='solid')
header_fill_amber = PatternFill(start_color='B45309', end_color='B45309', fill_type='solid')

kpi_label_font = Font(name=FONT_NAME, size=9, bold=True, color='64748B')
kpi_val_font = Font(name=FONT_NAME, size=17, bold=True, color='0F172A')
kpi_sub_font = Font(name=FONT_NAME, size=9, italic=True, color='059669')

kpi_fill_blue = PatternFill(start_color='EFF6FF', end_color='EFF6FF', fill_type='solid')
kpi_fill_rose = PatternFill(start_color='FFF1F2', end_color='FFF1F2', fill_type='solid')
kpi_fill_amber = PatternFill(start_color='FFFBEB', end_color='FFFBEB', fill_type='solid')
kpi_fill_emerald = PatternFill(start_color='ECFDF5', end_color='ECFDF5', fill_type='solid')

data_font = Font(name=FONT_NAME, size=9)
bold_data_font = Font(name=FONT_NAME, size=9, bold=True)
total_font = Font(name=FONT_NAME, size=10, bold=True, color='0F172A')
total_fill = PatternFill(start_color='F1F5F9', end_color='F1F5F9', fill_type='solid')

thin_border_side = Side(border_style='thin', color='CBD5E1')
thin_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
top_thin_bottom_double = Border(top=Side(border_style='thin', color='94A3B8'), bottom=Side(border_style='double', color='0F172A'))

align_left = Alignment(horizontal='left', vertical='center')
align_right = Alignment(horizontal='right', vertical='center')
align_center = Alignment(horizontal='center', vertical='center')

# SHEET 1: 📊 สรุปผลสำรวจน้ำท่วม 2567
ws_dash = wb.create_sheet(title='📊 สรุปผลสำรวจน้ำท่วม 2567')
ws_dash.views.sheetView[0].showGridLines = True

ws_dash['B2'] = 'แดชบอร์ดสรุปผลสำรวจความเสียหายและกลุ่มเปราะบางน้ำท่วมรายครัวเรือน จ.เชียงใหม่ (ปี 2567)'
ws_dash['B2'].font = title_font
ws_dash['B3'] = 'การวิเคราะห์เจาะลึกรายหลังคาเรือน 4,450 ครัวเรือน ครอบคลุม ทต.หนองหอย, ทน.เชียงใหม่, ทต.ท่าวังตาล และ ทต.หนองผึ้ง'
ws_dash['B3'].font = subtitle_font

# KPI 1: Total Households
ws_dash.merge_cells('B5:C5'); ws_dash.merge_cells('B6:C6'); ws_dash.merge_cells('B7:C7')
ws_dash['B5'] = '🏠 จำนวนครัวเรือนที่สำรวจ'; ws_dash['B5'].font = kpi_label_font; ws_dash['B5'].alignment = align_center; ws_dash['B5'].fill = kpi_fill_blue
ws_dash['B6'] = f"{len(df_hh):,} ครัวเรือน"; ws_dash['B6'].font = kpi_val_font; ws_dash['B6'].alignment = align_center; ws_dash['B6'].fill = kpi_fill_blue
ws_dash['B7'] = '4 เทศบาลแนวริมน้ำปิง'; ws_dash['B7'].font = kpi_sub_font; ws_dash['B7'].alignment = align_center; ws_dash['B7'].fill = kpi_fill_blue

# KPI 2: Total Damages
total_dmg_val = df_hh['มูลค่าความเสียหายรวม_บาท'].sum()
ws_dash.merge_cells('D5:E5'); ws_dash.merge_cells('D6:E6'); ws_dash.merge_cells('D7:E7')
ws_dash['D5'] = '💸 มูลค่าความเสียหายรวม'; ws_dash['D5'].font = kpi_label_font; ws_dash['D5'].alignment = align_center; ws_dash['D5'].fill = kpi_fill_rose
ws_dash['D6'] = f"{total_dmg_val/1e6:,.2f} ล้านบาท"; ws_dash['D6'].font = kpi_val_font; ws_dash['D6'].alignment = align_center; ws_dash['D6'].fill = kpi_fill_rose
ws_dash['D7'] = f"เฉลี่ย {(total_dmg_val/len(df_hh)):,.0f} บาท/ครัวเรือน"; ws_dash['D7'].font = Font(name=FONT_NAME, size=9, italic=True, color='E11D48'); ws_dash['D7'].alignment = align_center; ws_dash['D7'].fill = kpi_fill_rose

# KPI 3: Vulnerable Households
vuln_hh_count = (df_hh['มีกลุ่มเปราะบาง'] == 'มี').sum()
ws_dash.merge_cells('F5:G5'); ws_dash.merge_cells('F6:G6'); ws_dash.merge_cells('F7:G7')
ws_dash['F5'] = '🚨 ครัวเรือนที่มีกลุ่มเปราะบาง'; ws_dash['F5'].font = kpi_label_font; ws_dash['F5'].alignment = align_center; ws_dash['F5'].fill = kpi_fill_amber
ws_dash['F6'] = f"{vuln_hh_count:,} ครัวเรือน"; ws_dash['F6'].font = kpi_val_font; ws_dash['F6'].alignment = align_center; ws_dash['F6'].fill = kpi_fill_amber
ws_dash['F7'] = f"คิดเป็น {(vuln_hh_count/len(df_hh))*100:.1f}% ของผู้ประสบภัย"; ws_dash['F7'].font = Font(name=FONT_NAME, size=9, italic=True, color='B45309'); ws_dash['F7'].alignment = align_center; ws_dash['F7'].fill = kpi_fill_amber

# KPI 4: Bedridden & Severe Cases
bedridden_total = df_hh['ผู้ป่วยติดเตียง_คน'].sum() + df_hh['คนพิการ_คน'].sum()
ws_dash.merge_cells('H5:I5'); ws_dash.merge_cells('H6:I6'); ws_dash.merge_cells('H7:I7')
ws_dash['H5'] = '⚡ ผู้ป่วยติดเตียง / คนพิการ'; ws_dash['H5'].font = kpi_label_font; ws_dash['H5'].alignment = align_center; ws_dash['H5'].fill = kpi_fill_emerald
ws_dash['H6'] = f"{int(bedridden_total):,} คน"; ws_dash['H6'].font = kpi_val_font; ws_dash['H6'].alignment = align_center; ws_dash['H6'].fill = kpi_fill_emerald
ws_dash['H7'] = 'กลุ่มวิกฤติที่ต้องส่งเรือช่วยด่วน'; ws_dash['H7'].font = kpi_sub_font; ws_dash['H7'].alignment = align_center; ws_dash['H7'].fill = kpi_fill_emerald

for col_start, col_end in [('B', 'C'), ('D', 'E'), ('F', 'G'), ('H', 'I')]:
    for r in range(5, 8):
        for c in range(openpyxl.utils.column_index_from_string(col_start), openpyxl.utils.column_index_from_string(col_end)+1):
            ws_dash.cell(row=r, column=c).border = thin_border

# Section 1: Summary Table by Municipality
ws_dash['B9'] = '🏢 สรุปเปรียบเทียบความเสียหายและกลุ่มเปราะบางแยกตาม 4 เทศบาล'
ws_dash['B9'].font = section_font

muni_headers = ['เทศบาล', 'อำเภอ', 'ครัวเรือนสำรวจ', 'เสียหายรวม (ลบ.)', 'เฉลี่ย/ครัวเรือน (บาท)', 'กลุ่มเปราะบาง (ครัวเรือน)', 'ผู้ป่วยติดเตียง/พิการ (คน)', 'ผู้สูงอายุ (คน)', 'ระดับน้ำเฉลี่ย (ม.)']
for col_idx, h in enumerate(muni_headers, start=2):
    cell = ws_dash.cell(row=10, column=col_idx, value=h)
    cell.font = header_font; cell.fill = header_fill_navy; cell.alignment = align_center; cell.border = thin_border

muni_summary = df_hh.groupby(['เทศบาล', 'อำเภอ']).agg({
    'รหัสผู้ตอบ': 'count',
    'มูลค่าความเสียหายรวม_บาท': ['sum', 'mean'],
    'มีกลุ่มเปราะบาง': lambda x: (x == 'มี').sum(),
    'ผู้ป่วยติดเตียง_คน': 'sum',
    'ผู้สูงอายุ_คน': 'sum',
    'ระดับน้ำท่วม_เมตร': 'mean'
}).reset_index()
muni_summary.columns = ['เทศบาล', 'อำเภอ', 'ครัวเรือน', 'เสียหายรวม_บาท', 'เฉลี่ย_บาท', 'เปราะบาง_ครัวเรือน', 'ติดเตียง_คน', 'ผู้สูงอายุ_คน', 'ระดับน้ำ_เมตร']

for row_idx, (_, r) in enumerate(muni_summary.iterrows(), start=11):
    vals = [r['เทศบาล'], r['อำเภอ'], r['ครัวเรือน'], r['เสียหายรวม_บาท'] / 1e6, r['เฉลี่ย_บาท'], r['เปราะบาง_ครัวเรือน'], r['ติดเตียง_คน'], r['ผู้สูงอายุ_คน'], r['ระดับน้ำ_เมตร']]
    for col_idx, val in enumerate(vals, start=2):
        cell = ws_dash.cell(row=row_idx, column=col_idx, value=val)
        cell.font = data_font; cell.border = thin_border
        if col_idx in [2, 3]: cell.alignment = align_left
        elif col_idx in [4, 7, 8, 9]: cell.alignment = align_right; cell.number_format = '#,##0'
        elif col_idx == 5: cell.alignment = align_right; cell.number_format = '#,##0.00'
        elif col_idx == 6: cell.alignment = align_right; cell.number_format = '#,##0'
        elif col_idx == 10: cell.alignment = align_right; cell.number_format = '0.00'

# Total Row
ws_dash.merge_cells('B15:C15'); ws_dash['B15'] = 'รวมทั้งสิ้น'
ws_dash['B15'].font = total_font; ws_dash['B15'].alignment = align_center; ws_dash['B15'].fill = total_fill; ws_dash['C15'].fill = total_fill
ws_dash['D15'] = f"=SUM(D11:D14)"; ws_dash['D15'].font = total_font; ws_dash['D15'].alignment = align_right; ws_dash['D15'].number_format = '#,##0'; ws_dash['D15'].fill = total_fill
ws_dash['E15'] = f"=SUM(E11:E14)"; ws_dash['E15'].font = total_font; ws_dash['E15'].alignment = align_right; ws_dash['E15'].number_format = '#,##0.00'; ws_dash['E15'].fill = total_fill
ws_dash['F15'] = f"=(E15*1000000)/D15"; ws_dash['F15'].font = total_font; ws_dash['F15'].alignment = align_right; ws_dash['F15'].number_format = '#,##0'; ws_dash['F15'].fill = total_fill
ws_dash['G15'] = f"=SUM(G11:G14)"; ws_dash['G15'].font = total_font; ws_dash['G15'].alignment = align_right; ws_dash['G15'].number_format = '#,##0'; ws_dash['G15'].fill = total_fill
ws_dash['H15'] = f"=SUM(H11:H14)"; ws_dash['H15'].font = total_font; ws_dash['H15'].alignment = align_right; ws_dash['H15'].number_format = '#,##0'; ws_dash['H15'].fill = total_fill
ws_dash['I15'] = f"=SUM(I11:I14)"; ws_dash['I15'].font = total_font; ws_dash['I15'].alignment = align_right; ws_dash['I15'].number_format = '#,##0'; ws_dash['I15'].fill = total_fill
ws_dash['J15'] = f"=AVERAGE(J11:J14)"; ws_dash['J15'].font = total_font; ws_dash['J15'].alignment = align_right; ws_dash['J15'].number_format = '0.00'; ws_dash['J15'].fill = total_fill

for c in range(2, 11): ws_dash.cell(row=15, column=c).border = top_thin_bottom_double

# Section 2: Damage Breakdown by Asset Type
ws_dash['B17'] = '💸 สรุปความเสียหายแยกตามประเภททรัพย์สิน (รวม 4 เทศบาล)'
ws_dash['B17'].font = section_font

dmg_headers = ['ประเภททรัพย์สินที่เสียหาย', 'มูลค่าความเสียหาย (ล้านบาท)', 'สัดส่วน (%)', 'จำนวนครัวเรือนที่เสียหาย']
for col_idx, h in enumerate(dmg_headers, start=2):
    cell = ws_dash.cell(row=18, column=col_idx, value=h)
    cell.font = header_font; cell.fill = header_fill_slate; cell.alignment = align_center; cell.border = thin_border

dmg_items = [
    ['ตัวบ้านและโครงสร้างที่อยู่อาศัย', df_hh['ความเสียหาย_ที่อยู่อาศัย_บาท'].sum(), (df_hh['ความเสียหาย_ที่อยู่อาศัย_บาท'] > 0).sum()],
    ['เฟอร์นิเจอร์และเครื่องใช้ไฟฟ้า', df_hh['ความเสียหาย_เครื่องใช้ไฟฟ้า_บาท'].sum(), (df_hh['ความเสียหาย_เครื่องใช้ไฟฟ้า_บาท'] > 0).sum()],
    ['รถยนต์และยานพาหนะจมน้ำ', df_hh['ความเสียหาย_รถยนต์_บาท'].sum(), (df_hh['ความเสียหาย_รถยนต์_บาท'] > 0).sum()],
    ['การขาดรายได้ช่วงน้ำท่วม', df_hh['ความเสียหาย_การขาดรายได้_บาท'].sum(), (df_hh['ความเสียหาย_การขาดรายได้_บาท'] > 0).sum()],
    ['สัตว์เลี้ยงและทรัพย์สินอื่นๆ', df_hh['ความเสียหาย_สัตว์เลี้ยง_บาท'].sum() + df_hh['ความเสียหาย_อื่นๆ_บาท'].sum(), ((df_hh['ความเสียหาย_สัตว์เลี้ยง_บาท'] + df_hh['ความเสียหาย_อื่นๆ_บาท']) > 0).sum()]
]

tot_dmg_sum = sum([x[1] for x in dmg_items])
for row_idx, item in enumerate(dmg_items, start=19):
    ws_dash.cell(row=row_idx, column=2, value=item[0]).font = data_font; ws_dash.cell(row=row_idx, column=2).border = thin_border
    c3 = ws_dash.cell(row=row_idx, column=3, value=item[1]/1e6); c3.font = data_font; c3.alignment = align_right; c3.number_format = '#,##0.00'; c3.border = thin_border
    c4 = ws_dash.cell(row=row_idx, column=4, value=item[1]/tot_dmg_sum if tot_dmg_sum > 0 else 0); c4.font = data_font; c4.alignment = align_right; c4.number_format = '0.0%'; c4.border = thin_border
    c5 = ws_dash.cell(row=row_idx, column=5, value=item[2]); c5.font = data_font; c5.alignment = align_right; c5.number_format = '#,##0'; c5.border = thin_border

# Section 3: 3 Weirs Opinion
ws_dash['G17'] = '🌊 ความคิดเห็นของประชาชนเรื่องการรื้อถอน 3 ฝาย'
ws_dash['G17'].font = section_font

weir_headers = ['ความคิดเห็นต่อ 3 ฝาย', 'จำนวนครัวเรือน', 'สัดส่วน (%)']
for col_idx, h in enumerate(weir_headers, start=7):
    cell = ws_dash.cell(row=18, column=col_idx, value=h)
    cell.font = header_font; cell.fill = header_fill_teal; cell.alignment = align_center; cell.border = thin_border

weir_counts = df_hh['ความเห็น_3_ฝาย'].value_counts()
for row_idx, (k, v) in enumerate(weir_counts.items(), start=19):
    ws_dash.cell(row=row_idx, column=7, value=k).font = data_font; ws_dash.cell(row=row_idx, column=7).border = thin_border
    c8 = ws_dash.cell(row=row_idx, column=8, value=v); c8.font = data_font; c8.alignment = align_right; c8.number_format = '#,##0'; c8.border = thin_border
    c9 = ws_dash.cell(row=row_idx, column=9, value=v/len(df_hh)); c9.font = data_font; c9.alignment = align_right; c9.number_format = '0.0%'; c9.border = thin_border

# Helper to write generic DataFrames to sheets
def write_df_sheet(ws, df, header_fill):
    ws.views.sheetView[0].showGridLines = True
    for col_idx, col_name in enumerate(df.columns, start=1):
        cell = ws.cell(row=1, column=col_idx, value=col_name)
        cell.font = header_font; cell.fill = header_fill; cell.alignment = align_center; cell.border = thin_border
    for row_idx, row_data in enumerate(df.values, start=2):
        for col_idx, val in enumerate(row_data, start=1):
            col_name = df.columns[col_idx - 1]
            cell = ws.cell(row=row_idx, column=col_idx, value=val if pd.notna(val) else '')
            cell.font = data_font; cell.border = thin_border
            if 'บาท' in col_name or 'เงิน' in col_name or 'รายได้' in col_name:
                cell.alignment = align_right; cell.number_format = '#,##0'
            elif 'คน' in col_name or 'จำนวน' in col_name or 'อายุ' in col_name:
                cell.alignment = align_right; cell.number_format = '#,##0'
            elif 'เมตร' in col_name or 'Latitude' in col_name or 'Longitude' in col_name:
                cell.alignment = align_right; cell.number_format = '#,##0.00'
            elif '🚨' in str(val) or '⚠️' in str(val):
                cell.alignment = align_left; cell.font = bold_data_font
            else:
                cell.alignment = align_left
    ws.freeze_panes = 'A2'

# SHEET 2: 🚨 ครัวเรือนกลุ่มเปราะบางวิกฤติ
df_vuln = df_hh[df_hh['ระดับความเร่งด่วน'].str.contains('วิกฤติ|เฝ้าระวัง')].sort_values(by=['ผู้ป่วยติดเตียง_คน', 'ระดับน้ำท่วม_เมตร', 'มูลค่าความเสียหายรวม_บาท'], ascending=False)
ws_vuln = wb.create_sheet(title='🚨 ครัวเรือนกลุ่มเปราะบางวิกฤติ')
write_df_sheet(ws_vuln, df_vuln, header_fill_rose)

# SHEET 3: 💰 สรุปความเสียหายรายเทศบาล
ws_muni_sheet = wb.create_sheet(title='💰 สรุปความเสียหายรายเทศบาล')
write_df_sheet(ws_muni_sheet, muni_summary, header_fill_navy)

# SHEET 4: 📋 Data_สำรวจรายครัวเรือน (Clean)
ws_data = wb.create_sheet(title='📋 Data_สำรวจรายครัวเรือน')
write_df_sheet(ws_data, df_hh, header_fill_slate)

# Adjust column widths
for sheet in wb.worksheets:
    for col in sheet.columns:
        max_len = max([len(str(cell.value or '')) for cell in col] or [0])
        col_letter = get_column_letter(col[0].column)
        sheet.column_dimensions[col_letter].width = max(min(max_len + 3, 45), 11)

master_survey_excel = 'ChiangMai_Flood_Household_Survey_Dashboard.xlsx'
wb.save(master_survey_excel)
print(f"Master Household Survey Excel saved as: {master_survey_excel}")

# -----------------------------------------------------------------------------
# 2. BUILD INTERACTIVE HOUSEHOLD POINT GIS DASHBOARD (HTML)
# -----------------------------------------------------------------------------
# Prepare sample payload (top 1,500 points for ultra-fast browser rendering + full summary stats)
with open('chiangmai_flood_households_gis.geojson', 'r', encoding='utf-8') as f:
    geo_hh = json.load(f)

geo_hh_str = json.dumps(geo_hh, ensure_ascii=False)

html_gis_hh = """<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ระบบแผนที่ GIS รายครัวเรือนผู้ประสบภัยน้ำท่วม เชียงใหม่ 2567</title>
  
  <!-- Tailwind CSS -->
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  
  <!-- Leaflet CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  
  <!-- Leaflet MarkerCluster -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" />
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" />
  <script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>

  <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  
  <style>
    body { font-family: 'Sarabun', sans-serif; }
    .map-container { height: calc(100vh - 190px); min-height: 520px; }
    .map-container-dual { height: calc(100vh - 230px); min-height: 480px; }
    
    .badge-crisis { background-color: #FEE2E2; color: #991B1B; border: 1px solid #FCA5A5; }
    .badge-warn { background-color: #FEF3C7; color: #92400E; border: 1px solid #FCD34D; }
    .badge-ok { background-color: #D1FAE5; color: #065F46; border: 1px solid #6EE7B7; }
  </style>
</head>
<body class="bg-slate-100 text-slate-800 antialiased min-h-screen flex flex-col">

  <!-- Header -->
  <header class="bg-slate-900 text-white border-b border-slate-800 sticky top-0 z-50 shadow-md">
    <div class="max-w-7xl mx-auto px-4 py-3 flex flex-col md:flex-row md:items-center justify-between gap-3">
      
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-rose-600 to-amber-500 flex items-center justify-center text-xl shadow-inner">
          📍
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="font-bold text-lg text-white">ระบบแผนที่ GIS พิกัดบ้านผู้ประสบภัยน้ำท่วม 2567 (เชียงใหม่)</h1>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-rose-500/20 text-rose-300 border border-rose-400/30">Household Point GIS (4,450 หลัง)</span>
          </div>
          <p class="text-xs text-slate-400">เจาะลึกกลุ่มเปราะบาง (ผู้ป่วยติดเตียง/คนชรา) • ระดับน้ำท่วม • ความเสียหายรายหลังคาเรือน (หนองหอย, นครเชียงใหม่, ท่าวังตาล, หนองผึ้ง)</p>
        </div>
      </div>

      <div class="flex items-center bg-slate-800/90 p-1 rounded-xl border border-slate-700/60 overflow-x-auto">
        <button onclick="navigateView('view-map')" id="nav-btn-map" class="nav-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-2 transition bg-blue-600 text-white shadow">
          <span>🗺️ แผนที่พิกัดบ้าน (Point GIS)</span>
        </button>
        <button onclick="navigateView('view-dual')" id="nav-btn-dual" class="nav-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-2 transition text-slate-400 hover:text-white hover:bg-slate-700/50">
          <span>🔄 เปรียบเทียบ 2 แผนที่ (กลุ่มเปราะบาง vs ความเสียหาย)</span>
        </button>
        <button onclick="navigateView('view-table')" id="nav-btn-table" class="nav-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-2 transition text-slate-400 hover:text-white hover:bg-slate-700/50">
          <span>📋 สรุปข้อมูล & ดาวน์โหลด</span>
        </button>
      </div>

    </div>
  </header>

  <!-- VIEW 1: SINGLE POINT GIS WITH SEARCH & DOSSIER -->
  <section id="view-map" class="flex-1 max-w-7xl w-full mx-auto p-4 flex flex-col space-y-3">
    
    <!-- Controls Bar -->
    <div class="bg-white p-3.5 rounded-2xl border border-slate-200 shadow-sm flex flex-col lg:flex-row lg:items-center justify-between gap-3">
      
      <!-- Filters -->
      <div class="flex flex-wrap items-center gap-2 text-xs">
        <input type="text" id="hh-search" oninput="filterPoints()" placeholder="🔍 ค้นหาบ้านเลขที่ / ชื่อ / ชุมชน..." class="px-3 py-1.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none w-56">
        
        <select id="hh-muni-filter" onchange="filterPoints()" class="px-3 py-1.5 font-semibold bg-slate-50 border border-slate-300 rounded-lg outline-none">
          <option value="all">🏢 ทุกเทศบาล (4,450 หลัง)</option>
          <option value="ท่าวังตาล">ทต.ท่าวังตาล (2,230 หลัง)</option>
          <option value="หนองหอย">ทต.หนองหอย (957 หลัง)</option>
          <option value="นครเชียงใหม่">ทน.เชียงใหม่ (771 หลัง)</option>
          <option value="หนองผึ้ง">ทต.หนองผึ้ง (492 หลัง)</option>
        </select>

        <select id="hh-vuln-filter" onchange="filterPoints()" class="px-3 py-1.5 font-semibold bg-slate-50 border border-slate-300 rounded-lg outline-none">
          <option value="all">⚡ ทุกสถานะกลุ่มเปราะบาง</option>
          <option value="bedridden">🚨 ผู้ป่วยติดเตียง / คนพิการ</option>
          <option value="elderly">👴 มีผู้สูงอายุในบ้าน</option>
          <option value="deep_water">🌊 น้ำท่วมสูง (> 1.2 เมตร)</option>
          <option value="critical">🚨 วิกฤติด่วนที่สุด</option>
        </select>

        <button onclick="resetMapFilter()" class="px-2.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg border border-slate-300">
          รีเซ็ต
        </button>
      </div>

      <!-- Quick Counter -->
      <div class="flex items-center gap-3 text-xs">
        <span class="text-slate-500">แสดงผล:</span>
        <strong id="hh-count-display" class="text-blue-600 font-bold text-sm">4,450 หลังคาเรือน</strong>
      </div>

    </div>

    <!-- Map & Sidebar Layout -->
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-4 flex-1">
      
      <!-- Map Area (3 Cols) -->
      <div class="lg:col-span-3 bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden relative">
        <div id="map-point" class="map-container w-full"></div>
      </div>

      <!-- Household Dossier Drawer (1 Col) -->
      <div class="lg:col-span-1 bg-white rounded-2xl border border-slate-200 shadow-sm p-4 flex flex-col justify-between overflow-y-auto max-h-[600px]">
        <div>
          <div class="flex items-center justify-between pb-3 border-b border-slate-100">
            <h3 class="font-bold text-slate-900 text-sm flex items-center gap-1.5">
              <span>🏠 ประวัติหลังคาเรือน</span>
            </h3>
            <span id="hh-dossier-urgency" class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">-</span>
          </div>

          <div class="mt-3">
            <div id="hh-dossier-id" class="text-xs font-bold text-blue-600">คลิกที่หมุดบ้านบนแผนที่</div>
            <div id="hh-dossier-name" class="text-lg font-bold text-slate-900 mt-0.5">เลือกหลังคาเรือนเพื่อดูข้อมูล</div>
            <div id="hh-dossier-address" class="text-xs text-slate-500 mt-0.5">-</div>
          </div>

          <!-- Metrics Box -->
          <div class="mt-4 space-y-2 text-xs">
            <div class="p-2.5 rounded-xl bg-rose-50 border border-rose-100">
              <div class="text-rose-700 font-bold mb-1">🌊 ระดับน้ำและผลกระทบ</div>
              <div class="flex justify-between text-slate-700">
                <span>ระดับน้ำท่วม:</span>
                <strong id="hh-dossier-depth" class="text-rose-900">-</strong>
              </div>
              <div class="flex justify-between text-slate-700 mt-0.5">
                <span>การตัดสินใจ:</span>
                <strong id="hh-dossier-decision">-</strong>
              </div>
            </div>

            <div class="p-2.5 rounded-xl bg-amber-50 border border-amber-100">
              <div class="text-amber-800 font-bold mb-1">🚨 สมาชิกกลุ่มเปราะบาง</div>
              <div class="flex justify-between text-slate-700">
                <span>ผู้ป่วยติดเตียง:</span>
                <strong id="hh-dossier-bedridden" class="text-amber-900">-</strong>
              </div>
              <div class="flex justify-between text-slate-700 mt-0.5">
                <span>ผู้สูงอายุ:</span>
                <strong id="hh-dossier-elderly">-</strong>
              </div>
              <div class="flex justify-between text-slate-700 mt-0.5">
                <span>คนพิการ:</span>
                <strong id="hh-dossier-disabled">-</strong>
              </div>
            </div>

            <div class="p-2.5 rounded-xl bg-emerald-50 border border-emerald-100">
              <div class="text-emerald-800 font-bold mb-1">💰 มูลค่าความเสียหาย</div>
              <div class="flex justify-between text-slate-700">
                <span>เสียหายรวม:</span>
                <strong id="hh-dossier-damage" class="text-emerald-900 font-bold text-sm">-</strong>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-4 pt-3 border-t border-slate-100 text-center">
          <div class="text-xs text-slate-500">📞 เบอร์ติดต่อฉุกเฉิน:</div>
          <div id="hh-dossier-phone" class="text-sm font-bold text-slate-900 mt-0.5">-</div>
        </div>
      </div>

    </div>

  </section>

  <!-- VIEW 2: DUAL SYNCED POINT MAP -->
  <section id="view-dual" class="flex-1 max-w-7xl w-full mx-auto p-4 hidden flex flex-col space-y-3">
    <div class="bg-white p-3 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between text-xs">
      <div class="flex items-center gap-2">
        <span class="text-lg">⚖️</span>
        <span class="font-bold text-slate-800">เปรียบเทียบเชิงพื้นที่: ซ้าย (กลุ่มเปราะบาง & ระดับน้ำ) vs ขวา (มูลค่าความเสียหาย)</span>
      </div>
      <span class="text-slate-500">ซูมหรือเลื่อนแผนที่ทั้ง 2 ฝั่งจะขยับตามกันอัตโนมัติ</span>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 flex-1">
      <!-- Dual Map Left -->
      <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
        <div class="px-4 py-2 bg-rose-50 border-b border-rose-100 text-xs font-bold text-rose-900 flex justify-between">
          <span>1. แผนที่ตำแหน่งกลุ่มเปราะบาง (แดง=ติดเตียง, ส้ม=คนชรา, ฟ้า=ทั่วไป)</span>
        </div>
        <div id="map-dual-left" class="map-container-dual flex-1"></div>
      </div>
      <!-- Dual Map Right -->
      <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
        <div class="px-4 py-2 bg-emerald-50 border-b border-emerald-100 text-xs font-bold text-emerald-900 flex justify-between">
          <span>2. แผนที่มูลค่าความเสียหาย (ขนาดหมุด = ความเสียหายบาท)</span>
        </div>
        <div id="map-dual-right" class="map-container-dual flex-1"></div>
      </div>
    </div>
  </section>

  <!-- VIEW 3: SUMMARY TABLE -->
  <section id="view-table" class="flex-1 max-w-7xl w-full mx-auto p-4 hidden flex flex-col space-y-4">
    <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
      <div>
        <h2 class="font-bold text-slate-900 text-base">ตารางสรุปผลสำรวจน้ำท่วมรายครัวเรือน 4,450 หลัง</h2>
        <p class="text-xs text-slate-500 mt-0.5">ดาวน์โหลดข้อมูลฉบับสมบูรณ์เพื่อนำไปเปิดใน Google Sheets หรือโปรแกรม GIS</p>
      </div>
      <a href="ChiangMai_Flood_Household_Survey_Dashboard.xlsx" download class="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl text-xs shadow transition flex items-center gap-2">
        <span>📥 ดาวน์โหลด Excel สำรวจครัวเรือน (Clean)</span>
      </a>
    </div>

    <!-- Municipality Summary Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="bg-white p-4 rounded-xl border border-slate-200">
        <div class="text-xs font-bold text-blue-600">ทต.ท่าวังตาล (อ.สารภี)</div>
        <div class="text-xl font-bold text-slate-900 mt-1">2,230 ครัวเรือน</div>
        <div class="text-xs text-slate-500 mt-1">มีพิกัด GPS จริง 867 จุด</div>
      </div>
      <div class="bg-white p-4 rounded-xl border border-slate-200">
        <div class="text-xs font-bold text-emerald-600">ทต.หนองหอย (อ.เมือง)</div>
        <div class="text-xl font-bold text-slate-900 mt-1">957 ครัวเรือน</div>
        <div class="text-xs text-slate-500 mt-1">พื้นที่ริมแม่น้ำปิง</div>
      </div>
      <div class="bg-white p-4 rounded-xl border border-slate-200">
        <div class="text-xs font-bold text-purple-600">ทน.เชียงใหม่ (อ.เมือง)</div>
        <div class="text-xl font-bold text-slate-900 mt-1">771 ครัวเรือน</div>
        <div class="text-xs text-slate-500 mt-1">ชุมชนวัดเกต / ช้างคลาน</div>
      </div>
      <div class="bg-white p-4 rounded-xl border border-slate-200">
        <div class="text-xs font-bold text-amber-600">ทต.หนองผึ้ง (อ.สารภี)</div>
        <div class="text-xl font-bold text-slate-900 mt-1">492 ครัวเรือน</div>
        <div class="text-xs text-slate-500 mt-1">น้ำท่วมลึกเฉลี่ย 1.8 เมตร</div>
      </div>
    </div>
  </section>

  <!-- Script Logic -->
  <script>
    const geojsonData = __GEOJSON_DATA__;

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

      setTimeout(() => {
        if (mapPoint) mapPoint.invalidateSize();
        if (mapDualLeft) mapDualLeft.invalidateSize();
        if (mapDualRight) mapDualRight.invalidateSize();
      }, 100);
    }

    let mapPoint, clusterGroup;
    let mapDualLeft, mapDualRight, dualLeftLayer, dualRightLayer;
    let isDualSyncing = false;

    const CENTER_COORD = [18.7500, 99.0050];

    function initPointMap() {
      mapPoint = L.map('map-point').setView(CENTER_COORD, 12);
      L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', { maxZoom: 18 }).addTo(mapPoint);

      clusterGroup = L.markerClusterGroup({
        chunkedLoading: true,
        maxClusterRadius: 40,
        spiderfyOnMaxZoom: true
      });

      renderMarkers(geojsonData.features);
      mapPoint.addLayer(clusterGroup);
    }

    function getMarkerColor(props) {
      if (props.bedridden > 0 || props.disabled > 0) return '#dc2626'; // Red
      if (props.elderly > 0) return '#f59e0b'; // Amber
      if (props.depth_m >= 1.2) return '#ea580c'; // Orange
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

        marker.bindTooltip(`<strong>${p.name}</strong> (${p.id})<br>บ้านเลขที่: ${p.house_no} ม.${p.village}<br>น้ำท่วม: ${p.depth_lvl}`, {
          direction: 'top'
        });

        marker.on('click', () => populateDossier(p));
        clusterGroup.addLayer(marker);
      });

      document.getElementById('hh-count-display').innerText = `${featuresList.length.toLocaleString()} หลังคาเรือน`;
    }

    function populateDossier(p) {
      document.getElementById('hh-dossier-id').innerText = `${p.id} | ${p.muni}`;
      document.getElementById('hh-dossier-name').innerText = p.name;
      document.getElementById('hh-dossier-address').innerText = `บ้านเลขที่ ${p.house_no} หมู่ ${p.village} ต.${p.subdist} อ.${p.dist}`;
      document.getElementById('hh-dossier-urgency').innerText = p.urgency.split(' ')[0] + ' ' + (p.urgency.includes('วิกฤติ') ? 'วิกฤติ' : 'เฝ้าระวัง');
      
      document.getElementById('hh-dossier-depth').innerText = `${p.depth_m > 0 ? p.depth_m + ' ม. ' : ''}(${p.depth_lvl})`;
      document.getElementById('hh-dossier-decision').innerText = p.decision;
      
      document.getElementById('hh-dossier-bedridden').innerText = `${p.bedridden} คน`;
      document.getElementById('hh-dossier-elderly').innerText = `${p.elderly} คน`;
      document.getElementById('hh-dossier-disabled').innerText = `${p.disabled} คน`;
      
      document.getElementById('hh-dossier-damage').innerText = `${Number(p.damage_thb).toLocaleString()} บาท`;
      document.getElementById('hh-dossier-phone').innerText = p.phone || '-';
    }

    function filterPoints() {
      const q = document.getElementById('hh-search').value.trim().toLowerCase();
      const muni = document.getElementById('hh-muni-filter').value;
      const vuln = document.getElementById('hh-vuln-filter').value;

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

    function resetMapFilter() {
      document.getElementById('hh-search').value = '';
      document.getElementById('hh-muni-filter').value = 'all';
      document.getElementById('hh-vuln-filter').value = 'all';
      renderMarkers(geojsonData.features);
    }

    // Dual Map Setup
    function initDualMaps() {
      mapDualLeft = L.map('map-dual-left', { zoomControl: true, attributionControl: false }).setView(CENTER_COORD, 12);
      L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png').addTo(mapDualLeft);

      mapDualRight = L.map('map-dual-right', { zoomControl: true, attributionControl: false }).setView(CENTER_COORD, 12);
      L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png').addTo(mapDualRight);

      // Sync
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

      // Populate dual layers
      geojsonData.features.forEach(f => {
        const p = f.properties;
        // Left: Vulnerability
        L.circleMarker([f.geometry.coordinates[1], f.geometry.coordinates[0]], {
          radius: 5,
          fillColor: getMarkerColor(p),
          color: '#ffffff',
          weight: 1,
          fillOpacity: 0.85
        }).bindTooltip(`${p.name}<br>${p.urgency}`).addTo(mapDualLeft);

        // Right: Damage (size based on damage)
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

full_hh_html = html_gis_hh.replace('__GEOJSON_DATA__', geo_hh_str)
with open('ChiangMai_Flood_Household_GIS_Dashboard.html', 'w', encoding='utf-8') as f:
    f.write(full_hh_html)

# Also save to brain artifact dir
artifact_hh_path = '/Users/commindo/.gemini/antigravity/brain/e2040493-6043-4283-af0a-d3d6adad8d8d/flood_household_gis_dashboard.html'
with open(artifact_hh_path, 'w', encoding='utf-8') as f:
    f.write(full_hh_html)

print("Interactive Point GIS Dashboard saved as: ChiangMai_Flood_Household_GIS_Dashboard.html")

# -----------------------------------------------------------------------------
# 3. BUILD QGIS PROJECT FOR HOUSEHOLD POINTS
# -----------------------------------------------------------------------------
geojson_hh_abs = os.path.abspath('chiangmai_flood_households_gis.geojson')

qgis_hh_xml = f'''<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis projectname="ChiangMai_Flood_Household_Survey_QGIS" version="3.28.0">
  <homePath path=""/>
  <title>แผนที่ GIS พิกัดบ้านผู้ประสบภัยน้ำท่วม 2567 (4,450 ครัวเรือน)</title>
  <projectCrs>
    <spatialrefsys nativeFormat="Wkt">
      <wkt>GEOGCRS["WGS 84",DATUM["World Geodetic System 1984",ELLIPSOID["WGS 84",6378137,298.257223563,LENGTHUNIT["metre",1]]],PRIMEM["Greenwich",0,ANGLEUNIT["degree",0.0174532925199433]],CS[ellipsoidal,2],AXIS["geodetic latitude (Lat)",north,ORDER[1],ANGLEUNIT["degree",0.0174532925199433]],AXIS["geodetic longitude (Lon)",east,ORDER[2],ANGLEUNIT["degree",0.0174532925199433]],ID["EPSG",4326]]</wkt>
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
    <layer-tree-layer id="layer_hh_points" name="📍 พิกัดบ้านผู้ประสบภัย 4,450 ครัวเรือน" source="{geojson_hh_abs}|layername=chiangmai_flood_households_gis" providerKey="ogr" checked="Qt::Checked" expanded="1"/>
  </layer-tree-group>
  <maplayers>
    <maplayer id="layer_hh_points" type="vector" geometry="Point" minScale="1e+08" maxScale="0" refreshOnNotifyEnabled="0" styleCategories="AllStyleCategories">
      <id>layer_hh_points</id>
      <datasource>{geojson_hh_abs}|layername=chiangmai_flood_households_gis</datasource>
      <layername>📍 พิกัดบ้านผู้ประสบภัย 4,450 ครัวเรือน</layername>
      <srs>
        <spatialrefsys nativeFormat="Wkt">
          <authid>EPSG:4326</authid>
          <description>WGS 84</description>
        </spatialrefsys>
      </srs>
      <provider encoding="UTF-8">ogr</provider>
      <renderer-v2 attr="urgency" type="categorizedSymbol" enableorderby="0">
        <categories>
          <category symbol="0" value="🚨 วิกฤติด่วนที่สุด (ผู้ป่วยติดเตียง/น้ำท่วมสูงมาก)" label="🚨 วิกฤติด่วนที่สุด (ผู้ป่วยติดเตียง/น้ำท่วมสูง)" render="true"/>
          <category symbol="1" value="⚠️ เฝ้าระวังสูง (มีกลุ่มเปราะบาง/น้ำท่วมสูง)" label="⚠️ เฝ้าระวังสูง (คนชรา/น้ำท่วมสูง)" render="true"/>
          <category symbol="2" value="🟡 ได้รับผลกระทบปานกลาง" label="🟡 ผลกระทบปานกลาง" render="true"/>
          <category symbol="3" value="🟢 ผลกระทบน้อย/ปกติ" label="🟢 ผลกระทบน้อย/ปกติ" render="true"/>
        </categories>
        <symbols>
          <symbol name="0" type="marker" alpha="0.9" clip_to_extent="1">
            <layer class="SimpleMarker" pass="0" locked="0">
              <prop k="color" v="220,38,38,255"/>
              <prop k="outline_color" v="255,255,255,255"/>
              <prop k="outline_width" v="0.4"/>
              <prop k="size" v="3.5"/>
            </layer>
          </symbol>
          <symbol name="1" type="marker" alpha="0.85" clip_to_extent="1">
            <layer class="SimpleMarker" pass="0" locked="0">
              <prop k="color" v="245,158,11,255"/>
              <prop k="outline_color" v="255,255,255,255"/>
              <prop k="outline_width" v="0.4"/>
              <prop k="size" v="3.0"/>
            </layer>
          </symbol>
          <symbol name="2" type="marker" alpha="0.85" clip_to_extent="1">
            <layer class="SimpleMarker" pass="0" locked="0">
              <prop k="color" v="59,130,246,255"/>
              <prop k="outline_color" v="255,255,255,255"/>
              <prop k="outline_width" v="0.4"/>
              <prop k="size" v="2.5"/>
            </layer>
          </symbol>
          <symbol name="3" type="marker" alpha="0.75" clip_to_extent="1">
            <layer class="SimpleMarker" pass="0" locked="0">
              <prop k="color" v="34,197,94,255"/>
              <prop k="outline_color" v="255,255,255,255"/>
              <prop k="outline_width" v="0.4"/>
              <prop k="size" v="2.2"/>
            </layer>
          </symbol>
        </symbols>
      </renderer-v2>
    </maplayer>
  </maplayers>
</qgis>
'''

with open('ChiangMai_Flood_Households_QGIS_Project.qgs', 'w', encoding='utf-8') as f:
    f.write(qgis_hh_xml)

print("All Household Survey assets generated successfully!")
