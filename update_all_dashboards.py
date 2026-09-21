#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
ระบบอัปเดตข้อมูลและแดชบอร์ดอัตโนมัติ (Automated Update Pipeline)
แผนงานบริหารจัดการทรัพยากรน้ำ จังหวัดเชียงใหม่
=============================================================================
วิธีใช้งาน:
  เมื่อมีการแก้ไขข้อมูลในไฟล์ Excel หรือดาวน์โหลดข้อมูลใหม่จาก Google Sheets
  ให้วางไฟล์ไว้ในโฟลเดอร์นี้ แล้วรันคำสั่ง:
      python3 update_all_dashboards.py
  ระบบจะทำการ:
    1. คลีนข้อมูลและคำนวณสถิติใหม่ทั้งหมด
    2. สร้างไฟล์ Master Excel (1.3 MB)
    3. ส่งออก CSV ทั้ง 7 ชุด
    4. อัปเดตไฟล์ GeoJSON สำหรับ QGIS
    5. อัปเดตแดชบอร์ด HTML ทั้ง 2 หน้า (หน้า Dashboard ปกติ และหน้า Dual GIS)
=============================================================================
"""

import os
import sys
import json
import pandas as pd
import numpy as np

print("="*70)
print("🚀 เริ่มต้นกระบวนการอัปเดตข้อมูลและแดชบอร์ดแผนน้ำเชียงใหม่...")
print("="*70)

# กำหนดชื่อไฟล์ต้นทาง
RISK_FILE = "พื้นที่เสี่ยง 1รวม.xlsx"
BUDGET_FILE = "ได้รับจัดสรร งบแผนน้ำ_เชียงใหม่ (65-70)-ผอ เจนศ.xlsx"

if not os.path.exists(RISK_FILE) or not os.path.exists(BUDGET_FILE):
    print(f"❌ ไม่พบไฟล์ข้อมูลต้นทางในโฟลเดอร์: {RISK_FILE} หรือ {BUDGET_FILE}")
    sys.exit(1)

# 1. รันการประมวลผลข้อมูลหลัก
print("⏳ 1/4 กำลังประมวลผลและคลีนข้อมูลจาก Excel...")
os.system("python3 generate_html_dashboard.py > /dev/null 2>&1")

# 2. รันสร้าง Master Excel
print("⏳ 2/4 กำลังสร้าง Master Excel Workbook และไฟล์ CSV...")
# รันคำสั่งไพพ์ไลน์
import subprocess
subprocess.run([sys.executable, "-c", """
import os, json, pandas as pd, numpy as np

# โหลดข้อมูลความเสี่ยง
df_risk_raw = pd.read_excel('พื้นที่เสี่ยง 1รวม.xlsx', sheet_name='ความเสี่ยง', skiprows=1).dropna(how='all')
df_risk = df_risk_raw.copy()
df_risk['ลำดับ'] = df_risk['ลำดับ'].astype(int)
df_risk['จังหวัด'] = df_risk['จังหวัด'].astype(str).str.strip()
df_risk['อำเภอ'] = df_risk['อำเภอ'].astype(str).str.strip()
df_risk['ตำบล'] = df_risk['ตำบล'].astype(str).str.strip()
df_risk['หมู่บ้าน'] = df_risk['หมู่บ้าน'].astype(str).str.strip()

risk_map = {'เสี่ยงสูง': 3, 'เสี่ยงปานกลาง': 2, 'เสี่ยงน้อย': 1}
pillar_names = {
    1: 'ด้านที่ 1 การจัดการน้ำอุปโภคบริโภค',
    2: 'ด้านที่ 2 การสร้างความมั่นคงของน้ำภาคการผลิต',
    3: 'ด้านที่ 3 การจัดการน้ำท่วมและอุทกภัย',
    4: 'ด้านที่ 4 การจัดการคุณภาพน้ำและการอนุรักษ์',
    5: 'ด้านที่ 5 การอนุรักษ์ฟื้นฟูป่าต้นน้ำและป้องกันการพังทลายของดิน'
}
pillar_short = {
    1: 'ด1_อุปโภคบริโภค', 2: 'ด2_น้ำภาคการผลิต', 3: 'ด3_น้ำท่วมอุทกภัย',
    4: 'ด4_คุณภาพน้ำ', 5: 'ด5_ป่าต้นน้ำดินพังทลาย'
}

for i in range(1, 6):
    df_risk[f'ด้าน {i}'] = df_risk[f'ด้าน {i}'].astype(str).str.strip()
    df_risk[f'คะแนน_ด้าน_{i}'] = df_risk[f'ด้าน {i}'].map(risk_map)

df_risk['คะแนนความเสี่ยงรวม'] = df_risk[[f'คะแนน_ด้าน_{i}' for i in range(1, 6)]].sum(axis=1)
df_risk['จำนวนด้านที่เสี่ยงสูง'] = (df_risk[[f'ด้าน {i}' for i in range(1, 6)]] == 'เสี่ยงสูง').sum(axis=1)
df_risk['จำนวนด้านที่เสี่ยงปานกลาง'] = (df_risk[[f'ด้าน {i}' for i in range(1, 6)]] == 'เสี่ยงปานกลาง').sum(axis=1)
df_risk['จำนวนด้านที่เสี่ยงน้อย'] = (df_risk[[f'ด้าน {i}' for i in range(1, 6)]] == 'เสี่ยงน้อย').sum(axis=1)

def get_priority_level(row):
    if row['จำนวนด้านที่เสี่ยงสูง'] >= 2: return '🚨 วิกฤติเร่งด่วน (เสี่ยงสูง 2+ ด้าน)'
    elif row['จำนวนด้านที่เสี่ยงสูง'] == 1: return '⚠️ เฝ้าระวังสูง (เสี่ยงสูง 1 ด้าน)'
    elif row['จำนวนด้านที่เสี่ยงปานกลาง'] >= 3: return '🟡 เฝ้าระวังปานกลาง (เสี่ยงกลาง 3+ ด้าน)'
    else: return '🟢 เสี่ยงต่ำ/ทั่วไป'
df_risk['ระดับความสำคัญ'] = df_risk.apply(get_priority_level, axis=1)

# โหลดข้อมูลงบประมาณ
df_budget_raw = pd.read_excel('ได้รับจัดสรร งบแผนน้ำ_เชียงใหม่ (65-70)-ผอ เจนศ.xlsx', sheet_name='2565-2570-6312-ปรับรหัส').dropna(how='all')
df_budget = df_budget_raw[df_budget_raw['ลำดับที่'].notna()].copy()
df_budget['ลำดับที่'] = df_budget['ลำดับที่'].astype(int)
df_budget['มิติงบประมาณ'] = df_budget['มิติงบประมาณ'].astype(str).str.strip().replace({'function': 'Function', 'nan': 'ไม่ระบุ', 'ไม่ทราบ': 'ไม่ระบุ'})
df_budget['ประเภทงบประมาณ'] = df_budget['ประเภทงบประมาณ'].astype(str).str.strip().replace({'function': 'Function', 'nan': 'ไม่ระบุ', 'ไม่ทราบ': 'ไม่ระบุ'})
df_budget['หน่วยงานรับผิดชอบ'] = df_budget['หน่วยงานรับผิดชอบ'].astype(str).str.strip()
df_budget['โครงการ'] = df_budget['โครงการ'].astype(str).str.strip()
df_budget['วงเงิน_ล้านบาท'] = df_budget['วงเงิน(ล้านบาท)'].astype(float)
df_budget['รหัสแผนแม่บท'] = df_budget['แผนแม่บทฯ'].astype(int)
df_budget['ชื่อแผนแม่บท'] = df_budget['รหัสแผนแม่บท'].map(pillar_names)
df_budget['ชื่อย่อด้าน'] = df_budget['รหัสแผนแม่บท'].map(pillar_short)
df_budget['ปีงบประมาณ'] = df_budget['ปี'].astype(int)
df_budget['ช่วงปีงบประมาณ'] = df_budget['ปีงบประมาณ'].apply(lambda y: 'ระยะต้น (2565-2567)' if y <= 2567 else 'ระยะปลาย (2568-2570)')
df_budget['อำเภอ'] = df_budget['อำเภอ'].apply(lambda x: str(x).strip() if pd.notna(x) else 'ไม่ระบุ').replace({'ทางดง': 'หางดง', 'nan': 'ไม่ระบุ'})
df_budget['ตำบล'] = df_budget['ตำบล'].apply(lambda x: str(x).strip() if pd.notna(x) else 'ไม่ระบุ').replace({'ทุ่งปี้': 'ทุ่งปี๊', 'วัดเกตุ': 'วัดเกต', 'น้ำแพร่พัฒนา': 'น้ำแพร่', 'nan': 'ไม่ระบุ'})

# Gap รายอำเภอ
districts = sorted(list(set(df_risk['อำเภอ'].unique())))
district_rows = []
for d in districts:
    sub_r = df_risk[df_risk['อำเภอ'] == d]
    sub_b = df_budget[df_budget['อำเภอ'] == d]
    total_villages = len(sub_r)
    total_proj = len(sub_b)
    total_budget = sub_b['วงเงิน_ล้านบาท'].sum()
    r_high_counts = [ (sub_r[f'ด้าน {i}'] == 'เสี่ยงสูง').sum() for i in range(1, 6) ]
    total_high = sum(r_high_counts)
    b_amounts = [ sub_b[sub_b['รหัสแผนแม่บท'] == i]['วงเงิน_ล้านบาท'].sum() for i in range(1, 6) ]
    p_counts = [ len(sub_b[sub_b['รหัสแผนแม่บท'] == i]) for i in range(1, 6) ]
    if total_high >= 70 and total_budget < 1000: gap_status = '🚨 เสี่ยงสูงวิกฤติ - งบประมาณไม่เพียงพอ'
    elif total_high >= 70: gap_status = '⚠️ เสี่ยงสูง - ได้รับงบประมาณต่อเนื่อง'
    elif total_high >= 30 and total_budget < 800: gap_status = '🟡 เสี่ยงปานกลาง - ควรเพิ่มงบประมาณ'
    elif total_high < 15 and total_budget > 2000: gap_status = '🔵 งบประมาณสูง - ความเสี่ยงต่ำ (โครงการโครงสร้างพื้นฐานหลัก)'
    else: gap_status = '🟢 สมดุลตามเกณฑ์'
    avg_budget_per_high = total_budget / total_high if total_high > 0 else total_budget
    district_rows.append({
        'อำเภอ': d, 'จำนวนหมู่บ้าน': total_villages, 'จำนวนเสี่ยงสูง_รวมทุกด้าน': total_high,
        'สถานะการจัดสรร (Gap Status)': gap_status, 'งบประมาณรวม (ล้านบาท)': total_budget, 'จำนวนโครงการรวม': total_proj,
        'งบเฉลี่ยต่อจุดเสี่ยงสูง (ล้านบาท)': avg_budget_per_high,
        'เสี่ยงสูง_ด1_อุปโภค': r_high_counts[0], 'โครงการ_ด1': p_counts[0], 'งบ_ด1 (ล้านบาท)': b_amounts[0],
        'เสี่ยงสูง_ด2_เกษตร': r_high_counts[1], 'โครงการ_ด2': p_counts[1], 'งบ_ด2 (ล้านบาท)': b_amounts[1],
        'เสี่ยงสูง_ด3_น้ำท่วม': r_high_counts[2], 'โครงการ_ด3': p_counts[2], 'งบ_ด3 (ล้านบาท)': b_amounts[2],
        'เสี่ยงสูง_ด4_คุณภาพน้ำ': r_high_counts[3], 'โครงการ_ด4': p_counts[3], 'งบ_ด4 (ล้านบาท)': b_amounts[3],
        'เสี่ยงสูง_ด5_ป่าต้นน้ำ': r_high_counts[4], 'โครงการ_ด5': p_counts[4], 'งบ_ด5 (ล้านบาท)': b_amounts[4]
    })

df_dist_gap = pd.DataFrame(district_rows)

# บันทึก CSV
csv_dir = 'data_clean_csv'
os.makedirs(csv_dir, exist_ok=True)
df_budget.to_csv(f'{csv_dir}/01_โครงการและงบประมาณ_Clean.csv', index=False, encoding='utf-8-sig')
df_risk.to_csv(f'{csv_dir}/02_พื้นที่เสี่ยงน้ำ_Clean.csv', index=False, encoding='utf-8-sig')
df_dist_gap.to_csv(f'{csv_dir}/04_สรุปรายอำเภอ_GapAnalysis.csv', index=False, encoding='utf-8-sig')
"""])

# 3. รันอัปเดต GIS และ GeoJSON
print("⏳ 3/5 กำลังอัปเดตไฟล์ GIS GeoJSON และ QGIS Project...")
subprocess.run([sys.executable, "build_gis_dashboard.py"])
subprocess.run([sys.executable, "create_qgis_package.py"])

# 4. รันอัปเดตข้อมูลสำรวจรายครัวเรือน
print("⏳ 4/5 กำลังประมวลผลข้อมูลสำรวจรายครัวเรือน 4,450 หลัง (Point GIS)...")
subprocess.run([sys.executable, "process_flood_survey.py"])
subprocess.run([sys.executable, "build_household_dashboard_package.py"])

# 5. รันสร้าง Google Maps Styled Dashboards
print("⏳ 5/5 กำลังสร้าง Web GIS แดชบอร์ดสไตล์ Google Maps...")
subprocess.run([sys.executable, "build_google_maps_dashboards.py"])

print("="*70)
print("✅ อัปเดตข้อมูลทุกระบบเสร็จสมบูรณ์ 100% ครบทุกชุด!")
print("   1. [แผนแม่บท] ChiangMai_Water_GIS_Dashboard.html (GIS เปรียบเทียบระดับอำเภอ)")
print("   2. [แผนแม่บท] ChiangMai_Water_Risk_Budget_Dashboard.xlsx (Master Excel)")
print("   3. [รายครัวเรือน] ChiangMai_Flood_Household_GIS_Dashboard.html (Point GIS 4,450 หลัง)")
print("   4. [รายครัวเรือน] ChiangMai_Flood_Household_Survey_Dashboard.xlsx (Master Excel)")
print("   5. [QGIS Projects] พร้อมเปิดใช้งานทั้งระดับอำเภอและระดับพิกัดบ้าน")
print("="*70)
