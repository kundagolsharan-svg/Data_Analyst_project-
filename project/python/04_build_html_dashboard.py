import json
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_PATH = BASE_DIR / "data" / "sales_data_cleaned.csv"
OUT_PATH = BASE_DIR / "dashboard" / "business_dashboard.html"

df = pd.read_csv(CLEAN_PATH)
records = df[[
    "OrderID", "OrderDate", "ShipDate", "ShipMode", "CustomerID", "CustomerName",
    "Region", "Category", "Product", "Quantity", "UnitPrice", "Discount",
    "Sales", "Profit", "ShippingDays", "ProfitMargin"
]].to_dict(orient="records")

data_json = json.dumps(records)

html_content = f'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Executive Sales & Operations Intelligence | Power BI Interactive</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root {{
    --font-main: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
    
    /* Dark Theme (Default) */
    --bg-base: #0B0F19;
    --bg-surface: #111827;
    --bg-surface-elevated: #1F2937;
    --bg-card: rgba(17, 24, 39, 0.85);
    --border-color: rgba(255, 255, 255, 0.09);
    --border-subtle: rgba(255, 255, 255, 0.05);
    
    --text-primary: #F9FAFB;
    --text-secondary: #9CA3AF;
    --text-muted: #6B7280;
    
    --primary: #3B82F6;
    --primary-glow: rgba(59, 130, 246, 0.25);
    --accent-cyan: #06B6D4;
    --accent-emerald: #10B981;
    --accent-amber: #F59E0B;
    --accent-purple: #8B5CF6;
    --accent-rose: #F43F5E;
    
    --kpi-revenue-glow: rgba(59, 130, 246, 0.15);
    --kpi-profit-glow: rgba(16, 185, 129, 0.15);
    --kpi-orders-glow: rgba(245, 158, 11, 0.15);
    --kpi-margin-glow: rgba(139, 92, 246, 0.15);
    --kpi-aov-glow: rgba(6, 182, 212, 0.15);
    
    --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
    --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.4);
    --shadow-lg: 0 16px 36px rgba(0, 0, 0, 0.5);
    --glass-blur: blur(12px);
  }}

  [data-theme="light"] {{
    --bg-base: #F8FAFC;
    --bg-surface: #FFFFFF;
    --bg-surface-elevated: #F1F5F9;
    --bg-card: rgba(255, 255, 255, 0.95);
    --border-color: #E2E8F0;
    --border-subtle: #F1F5F9;
    
    --text-primary: #0F172A;
    --text-secondary: #475569;
    --text-muted: #94A3B8;
    
    --primary: #2563EB;
    --primary-glow: rgba(37, 99, 235, 0.15);
    --accent-cyan: #0891B2;
    --accent-emerald: #059669;
    --accent-amber: #D97706;
    --accent-purple: #7C3AED;
    --accent-rose: #E11D48;
    
    --kpi-revenue-glow: rgba(37, 99, 235, 0.08);
    --kpi-profit-glow: rgba(5, 150, 105, 0.08);
    --kpi-orders-glow: rgba(217, 119, 6, 0.08);
    --kpi-margin-glow: rgba(124, 58, 237, 0.08);
    --kpi-aov-glow: rgba(8, 145, 178, 0.08);
    
    --shadow-sm: 0 2px 8px rgba(15, 23, 42, 0.04);
    --shadow-md: 0 6px 18px rgba(15, 23, 42, 0.08);
    --shadow-lg: 0 12px 28px rgba(15, 23, 42, 0.12);
  }}

  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    transition: background-color 0.25s ease, border-color 0.25s ease, color 0.2s ease;
  }}

  body {{
    font-family: var(--font-main);
    background-color: var(--bg-base);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    overflow-x: hidden;
  }}

  /* Top Navigation & Header */
  header.app-header {{
    background: var(--bg-surface);
    border-bottom: 1px solid var(--border-color);
    padding: 14px 28px;
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: var(--glass-blur);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  .brand {{
    display: flex;
    align-items: center;
    gap: 14px;
  }}

  .brand-logo {{
    width: 38px;
    height: 38px;
    background: linear-gradient(135deg, #F2C811, #F4A261, #E76F51);
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #1A1A1A;
    font-weight: 800;
    font-size: 1.2rem;
    box-shadow: 0 4px 12px rgba(242, 200, 17, 0.35);
  }}

  .brand-text h1 {{
    font-size: 1.15rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--text-primary);
  }}

  .brand-text p {{
    font-size: 0.78rem;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 2px;
  }}

  .badge-pbi {{
    background: rgba(242, 200, 17, 0.15);
    color: #EAB308;
    border: 1px solid rgba(242, 200, 17, 0.3);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
  }}

  .header-actions {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}

  .theme-toggle-btn, .export-btn {{
    background: var(--bg-surface-elevated);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
    padding: 8px 14px;
    border-radius: 8px;
    font-size: 0.82rem;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: var(--font-main);
  }}

  .theme-toggle-btn:hover, .export-btn:hover {{
    border-color: var(--primary);
    transform: translateY(-1px);
  }}

  /* Page Tabs Bar */
  .page-nav-bar {{
    background: var(--bg-surface);
    border-bottom: 1px solid var(--border-color);
    padding: 0 28px;
    display: flex;
    gap: 6px;
    overflow-x: auto;
  }}

  .tab-btn {{
    background: transparent;
    border: none;
    color: var(--text-secondary);
    padding: 13px 18px;
    font-size: 0.88rem;
    font-weight: 600;
    cursor: pointer;
    position: relative;
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: var(--font-main);
    white-space: nowrap;
  }}

  .tab-btn:hover {{
    color: var(--text-primary);
  }}

  .tab-btn.active {{
    color: var(--primary);
  }}

  .tab-btn.active::after {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--primary);
    border-radius: 3px 3px 0 0;
    box-shadow: 0 -2px 8px var(--primary);
  }}

  /* Slicers / Filters Bar */
  .slicers-bar {{
    background: var(--bg-card);
    backdrop-filter: var(--glass-blur);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 14px 20px;
    margin: 20px 28px 0;
    display: flex;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
    box-shadow: var(--shadow-sm);
  }}

  .slicer-label {{
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    display: block;
    margin-bottom: 4px;
  }}

  .slicer-item {{
    display: flex;
    flex-direction: column;
    min-width: 145px;
  }}

  .slicer-select {{
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    padding: 7px 12px;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 500;
    outline: none;
    font-family: var(--font-main);
    cursor: pointer;
  }}

  .slicer-select:focus {{
    border-color: var(--primary);
  }}

  .slicer-reset-btn {{
    margin-left: auto;
    background: transparent;
    border: 1px solid var(--border-color);
    color: var(--text-secondary);
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 0.82rem;
    font-weight: 600;
    cursor: pointer;
    font-family: var(--font-main);
  }}

  .slicer-reset-btn:hover {{
    background: var(--bg-surface-elevated);
    color: var(--text-primary);
    border-color: var(--text-muted);
  }}

  /* Main Container & Pages */
  main.app-main {{
    padding: 20px 28px 40px;
    flex: 1;
    max-width: 1680px;
    margin: 0 auto;
    width: 100%;
  }}

  .tab-page {{
    display: none;
    animation: fadeIn 0.3s ease forwards;
  }}

  .tab-page.active {{
    display: block;
  }}

  @keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(6px); }}
    to {{ opacity: 1; transform: translateY(0); }}
  }}

  /* KPI Cards Grid */
  .kpi-deck {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
    gap: 16px;
    margin-bottom: 22px;
  }}

  .kpi-card {{
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 14px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
    backdrop-filter: var(--glass-blur);
    box-shadow: var(--shadow-sm);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .kpi-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background: var(--accent-color, var(--primary));
  }}

  .kpi-card.revenue {{ --accent-color: var(--primary); background: linear-gradient(180deg, var(--kpi-revenue-glow) 0%, var(--bg-card) 60%); }}
  .kpi-card.profit {{ --accent-color: var(--accent-emerald); background: linear-gradient(180deg, var(--kpi-profit-glow) 0%, var(--bg-card) 60%); }}
  .kpi-card.margin {{ --accent-color: var(--accent-purple); background: linear-gradient(180deg, var(--kpi-margin-glow) 0%, var(--bg-card) 60%); }}
  .kpi-card.orders {{ --accent-color: var(--accent-amber); background: linear-gradient(180deg, var(--kpi-orders-glow) 0%, var(--bg-card) 60%); }}
  .kpi-card.aov {{ --accent-color: var(--accent-cyan); background: linear-gradient(180deg, var(--kpi-aov-glow) 0%, var(--bg-card) 60%); }}
  .kpi-card.units {{ --accent-color: var(--accent-rose); }}

  .kpi-top {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }}

  .kpi-title {{
    font-size: 0.74rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-secondary);
  }}

  .kpi-badge {{
    font-size: 0.72rem;
    font-weight: 600;
    padding: 2px 7px;
    border-radius: 12px;
    background: rgba(16, 185, 129, 0.15);
    color: var(--accent-emerald);
    border: 1px solid rgba(16, 185, 129, 0.25);
  }}

  .kpi-val {{
    font-size: 1.75rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--text-primary);
    margin: 4px 0 8px;
    font-variant-numeric: tabular-nums;
  }}

  .kpi-subtext {{
    font-size: 0.74rem;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 6px;
  }}

  /* Visuals Grid Layouts */
  .visual-grid-2-1 {{
    display: grid;
    grid-template-columns: 1.8fr 1.2fr;
    gap: 18px;
    margin-bottom: 20px;
  }}

  .visual-grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
    margin-bottom: 20px;
  }}

  .visual-card {{
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 14px;
    padding: 20px 22px;
    backdrop-filter: var(--glass-blur);
    box-shadow: var(--shadow-sm);
    display: flex;
    flex-direction: column;
    min-height: 380px;
  }}

  .visual-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
  }}

  .visual-title {{
    font-size: 0.96rem;
    font-weight: 700;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  .visual-subtitle {{
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: 2px;
  }}

  .chart-box {{
    position: relative;
    flex: 1;
    width: 100%;
    min-height: 280px;
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  canvas.native-chart {{
    width: 100% !important;
    height: 100% !important;
    display: block;
  }}

  /* Tooltip overlay */
  .chart-tooltip {{
    position: absolute;
    background: rgba(15, 23, 42, 0.95);
    border: 1px solid var(--border-color);
    color: #F8FAFC;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 0.78rem;
    pointer-events: none;
    box-shadow: 0 4px 14px rgba(0,0,0,0.5);
    opacity: 0;
    transition: opacity 0.15s ease, transform 0.15s ease;
    z-index: 50;
    white-space: nowrap;
  }}

  [data-theme="light"] .chart-tooltip {{
    background: rgba(255, 255, 255, 0.96);
    color: #0F172A;
    border-color: #CBD5E1;
    box-shadow: 0 4px 14px rgba(0,0,0,0.15);
  }}

  /* Custom Data Tables & Matrices */
  .table-responsive {{
    width: 100%;
    overflow-x: auto;
    flex: 1;
  }}

  table.pbi-table {{
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-size: 0.84rem;
  }}

  table.pbi-table th {{
    background: var(--bg-surface-elevated);
    color: var(--text-secondary);
    text-transform: uppercase;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    padding: 10px 14px;
    border-bottom: 1px solid var(--border-color);
    text-align: left;
    white-space: nowrap;
    position: sticky;
    top: 0;
    cursor: pointer;
    user-select: none;
  }}

  table.pbi-table th:hover {{
    color: var(--primary);
  }}

  table.pbi-table td {{
    padding: 10px 14px;
    border-bottom: 1px solid var(--border-subtle);
    color: var(--text-primary);
    font-variant-numeric: tabular-nums;
  }}

  table.pbi-table tr:hover td {{
    background: rgba(59, 130, 246, 0.06);
  }}

  .num-cell {{
    text-align: right;
  }}

  /* Data Bars in Table */
  .data-bar-wrapper {{
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 8px;
    width: 100%;
  }}

  .data-bar-container {{
    width: 90px;
    height: 8px;
    background: rgba(255, 255, 255, 0.06);
    border-radius: 4px;
    overflow: hidden;
  }}

  [data-theme="light"] .data-bar-container {{
    background: #E2E8F0;
  }}

  .data-bar-fill {{
    height: 100%;
    background: linear-gradient(90deg, #3B82F6, #60A5FA);
    border-radius: 4px;
  }}

  .margin-tag {{
    display: inline-block;
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 700;
  }}

  .margin-high {{
    background: rgba(16, 185, 129, 0.15);
    color: #34D399;
    border: 1px solid rgba(16, 185, 129, 0.3);
  }}

  .margin-med {{
    background: rgba(245, 158, 11, 0.15);
    color: #FBBF24;
    border: 1px solid rgba(245, 158, 11, 0.3);
  }}

  .margin-low {{
    background: rgba(244, 63, 94, 0.15);
    color: #FB7185;
    border: 1px solid rgba(244, 63, 94, 0.3);
  }}

  .category-pill {{
    display: inline-block;
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 600;
  }}

  .cat-tech {{ background: rgba(59, 130, 246, 0.15); color: #60A5FA; }}
  .cat-office {{ background: rgba(16, 185, 129, 0.15); color: #34D399; }}
  .cat-furniture {{ background: rgba(245, 158, 11, 0.15); color: #FBBF24; }}

  /* DAX Library & Model Documentation */
  .dax-card {{
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 14px;
  }}

  .dax-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }}

  .dax-name {{
    font-size: 0.88rem;
    font-weight: 700;
    color: var(--primary);
  }}

  .dax-code {{
    font-family: var(--font-mono);
    background: rgba(0, 0, 0, 0.3);
    padding: 10px 14px;
    border-radius: 6px;
    font-size: 0.78rem;
    color: #E2E8F0;
    overflow-x: auto;
    border: 1px solid var(--border-color);
    line-height: 1.5;
  }}

  [data-theme="light"] .dax-code {{
    background: #0F172A;
    color: #F8FAFC;
  }}

  .copy-btn {{
    background: transparent;
    border: 1px solid var(--border-color);
    color: var(--text-secondary);
    padding: 3px 8px;
    border-radius: 5px;
    font-size: 0.7rem;
    cursor: pointer;
  }}

  .copy-btn:hover {{
    color: var(--primary);
    border-color: var(--primary);
  }}

  /* Donut Legend */
  .donut-legend {{
    display: flex;
    justify-content: center;
    gap: 16px;
    margin-top: 10px;
    flex-wrap: wrap;
  }}

  .legend-item {{
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.78rem;
    color: var(--text-secondary);
    font-weight: 600;
  }}

  .legend-dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
  }}

  /* Responsive Design */
  @media (max-width: 1200px) {{
    .visual-grid-2-1, .visual-grid-2 {{
      grid-template-columns: 1fr;
    }}
  }}

  @media (max-width: 768px) {{
    header.app-header {{
      flex-direction: column;
      align-items: flex-start;
      gap: 12px;
      padding: 14px 16px;
    }}
    .page-nav-bar, .slicers-bar, main.app-main {{
      padding-left: 14px;
      padding-right: 14px;
      margin-left: 0;
      margin-right: 0;
    }}
    .kpi-deck {{
      grid-template-columns: 1fr 1fr;
    }}
  }}
</style>
</head>
<body>

<div id="chartTooltip" class="chart-tooltip"></div>

<header class="app-header">
  <div class="brand">
    <div class="brand-logo">📊</div>
    <div class="brand-text">
      <h1>Executive Sales & Operations Intelligence</h1>
      <p><span class="badge-pbi">Power BI Architecture</span> Sample Retail Sales Data · 2024–2025</p>
    </div>
  </div>
  <div class="header-actions">
    <button class="export-btn" id="exportCsvBtn" title="Download active filtered dataset">📥 Export CSV</button>
    <button class="theme-toggle-btn" id="themeToggleBtn">☀️ Light Mode</button>
  </div>
</header>

<nav class="page-nav-bar">
  <button class="tab-btn active" data-tab="tab-overview">📑 Page 1 — Executive Overview</button>
  <button class="tab-btn" data-tab="tab-products">📊 Page 2 — Product Performance</button>
  <button class="tab-btn" data-tab="tab-customers">👥 Page 3 — Customer & Regional Detail</button>
  <button class="tab-btn" data-tab="tab-dax">📐 Page 4 — DAX & Modeling Architecture</button>
</nav>

<div class="slicers-bar">
  <div class="slicer-item">
    <label class="slicer-label" for="slicerRegion">Region</label>
    <select id="slicerRegion" class="slicer-select">
      <option value="All">All Regions</option>
      <option value="East">East</option>
      <option value="North">North</option>
      <option value="South">South</option>
      <option value="West">West</option>
    </select>
  </div>
  <div class="slicer-item">
    <label class="slicer-label" for="slicerCategory">Category</label>
    <select id="slicerCategory" class="slicer-select">
      <option value="All">All Categories</option>
      <option value="Furniture">Furniture</option>
      <option value="Office Supplies">Office Supplies</option>
      <option value="Technology">Technology</option>
    </select>
  </div>
  <div class="slicer-item">
    <label class="slicer-label" for="slicerYear">Year</label>
    <select id="slicerYear" class="slicer-select">
      <option value="All">All Years</option>
      <option value="2024">2024</option>
      <option value="2025">2025</option>
    </select>
  </div>
  <div class="slicer-item">
    <label class="slicer-label" for="slicerShipMode">Ship Mode</label>
    <select id="slicerShipMode" class="slicer-select">
      <option value="All">All Ship Modes</option>
      <option value="Standard Class">Standard Class</option>
      <option value="Second Class">Second Class</option>
      <option value="First Class">First Class</option>
      <option value="Same Day">Same Day</option>
    </select>
  </div>
  <button id="resetSlicersBtn" class="slicer-reset-btn">↺ Reset Slicers</button>
</div>

<main class="app-main">

  <!-- =========================================================================
       PAGE 1: EXECUTIVE OVERVIEW
       ========================================================================= -->
  <section id="tab-overview" class="tab-page active">
    
    <div class="kpi-deck">
      <div class="kpi-card revenue">
        <div class="kpi-top">
          <span class="kpi-title">Total Revenue</span>
          <span class="kpi-badge" id="kpiRevBadge">Active</span>
        </div>
        <div class="kpi-val" id="kpiRevenue">$0.00</div>
        <div class="kpi-subtext" id="kpiRevSub">YTD Growth: +14.2%</div>
      </div>

      <div class="kpi-card profit">
        <div class="kpi-top">
          <span class="kpi-title">Total Profit</span>
          <span class="kpi-badge">Net Income</span>
        </div>
        <div class="kpi-val" id="kpiProfit">$0.00</div>
        <div class="kpi-subtext">Gross Margin Health</div>
      </div>

      <div class="kpi-card margin">
        <div class="kpi-top">
          <span class="kpi-title">Profit Margin %</span>
          <span class="kpi-badge">Efficiency</span>
        </div>
        <div class="kpi-val" id="kpiMargin">0.0%</div>
        <div class="kpi-subtext">Target: 25.0%</div>
      </div>

      <div class="kpi-card orders">
        <div class="kpi-top">
          <span class="kpi-title">Total Orders</span>
          <span class="kpi-badge">Volume</span>
        </div>
        <div class="kpi-val" id="kpiOrders">0</div>
        <div class="kpi-subtext" id="kpiUnitsSub">0 units sold</div>
      </div>

      <div class="kpi-card aov">
        <div class="kpi-top">
          <span class="kpi-title">Avg Order Value (AOV)</span>
          <span class="kpi-badge">Basket Size</span>
        </div>
        <div class="kpi-val" id="kpiAOV">$0.00</div>
        <div class="kpi-subtext">Revenue / Orders</div>
      </div>
    </div>

    <div class="visual-grid-2-1">
      <div class="visual-card">
        <div class="visual-header">
          <div>
            <div class="visual-title">📈 Monthly Revenue & Revenue LM (Last Month) Trend</div>
            <div class="visual-subtitle">Time Intelligence (DATEADD -1 Month & Monthly Run Rate)</div>
          </div>
        </div>
        <div class="chart-box" id="monthlyTrendBox">
          <canvas id="monthlyTrendCanvas" class="native-chart"></canvas>
        </div>
      </div>

      <div class="visual-card">
        <div class="visual-header">
          <div>
            <div class="visual-title">🍩 Revenue Share by Category</div>
            <div class="visual-subtitle">Contribution % across Product Verticals</div>
          </div>
        </div>
        <div class="chart-box" id="categoryDonutBox" style="flex-direction:column;">
          <canvas id="categoryDonutCanvas" class="native-chart" style="max-height:220px;"></canvas>
          <div class="donut-legend" id="categoryLegend"></div>
        </div>
      </div>
    </div>

    <div class="visual-grid-2">
      <div class="visual-card">
        <div class="visual-header">
          <div>
            <div class="visual-title">🏢 Total Revenue & Profit by Region</div>
            <div class="visual-subtitle">Regional Performance Clustered Comparison</div>
          </div>
        </div>
        <div class="chart-box" id="regionBarBox">
          <canvas id="regionBarCanvas" class="native-chart"></canvas>
        </div>
      </div>

      <div class="visual-card">
        <div class="visual-header">
          <div>
            <div class="visual-title">📦 Top 10 High-Value Orders</div>
            <div class="visual-subtitle">Instant Transaction Inspector</div>
          </div>
        </div>
        <div class="table-responsive" style="max-height: 290px;">
          <table class="pbi-table" id="topOrdersTable">
            <thead>
              <tr>
                <th>Order ID</th>
                <th>Date</th>
                <th>Customer</th>
                <th>Product</th>
                <th class="num-cell">Sales</th>
                <th class="num-cell">Profit</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>
      </div>
    </div>

  </section>

  <!-- =========================================================================
       PAGE 2: PRODUCT PERFORMANCE
       ========================================================================= -->
  <section id="tab-products" class="tab-page">
    
    <div class="kpi-deck">
      <div class="kpi-card revenue">
        <div class="kpi-top"><span class="kpi-title">Top Product</span><span class="kpi-badge">Rank 1</span></div>
        <div class="kpi-val" style="font-size:1.4rem;" id="kpiTopProduct">-</div>
        <div class="kpi-subtext" id="kpiTopProductRev">$0.00 revenue</div>
      </div>
      <div class="kpi-card margin">
        <div class="kpi-top"><span class="kpi-title">Highest Margin Cat</span><span class="kpi-badge">Profitability</span></div>
        <div class="kpi-val" style="font-size:1.4rem;" id="kpiTopCatMargin">-</div>
        <div class="kpi-subtext">Technology sector lead</div>
      </div>
      <div class="kpi-card profit">
        <div class="kpi-top"><span class="kpi-title">Avg Discount %</span><span class="kpi-badge">Erosion</span></div>
        <div class="kpi-val" id="kpiAvgDiscount">0.0%</div>
        <div class="kpi-subtext">Correlation with profit: -0.30</div>
      </div>
      <div class="kpi-card orders">
        <div class="kpi-top"><span class="kpi-title">SKU Portfolio</span><span class="kpi-badge">Active</span></div>
        <div class="kpi-val" id="kpiProductCount">12</div>
        <div class="kpi-subtext">All items contributing</div>
      </div>
    </div>

    <div class="visual-grid-2">
      <div class="visual-card">
        <div class="visual-header">
          <div>
            <div class="visual-title">🏆 Top Products by Total Revenue (RANKX)</div>
            <div class="visual-subtitle">Filter visual to Product Revenue Rank ≤ 10</div>
          </div>
        </div>
        <div class="chart-box" id="productRankBox">
          <canvas id="productRankCanvas" class="native-chart"></canvas>
        </div>
      </div>

      <div class="visual-card">
        <div class="visual-header">
          <div>
            <div class="visual-title">🎯 Discount % vs. Profit Margin % (Bubble Size = Revenue)</div>
            <div class="visual-subtitle">Demonstrates discount margin erosion & volume trade-offs</div>
          </div>
        </div>
        <div class="chart-box" id="discountScatterBox">
          <canvas id="discountScatterCanvas" class="native-chart"></canvas>
        </div>
      </div>
    </div>

    <div class="visual-card">
      <div class="visual-header">
        <div>
          <div class="visual-title">📑 Product Performance Matrix with Conditional Data Bars & Color Scales</div>
          <div class="visual-subtitle">Live DAX aggregation: Units Sold, Total Revenue, Total Profit, Profit Margin %</div>
        </div>
      </div>
      <div class="table-responsive">
        <table class="pbi-table" id="productMatrixTable">
          <thead>
            <tr>
              <th>Product</th>
              <th>Category</th>
              <th class="num-cell">Units Sold</th>
              <th class="num-cell" style="min-width:180px;">Total Revenue (Data Bars)</th>
              <th class="num-cell">Total Profit</th>
              <th class="num-cell">Avg Discount</th>
              <th class="num-cell">Profit Margin %</th>
            </tr>
          </thead>
          <tbody></tbody>
        </table>
      </div>
    </div>

  </section>

  <!-- =========================================================================
       PAGE 3: CUSTOMER & REGIONAL DETAIL
       ========================================================================= -->
  <section id="tab-customers" class="tab-page">
    
    <div class="kpi-deck">
      <div class="kpi-card aov">
        <div class="kpi-top"><span class="kpi-title">Unique Customers</span><span class="kpi-badge">Accounts</span></div>
        <div class="kpi-val" id="kpiUniqueCust">0</div>
        <div class="kpi-subtext">Active purchasing base</div>
      </div>
      <div class="kpi-card orders">
        <div class="kpi-top"><span class="kpi-title">Orders Per Customer</span><span class="kpi-badge">Retention</span></div>
        <div class="kpi-val" id="kpiOrdersPerCust">0.0</div>
        <div class="kpi-subtext">High repeat purchase frequency</div>
      </div>
      <div class="kpi-card profit">
        <div class="kpi-top"><span class="kpi-title">Avg Shipping Duration</span><span class="kpi-badge">Fulfillment</span></div>
        <div class="kpi-val" id="kpiAvgShipDays">0.0 d</div>
        <div class="kpi-subtext">Order Date to Ship Date</div>
      </div>
      <div class="kpi-card revenue">
        <div class="kpi-top"><span class="kpi-title">Avg Spend Per Customer</span><span class="kpi-badge">LTV</span></div>
        <div class="kpi-val" id="kpiCustAvgSpend">$0.00</div>
        <div class="kpi-subtext">Account lifetime value</div>
      </div>
    </div>

    <div class="visual-grid-2">
      <div class="visual-card">
        <div class="visual-header">
          <div>
            <div class="visual-title">🚚 Shipping Mode Volume & Lead Time</div>
            <div class="visual-subtitle">Orders by ShipMode vs. Average Days to Ship</div>
          </div>
        </div>
        <div class="chart-box" id="shipModeBox">
          <canvas id="shipModeCanvas" class="native-chart"></canvas>
        </div>
      </div>

      <div class="visual-card">
        <div class="visual-header">
          <div>
            <div class="visual-title">🗺️ Regional Order Density & Margin Index</div>
            <div class="visual-subtitle">Regional efficiency breakdown</div>
          </div>
        </div>
        <div class="chart-box" id="regionalMarginBox">
          <canvas id="regionalMarginCanvas" class="native-chart"></canvas>
        </div>
      </div>
    </div>

    <div class="visual-card">
      <div class="visual-header">
        <div>
          <div class="visual-title">👥 Top Customer Accounts (Sorted by Lifetime Revenue)</div>
          <div class="visual-subtitle">Searchable account roster with customer tiering</div>
        </div>
      </div>
      <div class="table-responsive" style="max-height: 380px;">
        <table class="pbi-table" id="customerAccountsTable">
          <thead>
            <tr>
              <th>Customer ID</th>
              <th>Customer Name</th>
              <th>Region</th>
              <th class="num-cell">Total Orders</th>
              <th class="num-cell">Total Units</th>
              <th class="num-cell">Lifetime Revenue</th>
              <th class="num-cell">Total Profit</th>
              <th class="num-cell">Account Tier</th>
            </tr>
          </thead>
          <tbody></tbody>
        </table>
      </div>
    </div>

  </section>

  <!-- =========================================================================
       PAGE 4: DAX & MODELING ARCHITECTURE
       ========================================================================= -->
  <section id="tab-dax" class="tab-page">
    
    <div class="visual-grid-2">
      <div class="visual-card">
        <div class="visual-header">
          <div>
            <div class="visual-title">⭐ Power BI Star Schema Data Model</div>
            <div class="visual-subtitle">Dimensional Modeling Best Practice</div>
          </div>
        </div>
        <div style="font-size:0.84rem; line-height:1.6; color:var(--text-secondary);">
          <p style="margin-bottom:12px;">This analytics engine uses a clean <strong>Star Schema</strong>:</p>
          <ul style="padding-left:20px; margin-bottom:14px;">
            <li><strong>Fact Table:</strong> <code>orders</code> (2,018 rows) — contains Transaction IDs, Dates, Quantities, Unit Price, Sales, and Profit.</li>
            <li><strong>Dimension 1:</strong> <code>DateTable</code> (1-to-many with <code>orders[OrderDate]</code>) — enables MoM, LM, YTD time intelligence.</li>
            <li><strong>Dimension 2:</strong> <code>customers</code> (1-to-many with <code>orders[CustomerID]</code>) — Name & Region.</li>
            <li><strong>Dimension 3:</strong> <code>products</code> (1-to-many with <code>orders[ProductID]</code>) — Product Name & Category.</li>
          </ul>
          <div style="background:var(--bg-surface-elevated); padding:12px 16px; border-radius:8px; border:1px solid var(--border-color);">
            <strong>💡 Pro-Tip:</strong> In Power BI, always mark <code>DateTable</code> as a Date Table (Table tools → Mark as Date Table) to unlock native DAX time intelligence functions!
          </div>
        </div>
      </div>

      <div class="visual-card">
        <div class="visual-header">
          <div>
            <div class="visual-title">🛠️ 15-Minute Power BI Build Guide</div>
            <div class="visual-subtitle">Step-by-step implementation in Power BI Desktop</div>
          </div>
        </div>
        <div style="font-size:0.84rem; line-height:1.6; color:var(--text-secondary);">
          <ol style="padding-left:20px;">
            <li><strong>Get Data:</strong> Load <code>data/sales_data_cleaned.csv</code> into Power BI Desktop.</li>
            <li><strong>Modeling:</strong> Create <code>DateTable = CALENDAR(MIN(sales_data_cleaned[OrderDate]), MAX(sales_data_cleaned[OrderDate]))</code>.</li>
            <li><strong>Relationships:</strong> Drag <code>DateTable[Date]</code> → <code>sales_data_cleaned[OrderDate]</code>.</li>
            <li><strong>Measures Table:</strong> Copy the DAX snippets below into a dedicated <code>_Measures</code> table.</li>
            <li><strong>Design Visuals:</strong> Follow the page layouts configured on Pages 1, 2, and 3!</li>
          </ol>
        </div>
      </div>
    </div>

    <div class="visual-card">
      <div class="visual-header">
        <div>
          <div class="visual-title">💻 Production DAX Measure Library</div>
          <div class="visual-subtitle">Ready-to-use copyable DAX formulas used across this dashboard</div>
        </div>
      </div>

      <div class="dax-card">
        <div class="dax-header">
          <span class="dax-name">Total Revenue & Total Profit (Core Aggregations)</span>
          <button class="copy-btn" onclick="copyDax(this, 'Total Revenue = SUM(sales_data_cleaned[Sales])\\nTotal Profit = SUM(sales_data_cleaned[Profit])')">Copy DAX</button>
        </div>
        <pre class="dax-code">Total Revenue = SUM(sales_data_cleaned[Sales])
Total Profit = SUM(sales_data_cleaned[Profit])
Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0)</pre>
      </div>

      <div class="dax-card">
        <div class="dax-header">
          <span class="dax-name">Time Intelligence: Revenue Last Month & MoM %</span>
          <button class="copy-btn" onclick="copyDax(this, 'Revenue LM = CALCULATE([Total Revenue], DATEADD(DateTable[Date], -1, MONTH))\\nRevenue MoM % = DIVIDE([Total Revenue] - [Revenue LM], [Revenue LM], 0)')">Copy DAX</button>
        </div>
        <pre class="dax-code">Revenue LM =
CALCULATE([Total Revenue], DATEADD(DateTable[Date], -1, MONTH))

Revenue MoM % =
DIVIDE([Total Revenue] - [Revenue LM], [Revenue LM], 0)

Revenue YTD =
TOTALYTD([Total Revenue], DateTable[Date])</pre>
      </div>

      <div class="dax-card">
        <div class="dax-header">
          <span class="dax-name">Ranking Measure: Product Revenue Rank (RANKX)</span>
          <button class="copy-btn" onclick="copyDax(this, 'Product Revenue Rank = RANKX(ALL(sales_data_cleaned[Product]), [Total Revenue], , DESC)')">Copy DAX</button>
        </div>
        <pre class="dax-code">Product Revenue Rank =
RANKX(ALL(sales_data_cleaned[Product]), [Total Revenue], , DESC)</pre>
      </div>

    </div>

  </section>

</main>

<script>
/* =============================================================================
   STANDALONE DATASET & ZERO-DEPENDENCY NATIVE CANVAS / SVG CHART ENGINE
   ============================================================================= */
const rawData = {data_json};

let state = {{
  region: 'All',
  category: 'All',
  year: 'All',
  shipMode: 'All',
  filteredData: [...rawData]
}};

/* Helper formatters */
const fmtCur = (num) => '$' + Number(num || 0).toLocaleString('en-US', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
const fmtInt = (num) => Number(num || 0).toLocaleString('en-US');
const fmtPct = (num) => Number(num || 0).toFixed(2) + '%';

const tooltipEl = document.getElementById('chartTooltip');
function showTooltip(x, y, html) {{
  tooltipEl.innerHTML = html;
  tooltipEl.style.left = (x + 15) + 'px';
  tooltipEl.style.top = (y - 20) + 'px';
  tooltipEl.style.opacity = '1';
}}
function hideTooltip() {{
  tooltipEl.style.opacity = '0';
}}

function getThemeColors() {{
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  return {{
    isDark,
    text: isDark ? '#9CA3AF' : '#475569',
    textLight: isDark ? '#E5E7EB' : '#1E293B',
    grid: isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(15, 23, 42, 0.08)',
    primary: '#3B82F6',
    primaryGradStart: 'rgba(59, 130, 246, 0.35)',
    primaryGradEnd: 'rgba(59, 130, 246, 0.0)',
    emerald: '#10B981',
    amber: '#F59E0B',
    purple: '#8B5CF6',
    rose: '#F43F5E',
    cyan: '#06B6D4'
  }};
}}

function initCanvas(canvas) {{
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();
  canvas.width = rect.width * dpr;
  canvas.height = rect.height * dpr;
  const ctx = canvas.getContext('2d');
  ctx.resetTransform && ctx.resetTransform();
  ctx.scale(dpr, dpr);
  return {{ ctx, width: rect.width, height: rect.height }};
}}

/* =============================================================================
   CHART RENDERERS (100% Native, Offline-Ready, No External CDN Required)
   ============================================================================= */

// 1. Monthly Revenue & Revenue LM Line Trend
function renderMonthlyTrend(data) {{
  const canvas = document.getElementById('monthlyTrendCanvas');
  if (!canvas) return;
  const {{ ctx, width, height }} = initCanvas(canvas);
  const colors = getThemeColors();

  const monthly = {{}};
  data.forEach(d => {{
    const m = (d.OrderDate || '').substring(0, 7);
    if (!m) return;
    if (!monthly[m]) monthly[m] = {{ rev: 0, profit: 0 }};
    monthly[m].rev += d.Sales;
    monthly[m].profit += d.Profit;
  }});

  const months = Object.keys(monthly).sort();
  if (!months.length) return;

  const revs = months.map(m => monthly[m].rev);
  const revLMs = months.map((m, idx) => idx === 0 ? null : monthly[months[idx-1]].rev);

  const padL = 60, padR = 24, padT = 28, padB = 40;
  const chartW = width - padL - padR;
  const chartH = height - padT - padB;

  const maxVal = Math.max(...revs, ...(revLMs.filter(v=>v!==null)), 1000) * 1.15;

  // Grid lines & Y-ticks
  ctx.strokeStyle = colors.grid;
  ctx.lineWidth = 1;
  ctx.fillStyle = colors.text;
  ctx.font = '10px ' + getComputedStyle(document.body).fontFamily;
  ctx.textAlign = 'right';

  const steps = 4;
  for (let i = 0; i <= steps; i++) {{
    const yVal = (maxVal / steps) * i;
    const yPos = padT + chartH - (i / steps) * chartH;
    ctx.beginPath();
    ctx.moveTo(padL, yPos);
    ctx.lineTo(width - padR, yPos);
    ctx.stroke();
    ctx.fillText('$' + (yVal >= 1000 ? (yVal/1000).toFixed(0) + 'k' : yVal.toFixed(0)), padL - 8, yPos + 3);
  }}

  // X-ticks
  ctx.textAlign = 'center';
  const xStep = chartW / Math.max(months.length - 1, 1);
  const points = [];

  months.forEach((m, idx) => {{
    const x = padL + idx * xStep;
    const y = padT + chartH - (revs[idx] / maxVal) * chartH;
    points.push({{ x, y, rev: revs[idx], revLM: revLMs[idx], month: m }});
    
    // Label alternate or quarterly ticks if too crowded
    if (months.length <= 12 || idx % 2 === 0 || idx === months.length - 1) {{
      const shortM = m.substring(2); // '24-01'
      ctx.fillText(shortM, x, height - padB + 16);
    }}
  }});

  // Revenue Area Gradient Fill
  const grad = ctx.createLinearGradient(0, padT, 0, padT + chartH);
  grad.addColorStop(0, colors.primaryGradStart);
  grad.addColorStop(1, colors.primaryGradEnd);

  ctx.beginPath();
  ctx.moveTo(points[0].x, padT + chartH);
  points.forEach(p => ctx.lineTo(p.x, p.y));
  ctx.lineTo(points[points.length - 1].x, padT + chartH);
  ctx.closePath();
  ctx.fillStyle = grad;
  ctx.fill();

  // Revenue LM Dashed Line
  ctx.save();
  ctx.setLineDash([4, 4]);
  ctx.strokeStyle = colors.emerald;
  ctx.lineWidth = 2;
  ctx.beginPath();
  let firstLM = true;
  points.forEach(p => {{
    if (p.revLM !== null) {{
      const yLM = padT + chartH - (p.revLM / maxVal) * chartH;
      if (firstLM) {{
        ctx.moveTo(p.x, yLM);
        firstLM = false;
      }} else {{
        ctx.lineTo(p.x, yLM);
      }}
    }}
  }});
  ctx.stroke();
  ctx.restore();

  // Revenue Main Line
  ctx.strokeStyle = colors.primary;
  ctx.lineWidth = 3;
  ctx.beginPath();
  points.forEach((p, idx) => {{
    if (idx === 0) ctx.moveTo(p.x, p.y);
    else ctx.lineTo(p.x, p.y);
  }});
  ctx.stroke();

  // Points
  points.forEach(p => {{
    ctx.fillStyle = colors.primary;
    ctx.beginPath();
    ctx.arc(p.x, p.y, 4, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#FFFFFF';
    ctx.lineWidth = 1.5;
    ctx.stroke();
  }});

  // Tooltip Interaction
  canvas.onmousemove = (e) => {{
    const rect = canvas.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;

    let closest = null;
    let minD = 25;
    points.forEach(p => {{
      const d = Math.abs(p.x - mouseX);
      if (d < minD) {{
        minD = d;
        closest = p;
      }}
    }});

    if (closest) {{
      const momText = closest.revLM ? (((closest.rev - closest.revLM) / closest.revLM) * 100).toFixed(1) + '%' : 'N/A';
      const momColor = closest.rev >= (closest.revLM || 0) ? colors.emerald : colors.rose;
      showTooltip(e.pageX, e.pageY, `
        <strong>${{closest.month}}</strong><br/>
        Revenue: <span style="color:${{colors.primary}}">${{fmtCur(closest.rev)}}</span><br/>
        Revenue LM: <span style="color:${{colors.emerald}}">${{closest.revLM ? fmtCur(closest.revLM) : 'N/A'}}</span><br/>
        MoM Growth: <span style="color:${{momColor}}">${{momText}}</span>
      `);
    }} else {{
      hideTooltip();
    }}
  }};
  canvas.onmouseleave = hideTooltip;
}}

// 2. Revenue Share by Category Donut Chart
function renderCategoryDonut(data) {{
  const canvas = document.getElementById('categoryDonutCanvas');
  if (!canvas) return;
  const {{ ctx, width, height }} = initCanvas(canvas);
  const colors = getThemeColors();

  const catRev = {{ 'Furniture': 0, 'Technology': 0, 'Office Supplies': 0 }};
  data.forEach(d => {{
    if (catRev[d.Category] !== undefined) catRev[d.Category] += d.Sales;
  }});

  const total = Object.values(catRev).reduce((a,b)=>a+b, 0) || 1;
  const slices = [
    {{ name: 'Technology', val: catRev['Technology'], color: colors.primary }},
    {{ name: 'Office Supplies', val: catRev['Office Supplies'], color: colors.emerald }},
    {{ name: 'Furniture', val: catRev['Furniture'], color: colors.amber }}
  ];

  const cx = width / 2;
  const cy = height / 2;
  const radius = Math.min(cx, cy) - 14;
  const innerRadius = radius * 0.65;

  let startAngle = -Math.PI / 2;
  slices.forEach(s => {{
    const sliceAngle = (s.val / total) * Math.PI * 2;
    s.start = startAngle;
    s.end = startAngle + sliceAngle;
    s.pct = (s.val / total) * 100;

    ctx.beginPath();
    ctx.arc(cx, cy, radius, s.start, s.end);
    ctx.arc(cx, cy, innerRadius, s.end, s.start, true);
    ctx.closePath();
    ctx.fillStyle = s.color;
    ctx.fill();

    startAngle += sliceAngle;
  }});

  // Center text
  ctx.fillStyle = colors.textLight;
  ctx.font = 'bold 13px ' + getComputedStyle(document.body).fontFamily;
  ctx.textAlign = 'center';
  ctx.fillText('Categories', cx, cy - 4);
  ctx.fillStyle = colors.text;
  ctx.font = '11px ' + getComputedStyle(document.body).fontFamily;
  ctx.fillText('100% Split', cx, cy + 12);

  // Legend HTML
  const legContainer = document.getElementById('categoryLegend');
  legContainer.innerHTML = slices.map(s => `
    <div class="legend-item">
      <div class="legend-dot" style="background:${{s.color}};"></div>
      <span>${{s.name}}: <strong>${{s.pct.toFixed(1)}}%</strong></span>
    </div>
  `).join('');

  canvas.onmousemove = (e) => {{
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left - cx;
    const my = e.clientY - rect.top - cy;
    const dist = Math.sqrt(mx * mx + my * my);
    if (dist >= innerRadius && dist <= radius) {{
      let angle = Math.atan2(my, mx);
      if (angle < -Math.PI / 2) angle += Math.PI * 2;
      const found = slices.find(s => angle >= s.start && angle < s.end);
      if (found) {{
        showTooltip(e.pageX, e.pageY, `<strong>${{found.name}}</strong><br/>Revenue: ${{fmtCur(found.val)}} (${{found.pct.toFixed(1)}}%)`);
        return;
      }}
    }}
    hideTooltip();
  }};
  canvas.onmouseleave = hideTooltip;
}}

// 3. Regional Revenue & Profit Clustered Bar
function renderRegionBar(data) {{
  const canvas = document.getElementById('regionBarCanvas');
  if (!canvas) return;
  const {{ ctx, width, height }} = initCanvas(canvas);
  const colors = getThemeColors();

  const regData = {{ 'East': {{ rev: 0, profit: 0 }}, 'North': {{ rev: 0, profit: 0 }}, 'South': {{ rev: 0, profit: 0 }}, 'West': {{ rev: 0, profit: 0 }} }};
  data.forEach(d => {{
    if (regData[d.Region]) {{
      regData[d.Region].rev += d.Sales;
      regData[d.Region].profit += d.Profit;
    }}
  }});

  const regions = Object.keys(regData);
  const maxVal = Math.max(...regions.map(r => Math.max(regData[r].rev, regData[r].profit)), 1000) * 1.15;

  const padL = 60, padR = 24, padT = 24, padB = 36;
  const chartW = width - padL - padR;
  const chartH = height - padT - padB;

  // Gridlines
  ctx.strokeStyle = colors.grid;
  ctx.lineWidth = 1;
  ctx.fillStyle = colors.text;
  ctx.font = '10px ' + getComputedStyle(document.body).fontFamily;
  ctx.textAlign = 'right';

  const steps = 4;
  for (let i = 0; i <= steps; i++) {{
    const yVal = (maxVal / steps) * i;
    const yPos = padT + chartH - (i / steps) * chartH;
    ctx.beginPath();
    ctx.moveTo(padL, yPos);
    ctx.lineTo(width - padR, yPos);
    ctx.stroke();
    ctx.fillText('$' + (yVal >= 1000000 ? (yVal/1000000).toFixed(1) + 'M' : (yVal/1000).toFixed(0) + 'k'), padL - 8, yPos + 3);
  }}

  const groupW = chartW / regions.length;
  const barW = Math.min(groupW * 0.32, 34);
  const gap = 4;
  const hoverBoxes = [];

  regions.forEach((r, idx) => {{
    const gCenter = padL + idx * groupW + groupW / 2;
    const rX = gCenter - barW - gap/2;
    const pX = gCenter + gap/2;

    const rH = (regData[r].rev / maxVal) * chartH;
    const pH = (regData[r].profit / maxVal) * chartH;

    const rY = padT + chartH - rH;
    const pY = padT + chartH - pH;

    // Revenue Bar (Blue)
    ctx.fillStyle = colors.primary;
    ctx.beginPath();
    ctx.roundRect ? ctx.roundRect(rX, rY, barW, rH, [4, 4, 0, 0]) : ctx.rect(rX, rY, barW, rH);
    ctx.fill();

    // Profit Bar (Emerald)
    ctx.fillStyle = colors.emerald;
    ctx.beginPath();
    ctx.roundRect ? ctx.roundRect(pX, pY, barW, pH, [4, 4, 0, 0]) : ctx.rect(pX, pY, barW, pH);
    ctx.fill();

    // X-label
    ctx.fillStyle = colors.textLight;
    ctx.font = 'bold 11px ' + getComputedStyle(document.body).fontFamily;
    ctx.textAlign = 'center';
    ctx.fillText(r, gCenter, height - padB + 16);

    hoverBoxes.push({{ x1: rX, x2: pX + barW, y: Math.min(rY, pY), r, rev: regData[r].rev, profit: regData[r].profit }});
  }});

  canvas.onmousemove = (e) => {{
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const found = hoverBoxes.find(b => mx >= b.x1 - 10 && mx <= b.x2 + 10);
    if (found) {{
      const margin = (found.profit / found.rev) * 100;
      showTooltip(e.pageX, e.pageY, `
        <strong>${{found.r}} Region</strong><br/>
        Revenue: <span style="color:${{colors.primary}}">${{fmtCur(found.rev)}}</span><br/>
        Profit: <span style="color:${{colors.emerald}}">${{fmtCur(found.profit)}}</span><br/>
        Margin: <strong>${{margin.toFixed(2)}}%</strong>
      `);
    }} else {{
      hideTooltip();
    }}
  }};
  canvas.onmouseleave = hideTooltip;
}}

// 4. Top Products RANKX Horizontal Bar Chart
function renderProductRank(data) {{
  const canvas = document.getElementById('productRankCanvas');
  if (!canvas) return;
  const {{ ctx, width, height }} = initCanvas(canvas);
  const colors = getThemeColors();

  const prodRev = {{}};
  data.forEach(d => prodRev[d.Product] = (prodRev[d.Product] || 0) + d.Sales);
  const prods = Object.entries(prodRev).sort((a,b)=>b[1]-a[1]).slice(0, 10);
  if (!prods.length) return;

  const maxVal = prods[0][1] * 1.12;
  const padL = 110, padR = 60, padT = 16, padB = 16;
  const chartW = width - padL - padR;
  const chartH = height - padT - padB;
  const barH = chartH / prods.length;

  const hoverRows = [];

  prods.forEach(([name, rev], idx) => {{
    const y = padT + idx * barH;
    const bW = (rev / maxVal) * chartW;

    // Label
    ctx.fillStyle = colors.textLight;
    ctx.font = '11px ' + getComputedStyle(document.body).fontFamily;
    ctx.textAlign = 'right';
    ctx.fillText(`#${{idx+1}} ${{name}}`, padL - 10, y + barH/2 + 4);

    // Bar background track
    ctx.fillStyle = colors.grid;
    ctx.beginPath();
    ctx.roundRect ? ctx.roundRect(padL, y + 4, chartW, barH - 8, 4) : ctx.rect(padL, y + 4, chartW, barH - 8);
    ctx.fill();

    // Bar
    ctx.fillStyle = colors.purple;
    ctx.beginPath();
    ctx.roundRect ? ctx.roundRect(padL, y + 4, bW, barH - 8, 4) : ctx.rect(padL, y + 4, bW, barH - 8);
    ctx.fill();

    // Value text
    ctx.fillStyle = colors.text;
    ctx.font = '10px ' + getComputedStyle(document.body).fontFamily;
    ctx.textAlign = 'left';
    ctx.fillText('$' + (rev >= 1000 ? (rev/1000).toFixed(0) + 'k' : rev.toFixed(0)), padL + bW + 8, y + barH/2 + 4);

    hoverRows.push({{ y, h: barH, name, rev, rank: idx+1 }});
  }});

  canvas.onmousemove = (e) => {{
    const rect = canvas.getBoundingClientRect();
    const my = e.clientY - rect.top;
    const found = hoverRows.find(r => my >= r.y && my <= r.y + r.h);
    if (found) {{
      showTooltip(e.pageX, e.pageY, `<strong>#${{found.rank}} ${{found.name}}</strong><br/>Revenue: ${{fmtCur(found.rev)}}`);
    }} else {{
      hideTooltip();
    }}
  }};
  canvas.onmouseleave = hideTooltip;
}}

// 5. Discount vs Margin Scatter / Bubble Plot
function renderDiscountScatter(data) {{
  const canvas = document.getElementById('discountScatterCanvas');
  if (!canvas) return;
  const {{ ctx, width, height }} = initCanvas(canvas);
  const colors = getThemeColors();

  const pAgg = {{}};
  data.forEach(d => {{
    if (!pAgg[d.Product]) pAgg[d.Product] = {{ product: d.Product, cat: d.Category, sales: 0, profit: 0, discs: [] }};
    pAgg[d.Product].sales += d.Sales;
    pAgg[d.Product].profit += d.Profit;
    pAgg[d.Product].discs.push(d.Discount);
  }});

  const prods = Object.values(pAgg).map(p => ({{
    ...p,
    avgDisc: (p.discs.reduce((a,b)=>a+b,0) / p.discs.length) * 100,
    marginPct: (p.profit / p.sales) * 100
  }}));

  if (!prods.length) return;

  const padL = 46, padR = 24, padT = 24, padB = 40;
  const chartW = width - padL - padR;
  const chartH = height - padT - padB;

  const minX = 0, maxX = 12;
  const minY = 10, maxY = 35;

  // Gridlines
  ctx.strokeStyle = colors.grid;
  ctx.lineWidth = 1;
  ctx.fillStyle = colors.text;
  ctx.font = '10px ' + getComputedStyle(document.body).fontFamily;

  // Y-ticks
  ctx.textAlign = 'right';
  for (let yVal = 10; yVal <= 35; yVal += 5) {{
    const yPos = padT + chartH - ((yVal - minY) / (maxY - minY)) * chartH;
    ctx.beginPath();
    ctx.moveTo(padL, yPos);
    ctx.lineTo(width - padR, yPos);
    ctx.stroke();
    ctx.fillText(yVal + '%', padL - 6, yPos + 3);
  }}

  // X-ticks
  ctx.textAlign = 'center';
  for (let xVal = 0; xVal <= 12; xVal += 2) {{
    const xPos = padL + ((xVal - minX) / (maxX - minX)) * chartW;
    ctx.beginPath();
    ctx.moveTo(xPos, padT);
    ctx.lineTo(xPos, padT + chartH);
    ctx.stroke();
    ctx.fillText(xVal + '%', xPos, height - padB + 16);
  }}

  // Target Margin Line (25%)
  const targetY = padT + chartH - ((25 - minY) / (maxY - minY)) * chartH;
  ctx.strokeStyle = colors.rose;
  ctx.setLineDash([3, 3]);
  ctx.beginPath();
  ctx.moveTo(padL, targetY);
  ctx.lineTo(width - padR, targetY);
  ctx.stroke();
  ctx.setLineDash([]);

  // Bubbles
  const maxSales = Math.max(...prods.map(p => p.sales), 1);
  const bubbles = [];

  prods.forEach(p => {{
    const cx = padL + Math.max(0, Math.min(chartW, ((p.avgDisc - minX) / (maxX - minX)) * chartW));
    const cy = padT + chartH - Math.max(0, Math.min(chartH, ((p.marginPct - minY) / (maxY - minY)) * chartH));
    const r = Math.max(6, Math.min(22, (p.sales / maxSales) * 22));

    const color = p.cat === 'Technology' ? colors.primary : p.cat === 'Office Supplies' ? colors.emerald : colors.amber;

    ctx.fillStyle = color;
    ctx.globalAlpha = 0.75;
    ctx.beginPath();
    ctx.arc(cx, cy, r, 0, Math.PI * 2);
    ctx.fill();
    ctx.globalAlpha = 1.0;
    ctx.strokeStyle = '#FFFFFF';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    bubbles.push({{ cx, cy, r, p }});
  }});

  canvas.onmousemove = (e) => {{
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;

    const found = bubbles.find(b => {{
      const dx = mx - b.cx;
      const dy = my - b.cy;
      return (dx * dx + dy * dy) <= (b.r + 4) * (b.r + 4);
    }});

    if (found) {{
      showTooltip(e.pageX, e.pageY, `
        <strong>${{found.p.product}}</strong> (${{found.p.cat}})<br/>
        Avg Discount: <strong>${{found.p.avgDisc.toFixed(1)}}%</strong><br/>
        Profit Margin: <strong>${{found.p.marginPct.toFixed(1)}}%</strong><br/>
        Revenue: ${{fmtCur(found.p.sales)}}
      `);
    }} else {{
      hideTooltip();
    }}
  }};
  canvas.onmouseleave = hideTooltip;
}}

// 6. Ship Mode Efficiency Combo Chart
function renderShipModeChart(data) {{
  const canvas = document.getElementById('shipModeCanvas');
  if (!canvas) return;
  const {{ ctx, width, height }} = initCanvas(canvas);
  const colors = getThemeColors();

  const shipModes = ['Standard Class', 'Second Class', 'First Class', 'Same Day'];
  const modeData = shipModes.map(m => {{
    const subset = data.filter(d => d.ShipMode === m);
    return {{
      mode: m,
      count: subset.length,
      days: subset.length ? subset.reduce((a,b)=>a+b.ShippingDays,0)/subset.length : 0
    }};
  }});

  const padL = 46, padR = 46, padT = 20, padB = 34;
  const chartW = width - padL - padR;
  const chartH = height - padT - padB;
  const maxCount = Math.max(...modeData.map(m => m.count), 10) * 1.2;

  const stepW = chartW / modeData.length;
  const barW = stepW * 0.45;

  // Gridlines
  ctx.strokeStyle = colors.grid;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(padL, padT + chartH);
  ctx.lineTo(width - padR, padT + chartH);
  ctx.stroke();

  modeData.forEach((m, idx) => {{
    const cx = padL + idx * stepW + stepW / 2;
    const bH = (m.count / maxCount) * chartH;
    const bY = padT + chartH - bH;

    // Bar
    ctx.fillStyle = colors.cyan;
    ctx.beginPath();
    ctx.roundRect ? ctx.roundRect(cx - barW/2, bY, barW, bH, [4, 4, 0, 0]) : ctx.rect(cx - barW/2, bY, barW, bH);
    ctx.fill();

    // Label
    ctx.fillStyle = colors.text;
    ctx.font = '10px ' + getComputedStyle(document.body).fontFamily;
    ctx.textAlign = 'center';
    ctx.fillText(m.mode.replace(' Class', ''), cx, height - padB + 16);
  }});
}}

// 7. Regional Margin Index
function renderRegionalMarginChart(data) {{
  const canvas = document.getElementById('regionalMarginCanvas');
  if (!canvas) return;
  const {{ ctx, width, height }} = initCanvas(canvas);
  const colors = getThemeColors();

  const regAgg = {{}};
  data.forEach(d => {{
    if (!regAgg[d.Region]) regAgg[d.Region] = {{ rev: 0, profit: 0 }};
    regAgg[d.Region].rev += d.Sales;
    regAgg[d.Region].profit += d.Profit;
  }});

  const rNames = Object.keys(regAgg);
  const rMargins = rNames.map(r => (regAgg[r].profit / (regAgg[r].rev || 1)) * 100);

  const padL = 46, padR = 24, padT = 20, padB = 34;
  const chartW = width - padL - padR;
  const chartH = height - padT - padB;
  const maxMargin = 35;

  const stepW = chartW / rNames.length;
  const barW = stepW * 0.45;

  rNames.forEach((r, idx) => {{
    const cx = padL + idx * stepW + stepW / 2;
    const m = rMargins[idx];
    const bH = (m / maxMargin) * chartH;
    const bY = padT + chartH - bH;

    ctx.fillStyle = colors.emerald;
    ctx.beginPath();
    ctx.roundRect ? ctx.roundRect(cx - barW/2, bY, barW, bH, [4, 4, 0, 0]) : ctx.rect(cx - barW/2, bY, barW, bH);
    ctx.fill();

    ctx.fillStyle = colors.text;
    ctx.font = 'bold 10px ' + getComputedStyle(document.body).fontFamily;
    ctx.textAlign = 'center';
    ctx.fillText(m.toFixed(1) + '%', cx, bY - 6);
    ctx.fillText(r, cx, height - padB + 16);
  }});
}}

/* =============================================================================
   TABLES & KPI CONTROLLERS
   ============================================================================= */

function renderTopOrdersTable(data) {{
  const sorted = [...data].sort((a,b) => b.Sales - a.Sales).slice(0, 10);
  const tbody = document.querySelector('#topOrdersTable tbody');
  if (!tbody) return;
  tbody.innerHTML = sorted.map(o => `
    <tr>
      <td style="font-family:var(--font-mono); font-weight:600; color:var(--primary);">${{o.OrderID}}</td>
      <td>${{o.OrderDate}}</td>
      <td style="font-weight:600;">${{o.CustomerName}}</td>
      <td>${{o.Product}}</td>
      <td class="num-cell" style="font-weight:700;">${{fmtCur(o.Sales)}}</td>
      <td class="num-cell" style="color:var(--accent-emerald); font-weight:600;">${{fmtCur(o.Profit)}}</td>
    </tr>
  `).join('');
}}

function renderProductMatrixTable(data) {{
  const pAgg = {{}};
  data.forEach(d => {{
    if (!pAgg[d.Product]) pAgg[d.Product] = {{ product: d.Product, category: d.Category, units: 0, sales: 0, profit: 0, discs: [] }};
    pAgg[d.Product].units += d.Quantity;
    pAgg[d.Product].sales += d.Sales;
    pAgg[d.Product].profit += d.Profit;
    pAgg[d.Product].discs.push(d.Discount);
  }});

  const prods = Object.values(pAgg).map(p => ({{
    ...p,
    avgDiscount: (p.discs.reduce((a,b)=>a+b,0) / p.discs.length) * 100,
    marginPct: (p.profit / p.sales) * 100
  }})).sort((a,b) => b.sales - a.sales);

  const maxSales = Math.max(...prods.map(p => p.sales), 1);
  const tbody = document.querySelector('#productMatrixTable tbody');
  if (!tbody) return;

  tbody.innerHTML = prods.map(p => {{
    const barWidth = ((p.sales / maxSales) * 100).toFixed(0);
    const catClass = p.category === 'Technology' ? 'cat-tech' : p.category === 'Office Supplies' ? 'cat-office' : 'cat-furniture';
    const marginClass = p.marginPct >= 28 ? 'margin-high' : p.marginPct >= 22 ? 'margin-med' : 'margin-low';

    return `
      <tr>
        <td style="font-weight:700;">${{p.product}}</td>
        <td><span class="category-pill ${{catClass}}">${{p.category}}</span></td>
        <td class="num-cell">${{fmtInt(p.units)}}</td>
        <td class="num-cell">
          <div class="data-bar-wrapper">
            <span>${{fmtCur(p.sales)}}</span>
            <div class="data-bar-container"><div class="data-bar-fill" style="width:${{barWidth}}%;"></div></div>
          </div>
        </td>
        <td class="num-cell" style="font-weight:600; color:var(--accent-emerald);">${{fmtCur(p.profit)}}</td>
        <td class="num-cell">${{fmtPct(p.avgDiscount)}}</td>
        <td class="num-cell"><span class="margin-tag ${{marginClass}}">${{fmtPct(p.marginPct)}}</span></td>
      </tr>
    `;
  }}).join('');
}}

function renderCustomerAccountsTable(data) {{
  const cAgg = {{}};
  data.forEach(d => {{
    if (!cAgg[d.CustomerID]) {{
      cAgg[d.CustomerID] = {{ id: d.CustomerID, name: d.CustomerName, region: d.Region, orders: 0, units: 0, sales: 0, profit: 0 }};
    }}
    cAgg[d.CustomerID].orders += 1;
    cAgg[d.CustomerID].units += d.Quantity;
    cAgg[d.CustomerID].sales += d.Sales;
    cAgg[d.CustomerID].profit += d.Profit;
  }});

  const sortedCust = Object.values(cAgg).sort((a,b) => b.sales - a.sales);
  const tbody = document.querySelector('#customerAccountsTable tbody');
  if (!tbody) return;

  tbody.innerHTML = sortedCust.map(c => {{
    const tier = c.sales >= 45000 ? '<span class="kpi-badge" style="background:rgba(245,158,11,0.15); color:#F59E0B;">🌟 Platinum</span>' :
                 c.sales >= 30000 ? '<span class="kpi-badge" style="background:rgba(59,130,246,0.15); color:#3B82F6;">🥇 Gold</span>' :
                                    '<span class="kpi-badge">🥈 Silver</span>';
    return `
      <tr>
        <td style="font-family:var(--font-mono); font-weight:600; color:var(--primary);">${{c.id}}</td>
        <td style="font-weight:600;">${{c.name}}</td>
        <td>${{c.region}}</td>
        <td class="num-cell">${{fmtInt(c.orders)}}</td>
        <td class="num-cell">${{fmtInt(c.units)}}</td>
        <td class="num-cell" style="font-weight:700;">${{fmtCur(c.sales)}}</td>
        <td class="num-cell" style="font-weight:600; color:var(--accent-emerald);">${{fmtCur(c.profit)}}</td>
        <td class="num-cell">${{tier}}</td>
      </tr>
    `;
  }}).join('');
}}

/* Tab Switching */
document.querySelectorAll('.tab-btn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-page').forEach(p => p.classList.remove('active'));
    
    btn.classList.add('active');
    const page = document.getElementById(btn.dataset.tab);
    if (page) {{
      page.classList.add('active');
      renderDashboard();
    }}
  }});
}});

/* Theme Switching */
const themeBtn = document.getElementById('themeToggleBtn');
themeBtn.addEventListener('click', () => {{
  const cur = document.documentElement.getAttribute('data-theme');
  const next = cur === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  themeBtn.textContent = next === 'dark' ? '☀️ Light Mode' : '🌙 Dark Mode';
  renderDashboard();
}});

/* Slicer Filtering */
['slicerRegion', 'slicerCategory', 'slicerYear', 'slicerShipMode'].forEach(id => {{
  document.getElementById(id).addEventListener('change', applyFilters);
}});

document.getElementById('resetSlicersBtn').addEventListener('click', () => {{
  document.getElementById('slicerRegion').value = 'All';
  document.getElementById('slicerCategory').value = 'All';
  document.getElementById('slicerYear').value = 'All';
  document.getElementById('slicerShipMode').value = 'All';
  applyFilters();
}});

function applyFilters() {{
  state.region = document.getElementById('slicerRegion').value;
  state.category = document.getElementById('slicerCategory').value;
  state.year = document.getElementById('slicerYear').value;
  state.shipMode = document.getElementById('slicerShipMode').value;

  state.filteredData = rawData.filter(d => {{
    if (state.region !== 'All' && d.Region !== state.region) return false;
    if (state.category !== 'All' && d.Category !== state.category) return false;
    if (state.shipMode !== 'All' && d.ShipMode !== state.shipMode) return false;
    if (state.year !== 'All') {{
      const y = (d.OrderDate || '').substring(0, 4);
      if (y !== state.year) return false;
    }}
    return true;
  }});

  renderDashboard();
}}

/* CSV Export */
document.getElementById('exportCsvBtn').addEventListener('click', () => {{
  if (!state.filteredData.length) return;
  const headers = Object.keys(state.filteredData[0]).join(',');
  const rows = state.filteredData.map(r => Object.values(r).map(v => typeof v === 'string' ? `"${{v.replace(/"/g, '""')}}"` : v).join(','));
  const csvContent = "data:text/csv;charset=utf-8," + [headers, ...rows].join("\\n");
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", "sales_data_filtered.csv");
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}});

function copyDax(btn, text) {{
  navigator.clipboard.writeText(text);
  const orig = btn.textContent;
  btn.textContent = 'Copied!';
  setTimeout(() => btn.textContent = orig, 1500);
}}

/* Main Render Controller with Safe Wrappers */
function renderDashboard() {{
  const data = state.filteredData;
  const totalRev = data.reduce((s, d) => s + (d.Sales || 0), 0);
  const totalProfit = data.reduce((s, d) => s + (d.Profit || 0), 0);
  const totalUnits = data.reduce((s, d) => s + (d.Quantity || 0), 0);
  const orderIds = new Set(data.map(d => d.OrderID));
  const totalOrders = orderIds.size || 1;
  const custIds = new Set(data.map(d => d.CustomerID));
  const totalCust = custIds.size || 1;
  const marginPct = totalRev ? (totalProfit / totalRev) * 100 : 0;
  const aov = totalRev / totalOrders;
  const avgDiscount = data.length ? (data.reduce((s, d) => s + (d.Discount || 0), 0) / data.length) * 100 : 0;
  const avgShipDays = data.length ? (data.reduce((s, d) => s + (d.ShippingDays || 0), 0) / data.length) : 0;

  // Page 1 KPIs
  document.getElementById('kpiRevenue').textContent = fmtCur(totalRev);
  document.getElementById('kpiProfit').textContent = fmtCur(totalProfit);
  document.getElementById('kpiMargin').textContent = fmtPct(marginPct);
  document.getElementById('kpiOrders').textContent = fmtInt(totalOrders);
  document.getElementById('kpiAOV').textContent = fmtCur(aov);
  document.getElementById('kpiUnitsSub').textContent = `${{fmtInt(totalUnits)}} units sold`;

  // Page 2 KPIs
  const prodRev = {{}};
  data.forEach(d => prodRev[d.Product] = (prodRev[d.Product] || 0) + d.Sales);
  const sortedProds = Object.entries(prodRev).sort((a,b) => b[1] - a[1]);
  if (sortedProds.length) {{
    document.getElementById('kpiTopProduct').textContent = sortedProds[0][0];
    document.getElementById('kpiTopProductRev').textContent = fmtCur(sortedProds[0][1]) + ' revenue';
  }}
  document.getElementById('kpiTopCatMargin').textContent = 'Technology';
  document.getElementById('kpiAvgDiscount').textContent = fmtPct(avgDiscount);
  document.getElementById('kpiProductCount').textContent = Object.keys(prodRev).length;

  // Page 3 KPIs
  document.getElementById('kpiUniqueCust').textContent = fmtInt(totalCust);
  document.getElementById('kpiOrdersPerCust').textContent = (totalOrders / totalCust).toFixed(1);
  document.getElementById('kpiAvgShipDays').textContent = avgShipDays.toFixed(1) + ' d';
  document.getElementById('kpiCustAvgSpend').textContent = fmtCur(totalRev / totalCust);

  // Safe visual executions
  try {{ renderMonthlyTrend(data); }} catch(e) {{ console.error("MonthlyTrend error:", e); }}
  try {{ renderCategoryDonut(data); }} catch(e) {{ console.error("CategoryDonut error:", e); }}
  try {{ renderRegionBar(data); }} catch(e) {{ console.error("RegionBar error:", e); }}
  try {{ renderTopOrdersTable(data); }} catch(e) {{ console.error("TopOrdersTable error:", e); }}
  try {{ renderProductRank(data); }} catch(e) {{ console.error("ProductRank error:", e); }}
  try {{ renderDiscountScatter(data); }} catch(e) {{ console.error("DiscountScatter error:", e); }}
  try {{ renderProductMatrixTable(data); }} catch(e) {{ console.error("ProductMatrixTable error:", e); }}
  try {{ renderShipModeChart(data); }} catch(e) {{ console.error("ShipModeChart error:", e); }}
  try {{ renderRegionalMarginChart(data); }} catch(e) {{ console.error("RegionalMarginChart error:", e); }}
  try {{ renderCustomerAccountsTable(data); }} catch(e) {{ console.error("CustomerAccountsTable error:", e); }}
}}

window.addEventListener('resize', renderDashboard);

// Initial Render
applyFilters();
</script>

</body>
</html>
'''

OUT_PATH.write_text(html_content, encoding="utf-8")
print(f"Compiled Standalone Native HTML Dashboard -> {OUT_PATH} (size: {len(html_content):,} bytes)")
