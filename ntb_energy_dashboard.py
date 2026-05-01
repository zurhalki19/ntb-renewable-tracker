import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from pathlib import Path
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="NTB Renewable Energy Tracker",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# MULTILINGUAL SETUP
# =========================================================
if "lang" not in st.session_state:
    st.session_state.lang = "en"

translations = {
    "en": {
        "page_title": "NTB Renewable Energy Tracker",
        "page_subtitle": "A public dashboard tracking renewable energy progress in West Nusa Tenggara.",
        "nav_situasi": "Current Situation",
        "nav_masterplan": "Energy Transition Masterplan",
        "nav_datacenter": "Data & Investment Hub",
        "hero_situasi_title": "NTB Current Energy Situation",
        "hero_situasi_desc": "Summary of the energy system, generation mix, demand, emissions, and renewable energy progress.",
        "hero_masterplan_title": "NTB Energy Transition Masterplan",
        "hero_masterplan_desc": "This page summarizes NTB’s energy transition pathway towards a cleaner, low-carbon system by 2050.",
        "hero_datacenter_title": "Data & Investment Hub",
        "hero_datacenter_desc": "Documents, sample data, project map, and summary of renewable energy investment opportunities in NTB.",
        "metric_re_share": "Renewable Share",
        "metric_re_capacity": "Installed RE Capacity",
        "metric_demand": "Electricity Demand",
        "metric_emissions": "CO₂ Emissions",
        "snapshot_dashboard": "Snapshot Dashboard",
        "tab_re_capacity": "Renewable Capacity",
        "tab_re_trend": "Renewable Share Trend",
        "tab_generation_mix": "Generation Mix",
        "tab_demand_emissions": "Demand and Emissions",
        "latest_updates": "Latest Updates",
        "read_more": "Read more →",
        "demand_trend": "Electricity Demand Trend",
        "emissions_trend": "CO₂ Emissions Pathway",
        "note_illustrative": "Note: Most values are based on extracted NTB Energy Masterplan / Net Zero 2050 pathway data. Some values, especially project coordinates and intermediate years, are indicative.",
        "nze_target": "NZE Target",
        "key_driver": "Key Driver",
        "emerging_role": "Emerging Role",
        "strategic_need": "Strategic Need",
        "transition_pathway": "Transition Pathway",
        "re_share_pathway": "Renewable Share Pathway",
        "co2_pathway": "CO₂ Emissions Pathway",
        "demand_projection": "Electricity Demand Projection",
        "capacity_pathway": "Capacity Expansion Pathway",
        "storage_pathway": "Battery Storage Pathway",
        "key_messages": "Key Messages from the Masterplan",
        "msg1": "Electricity demand is projected to increase strongly, reaching about 21.8 TWh in the NZE scenario by 2050.",
        "msg2": "Solar PV becomes the backbone of the future electricity system due to high potential and low-cost generation.",
        "msg3": "Wind development, especially in Sumbawa, supports diversification of renewable generation.",
        "msg4": "Battery storage and interconnection become critical as solar and wind penetration increases.",
        "msg5": "The NZE pathway requires fossil power phase-out and broader electrification across end-use sectors.",
        "note_pathway": "Note: Pathway values are scenario-based. Renewable share values combine available Lombok and Sumbawa indicators and should be read as indicative NTB pathway values.",
        "resource_potential": "Resource Potential",
        "investment_opportunities": "Investment Opportunities",
        "download_center": "Download Center",
        "download_project_list": "Download project pipeline (CSV)",
        "download_pathway_data": "Download capacity pathway data (CSV)",
        "project_map": "Project Map",
        "filter_tech": "Filter by technology",
        "note_datacenter": "Project coordinates are indicative placeholders because the extracted project pipeline gives locations but not exact coordinates. Official coordinates should be added later.",
        "footer_developed": "Developed by",
        "footer_anu": "Australian National University",
        "footer_based": "Based on NTB Energy Masterplan / Net Zero 2050 pathway extraction",
        "footer_illus": "Some values are scenario-based or indicative and should be verified with official data before policy or investment decisions.",
        "resource": "Resource",
        "summary": "Summary",
        "opportunity": "Opportunity",
        "focus_area": "Potential Focus Area",
        "stage": "Stage",
        "dataset": "Dataset / Document",
        "status": "Status",
        "popup_technology": "Technology",
        "popup_capacity": "Capacity",
        "popup_status": "Status",
        "popup_location": "Location",
        "popup_developer": "Developer",
        "news1_title": "NTB’s energy transition needs stronger data visibility",
        "news1_text": "This dashboard helps present key energy, pathway, and investment data in one public-facing platform.",
        "news2_title": "Solar and wind dominate the NZE pathway",
        "news2_text": "The pathway shows rapid expansion of solar PV and wind, especially in Sumbawa, supported by storage.",
        "news3_title": "Electricity demand may rise sharply by 2050",
        "news3_text": "Electrification and EV adoption drive strong demand growth in the NZE scenario."
    },
    "id": {
        "page_title": "NTB Renewable Energy Tracker",
        "page_subtitle": "Dasbor publik untuk memantau perkembangan energi terbarukan di Nusa Tenggara Barat.",
        "nav_situasi": "Situasi Energi Saat Ini",
        "nav_masterplan": "Masterplan Transisi Energi NTB",
        "nav_datacenter": "Data & Investment Hub",
        "hero_situasi_title": "Situasi Energi NTB Saat Ini",
        "hero_situasi_desc": "Ringkasan kondisi sistem energi, bauran listrik, demand, emisi, dan perkembangan energi terbarukan.",
        "hero_masterplan_title": "Masterplan Transisi Energi NTB",
        "hero_masterplan_desc": "Halaman ini merangkum arah transisi energi NTB menuju sistem energi yang lebih bersih dan rendah emisi hingga 2050.",
        "hero_datacenter_title": "Data & Investment Hub",
        "hero_datacenter_desc": "Dokumen, data contoh, peta proyek, dan ringkasan peluang investasi energi terbarukan di NTB.",
        "metric_re_share": "Bauran Terbarukan",
        "metric_re_capacity": "Kapasitas Terpasang EBT",
        "metric_demand": "Kebutuhan Listrik",
        "metric_emissions": "Emisi CO₂",
        "snapshot_dashboard": "Dasbor Kilat",
        "tab_re_capacity": "Kapasitas EBT",
        "tab_re_trend": "Tren Bauran EBT",
        "tab_generation_mix": "Bauran Pembangkit",
        "tab_demand_emissions": "Kebutuhan dan Emisi",
        "latest_updates": "Update Terbaru",
        "read_more": "Baca selengkapnya →",
        "demand_trend": "Tren Kebutuhan Listrik",
        "emissions_trend": "Jalur Emisi CO₂",
        "note_illustrative": "Catatan: Sebagian besar nilai berasal dari ekstraksi Masterplan Energi NTB / Net Zero 2050 pathway. Beberapa nilai, terutama koordinat proyek dan tahun antara, masih indikatif.",
        "nze_target": "Target NZE",
        "key_driver": "Penggerak Utama",
        "emerging_role": "Peran yang Muncul",
        "strategic_need": "Kebutuhan Strategis",
        "transition_pathway": "Jalur Transisi",
        "re_share_pathway": "Proyeksi Bauran EBT",
        "co2_pathway": "Proyeksi Emisi CO₂",
        "demand_projection": "Proyeksi Kebutuhan Listrik",
        "capacity_pathway": "Proyeksi Kapasitas",
        "storage_pathway": "Proyeksi Penyimpanan Baterai",
        "key_messages": "Pesan Utama dari Masterplan",
        "msg1": "Kebutuhan listrik diproyeksikan meningkat kuat, mencapai sekitar 21,8 TWh dalam skenario NZE pada 2050.",
        "msg2": "PLTS menjadi tulang punggung sistem kelistrikan masa depan karena potensi tinggi dan biaya produksi yang kompetitif.",
        "msg3": "Pengembangan angin, terutama di Sumbawa, mendukung diversifikasi pembangkit terbarukan.",
        "msg4": "Penyimpanan baterai dan interkoneksi menjadi sangat penting ketika penetrasi PLTS dan angin meningkat.",
        "msg5": "Jalur NZE membutuhkan phase-out pembangkit fosil dan elektrifikasi yang lebih luas di sektor pengguna akhir.",
        "note_pathway": "Catatan: Nilai pathway berbasis skenario. Nilai bauran EBT menggabungkan indikator Lombok dan Sumbawa yang tersedia dan perlu dibaca sebagai indikatif untuk NTB.",
        "resource_potential": "Potensi Sumber Daya",
        "investment_opportunities": "Peluang Investasi",
        "download_center": "Pusat Unduhan",
        "download_project_list": "Unduh pipeline proyek (CSV)",
        "download_pathway_data": "Unduh data pathway kapasitas (CSV)",
        "project_map": "Peta Proyek",
        "filter_tech": "Filter berdasarkan teknologi",
        "note_datacenter": "Koordinat proyek masih berupa placeholder indikatif karena pipeline proyek yang diekstrak hanya memberikan lokasi umum, bukan koordinat pasti. Koordinat resmi perlu ditambahkan nanti.",
        "footer_developed": "Dikembangkan oleh",
        "footer_anu": "Australian National University",
        "footer_based": "Berdasarkan ekstraksi Masterplan Energi NTB / Net Zero 2050 pathway",
        "footer_illus": "Beberapa nilai berbasis skenario atau indikatif dan perlu diverifikasi dengan data resmi sebelum digunakan untuk keputusan kebijakan atau investasi.",
        "resource": "Sumber Daya",
        "summary": "Ringkasan",
        "opportunity": "Peluang",
        "focus_area": "Area Fokus Potensial",
        "stage": "Tahap",
        "dataset": "Dataset / Dokumen",
        "status": "Status",
        "popup_technology": "Teknologi",
        "popup_capacity": "Kapasitas",
        "popup_status": "Status",
        "popup_location": "Lokasi",
        "popup_developer": "Pengembang",
        "news1_title": "Transisi energi NTB memerlukan visibilitas data yang lebih kuat",
        "news1_text": "Dasbor ini membantu menyajikan data energi, pathway, dan investasi dalam satu platform publik.",
        "news2_title": "PLTS dan angin mendominasi pathway NZE",
        "news2_text": "Pathway menunjukkan ekspansi cepat PLTS dan angin, terutama di Sumbawa, didukung oleh storage.",
        "news3_title": "Kebutuhan listrik dapat meningkat tajam menuju 2050",
        "news3_text": "Elektrifikasi dan adopsi kendaraan listrik mendorong pertumbuhan demand dalam skenario NZE."
    }
}


def t(key: str) -> str:
    return translations[st.session_state.lang].get(key, key)


# =========================================================
# LANGUAGE SELECTOR FIRST
# =========================================================
lang_col_1, lang_col_2 = st.columns([4, 1])
with lang_col_2:
    lang_choice = st.selectbox(
        "Language",
        ["English", "Bahasa Indonesia"],
        index=0 if st.session_state.lang == "en" else 1,
        label_visibility="collapsed",
        key="lang_selector"
    )

st.session_state.lang = "en" if lang_choice == "English" else "id"

# =========================================================
# BACKGROUND
# =========================================================
def get_base64_image(image_path: str):
    path = Path(image_path)
    if path.exists():
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


bg_gradient = """
background: linear-gradient(145deg, #d4e9ff 0%, #b8f0e6 40%, #f2f9e9 100%);
"""

bg_image = get_base64_image("background.jpg")

if bg_image:
    bg_css = f"""
    background-image:
        linear-gradient(145deg, rgba(212,233,255,0.92), rgba(184,240,230,0.92), rgba(242,249,233,0.92)),
        url("data:image/jpg;base64,{bg_image}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    """
else:
    bg_css = bg_gradient

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown(
    f"""
    <style>
    .stApp {{
        {bg_css}
    }}

    .block-container {{
        max-width: 1380px;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }}

    [data-testid="stSidebar"] {{
        display: none;
    }}

    header {{
        visibility: hidden;
    }}

    h1, h2, h3 {{
        color: #0a2e4b;
        font-weight: 700;
    }}

    .top-title {{
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #0f4c75, #3282b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.2rem;
    }}

    .top-subtitle {{
        color: #1e4a6b;
        font-size: 1.1rem;
        margin-bottom: 1.2rem;
        font-weight: 400;
    }}

    div[data-baseweb="radio"] {{
        background: rgba(255,255,255,0.5);
        backdrop-filter: blur(4px);
        border-radius: 40px;
        padding: 8px 12px;
        display: inline-flex;
        border: 1px solid rgba(255,255,255,0.6);
    }}
    div[data-baseweb="radio"] > div {{
        gap: 6px;
    }}
    div[data-baseweb="radio"] label {{
        background: transparent;
        border-radius: 30px;
        padding: 8px 22px;
        color: #0a2e4b;
        font-weight: 600;
        transition: all 0.2s ease;
    }}
    div[data-baseweb="radio"] label:hover {{
        background: rgba(50,130,184,0.15);
    }}

    .hero-strip {{
        background: linear-gradient(135deg, #0f4c75, #3282b8, #1b98b0);
        padding: 22px 28px;
        border-radius: 24px;
        color: white;
        margin-bottom: 22px;
        box-shadow: 0 12px 28px rgba(15,76,117,0.25);
    }}

    .hero-strip h2 {{
        color: white !important;
        margin-bottom: 0.3rem;
        font-size: 2rem;
    }}

    .hero-strip p {{
        color: rgba(255,255,255,0.95) !important;
        font-size: 1.1rem;
    }}

    [data-testid="stMetric"] {{
        background: rgba(255,255,255,0.85);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255,255,255,0.7);
        padding: 20px;
        border-radius: 24px;
        box-shadow: 0 8px 22px rgba(25,80,120,0.15);
        transition: transform 0.2s;
    }}
    [data-testid="stMetric"]:hover {{
        transform: translateY(-4px);
        background: rgba(255,255,255,0.95);
    }}
    [data-testid="stMetricLabel"] p {{
        color: #0f4c75 !important;
        font-weight: 600;
    }}
    [data-testid="stMetricValue"] {{
        color: #1b98b0 !important;
        font-size: 2rem !important;
        font-weight: 700;
    }}

    .soft-card {{
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255,255,255,0.7);
        border-radius: 24px;
        padding: 20px;
        box-shadow: 0 8px 22px rgba(25,80,120,0.1);
        transition: all 0.2s;
    }}
    .soft-card:hover {{
        background: rgba(255,255,255,0.98);
        box-shadow: 0 12px 28px rgba(15,76,117,0.15);
    }}

    .news-card {{
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255,255,255,0.7);
        border-radius: 24px;
        padding: 18px;
        margin-bottom: 15px;
        box-shadow: 0 8px 22px rgba(25,80,120,0.1);
        transition: all 0.2s;
        border-left: 6px solid #3282b8;
    }}
    .news-card:hover {{
        background: rgba(255,255,255,0.98);
        transform: scale(1.01);
    }}
    .news-card h4 {{
        color: #0f4c75;
        margin-bottom: 6px;
    }}

    .mini-note {{
        color: #2c6079;
        font-size: 0.92rem;
        background: rgba(255,255,255,0.65);
        padding: 8px 14px;
        border-radius: 30px;
        display: inline-block;
        margin-top: 8px;
    }}

    .footer {{
        text-align: center;
        padding-top: 20px;
        padding-bottom: 10px;
        color: #1e4a6b;
        font-size: 0.85rem;
        background: rgba(255,255,255,0.4);
        backdrop-filter: blur(2px);
        border-radius: 40px;
        margin-top: 30px;
    }}

    a {{
        color: #1b98b0 !important;
        text-decoration: none;
        font-weight: 600;
        transition: color 0.2s;
    }}
    a:hover {{
        color: #0f4c75 !important;
        text-decoration: underline;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background: rgba(255,255,255,0.4);
        backdrop-filter: blur(4px);
        border-radius: 30px;
        padding: 6px;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 30px;
        padding: 8px 20px;
        color: #0f4c75;
        font-weight: 600;
    }}
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, #0f4c75, #3282b8) !important;
        color: white !important;
    }}

    .stButton button {{
        background: linear-gradient(135deg, #0f4c75, #3282b8);
        color: white;
        border: none;
        border-radius: 40px;
        padding: 10px 28px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(15,76,117,0.3);
        transition: all 0.2s;
    }}
    .stButton button:hover {{
        background: linear-gradient(135deg, #1b98b0, #0f4c75);
        box-shadow: 0 6px 16px rgba(27,152,176,0.4);
        transform: scale(1.02);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# DATA BASED ON NTB NET ZERO 2050 PATHWAY EXTRACTION
# =========================================================
current_mix_data = pd.DataFrame({
    "Source": [
        "HSD / Diesel",
        "MFO",
        "Biodiesel",
        "Coal",
        "Hydropower",
        "Solar PV",
        "Biomass / Cofiring"
    ],
    "Share": [40.41, 16.48, 14.32, 24.76, 1.78, 2.11, 0.14]
})

current_re_capacity_data = pd.DataFrame({
    "Technology": ["Solar PV", "Wind", "Hydropower", "Geothermal", "Bioenergy"],
    "Capacity (MW)": [31, 0, 39, 10, 10]
})

current_demand_data = pd.DataFrame({
    "Year": [2021, 2025, 2030, 2050],
    "Electricity Demand (GWh)": [2290, 3277, 4745, 21800]
})

current_emission_data = pd.DataFrame({
    "Year": [2025, 2030, 2035, 2040, 2045, 2050],
    "CO2 Emissions (MtCO2)": [4.5, 3.0, 1.5, 1.0, 0.5, 0.06]
})

current_re_share_data = pd.DataFrame({
    "Year": [2025, 2030, 2040, 2050],
    "Renewable Share (%)": [19, 69, 99, 100]
})

pathway_share_data = current_re_share_data.copy()
pathway_demand_data = current_demand_data.copy()
pathway_emission_data = current_emission_data.copy()

capacity_pathway_data = pd.DataFrame({
    "Year": [2025, 2030, 2040, 2050],
    "Solar PV": [31, 1008, 4253, 9758],
    "Wind": [0, 188, 1480, 2605],
    "Hydropower": [39, 39, 52, 52],
    "Bioenergy": [10, 174, 316, 316],
    "Geothermal": [10, 10, 175, 175],
    "Natural Gas": [515, 1217, 1687, 1587],
    "Coal": [186, 206, 206, 206]
})

storage_pathway_data = pd.DataFrame({
    "Year": [2030, 2040, 2050],
    "Lombok Storage (MWh)": [1500, 4000, 6000],
    "Sumbawa Storage (MWh)": [2000, 7000, 12000]
})

resource_potential_data = pd.DataFrame({
    "Resource": ["Solar PV", "Wind", "Hydropower", "Bioenergy", "Battery Storage"],
    "Summary": [
        "Solar potential is very high, especially in Sumbawa with around 9,628 MW potential and around 1,000 MW in Lombok.",
        "Wind potential is significant, especially onshore wind in Sumbawa with around 1,667 MW potential and around 938 MW in Lombok.",
        "Hydropower potential is limited, with around 52 MW total potential across Lombok and Sumbawa.",
        "Bioenergy potential is around 297 MW in Lombok and 19 MW in Sumbawa.",
        "Battery storage is important to support solar and wind integration, with NZE requiring up to around 18 GWh by 2050 across Lombok and Sumbawa."
    ]
})

investment_data = pd.DataFrame({
    "Opportunity": [
        "Utility-scale Solar PV",
        "Onshore Wind Development",
        "Battery Storage",
        "Grid Interconnection",
        "Bioenergy Development",
        "Energy Data & GIS Support"
    ],
    "Potential Focus Area": [
        "Sumbawa and Lombok",
        "Sumbawa",
        "Lombok and Sumbawa power systems",
        "Lombok-Sumbawa system integration",
        "Lombok and selected agricultural areas",
        "Provincial energy planning and investment monitoring"
    ],
    "Stage": [
        "Priority",
        "Strategic",
        "Critical support",
        "Critical infrastructure",
        "Selective",
        "Supporting function"
    ]
})

investment_insight_data = pd.DataFrame({
    "Item": [
        "Power system cost in NZE by 2050",
        "Main investment driver",
        "Key barrier: grid",
        "Key barrier: regulation",
        "Key barrier: finance"
    ],
    "Summary": [
        "Projected to reach around 1,838 MUSD by 2050.",
        "High capital investment for solar, wind, storage, and grid infrastructure.",
        "Weak grid, isolated systems, and voltage/frequency stability limit VRE deployment.",
        "Long commissioning process, land acquisition, and local content rules can slow project delivery.",
        "High upfront investment is needed, although fuel savings may reduce long-term cost."
    ]
})

download_items = pd.DataFrame({
    "Dataset / Document": [
        "NTB Energy Masterplan summary",
        "Generation mix 2023",
        "NZE capacity pathway",
        "Resource potential data",
        "Project pipeline sample"
    ],
    "Status": ["Extracted", "Available", "Available", "Available", "Available"]
})

project_data = pd.DataFrame({
    "Project": [
        "Lombok Peaker",
        "Sedau Kumbi",
        "Lombok FTP-2",
        "Lunyuk Solar",
        "Medang Solar",
        "Dedieselisasi Solar",
        "Sumbawa-2",
        "Kokok Babak",
        "Sumbawa-Bima Solar",
        "Lombok Mini Hydro",
        "Sumbawa-Bima Biomass",
        "Sumbawa-Bima Geothermal",
        "Lombok 3 EBT Base",
        "Lombok 4 EBT Base"
    ],
    "Technology": [
        "Gas",
        "Hydropower",
        "Coal",
        "Solar PV",
        "Solar PV",
        "Solar PV",
        "Gas",
        "Hydropower",
        "Solar PV",
        "Hydropower",
        "Biomass",
        "Geothermal",
        "Renewable Base",
        "Renewable Base"
    ],
    "Capacity (MW)": [10, 1.3, 100, 2, 0.3, 8.4, 30, 2.3, 10, 1.75, 10, 10, 100, 100],
    "Status": [
        "Operational",
        "Operational",
        "Under construction",
        "Plan",
        "Operational",
        "Plan",
        "Bidding",
        "Under construction",
        "Plan",
        "Plan",
        "Plan",
        "Plan",
        "Plan",
        "Plan"
    ],
    "Developer": ["PLN", "IPP", "PLN", "PLN", "PLN", "IPP", "PLN", "IPP", "IPP", "IPP", "IPP", "PLN", "PLN", "PLN"],
    "Location": [
        "Lombok",
        "Lombok",
        "Lombok",
        "Lunyuk / Isolated System",
        "Medang / Isolated System",
        "Isolated System",
        "Sumbawa",
        "Lombok",
        "Sumbawa-Bima",
        "Lombok",
        "Sumbawa-Bima",
        "Sumbawa-Bima",
        "Lombok",
        "Lombok"
    ],
    "lat": [-8.65, -8.60, -8.70, -8.95, -8.50, -8.80, -8.55, -8.58, -8.45, -8.65, -8.50, -8.45, -8.70, -8.70],
    "lon": [116.30, 116.25, 116.35, 117.20, 117.10, 117.30, 117.45, 116.28, 118.20, 116.30, 118.30, 118.25, 116.35, 116.40]
})

news_items = [
    {"title_key": "news1_title", "text_key": "news1_text", "link": "https://example.com/update1"},
    {"title_key": "news2_title", "text_key": "news2_text", "link": "https://example.com/update2"},
    {"title_key": "news3_title", "text_key": "news3_text", "link": "https://example.com/update3"}
]

color_map = {
    "Solar PV": "#f3c742",
    "Wind": "#8b5cf6",
    "Hydropower": "#3b82f6",
    "Bioenergy": "#7cb342",
    "Biomass": "#7cb342",
    "Biomass / Cofiring": "#7cb342",
    "Geothermal": "#ef4444",
    "Battery Storage": "#f97316",
    "HSD / Diesel": "#2c7fb8",
    "MFO": "#64748b",
    "Biodiesel": "#14b8a6",
    "Coal": "#475569",
    "Natural Gas": "#38bdf8",
    "Gas": "#38bdf8",
    "Renewable Base": "#22c55e"
}


def get_folium_color(tech: str) -> str:
    colors = {
        "Solar PV": "orange",
        "Wind": "purple",
        "Hydropower": "blue",
        "Biomass": "green",
        "Bioenergy": "green",
        "Geothermal": "red",
        "Gas": "lightblue",
        "Coal": "darkgray",
        "Renewable Base": "green"
    }
    return colors.get(tech, "gray")


# =========================================================
# HEADER
# =========================================================
col_title, _ = st.columns([4, 1])
with col_title:
    st.markdown(f'<div class="top-title">{t("page_title")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="top-subtitle">{t("page_subtitle")}</div>', unsafe_allow_html=True)

page_options = ["situasi", "masterplan", "datacenter"]
page_label = {
    "situasi": t("nav_situasi"),
    "masterplan": t("nav_masterplan"),
    "datacenter": t("nav_datacenter")
}

page = st.radio(
    "Main navigation",
    page_options,
    format_func=lambda x: page_label[x],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("---")

# =========================================================
# PAGE 1: CURRENT SITUATION
# =========================================================
if page == "situasi":
    st.markdown(
        f"""
        <div class="hero-strip">
            <h2>{t('hero_situasi_title')}</h2>
            <p>{t('hero_situasi_desc')}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    total_re_capacity = current_re_capacity_data["Capacity (MW)"].sum()

    k1, k2, k3, k4 = st.columns(4)
    k1.metric(t("metric_re_share"), "19%")
    k2.metric(t("metric_re_capacity"), f"{total_re_capacity:.0f} MW")
    k3.metric(t("metric_demand"), "2,290 GWh")
    k4.metric(t("metric_emissions"), "~4.5 MtCO₂")

    st.markdown(f"### {t('snapshot_dashboard')}")
    left, right = st.columns([2.1, 1])

    with left:
        tab1, tab2, tab3 = st.tabs([
            t("tab_re_capacity"),
            t("tab_re_trend"),
            t("tab_generation_mix")
        ])

        with tab1:
            fig1 = px.bar(
                current_re_capacity_data,
                x="Technology",
                y="Capacity (MW)",
                color="Technology",
                color_discrete_map=color_map,
                title=t("tab_re_capacity")
            )
            fig1.update_layout(showlegend=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.8)")
            st.plotly_chart(fig1, use_container_width=True)

        with tab2:
            fig2 = px.line(
                current_re_share_data,
                x="Year",
                y="Renewable Share (%)",
                markers=True,
                title=t("tab_re_trend")
            )
            fig2.update_traces(line=dict(width=3))
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.8)")
            st.plotly_chart(fig2, use_container_width=True)

        with tab3:
            fig3 = px.pie(
                current_mix_data,
                names="Source",
                values="Share",
                title=t("tab_generation_mix"),
                color="Source",
                color_discrete_map=color_map
            )
            fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig3, use_container_width=True)

    with right:
        st.markdown(f"### {t('latest_updates')}")
        for item in news_items:
            st.markdown(
                f"""
                <div class="news-card">
                    <h4>{t(item['title_key'])}</h4>
                    <p>{t(item['text_key'])}</p>
                    <a href="{item['link']}" target="_blank">{t('read_more')}</a>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(f"### {t('tab_demand_emissions')}")
    c1, c2 = st.columns(2)

    with c1:
        fig4 = px.line(
            current_demand_data,
            x="Year",
            y="Electricity Demand (GWh)",
            markers=True,
            title=t("demand_trend")
        )
        fig4.update_traces(line=dict(width=3))
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.8)")
        st.plotly_chart(fig4, use_container_width=True)

    with c2:
        fig5 = px.line(
            current_emission_data,
            x="Year",
            y="CO2 Emissions (MtCO2)",
            markers=True,
            title=t("emissions_trend")
        )
        fig5.update_traces(line=dict(width=3))
        fig5.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.8)")
        st.plotly_chart(fig5, use_container_width=True)

    st.markdown(f'<p class="mini-note">{t("note_illustrative")}</p>', unsafe_allow_html=True)

# =========================================================
# PAGE 2: MASTERPLAN
# =========================================================
elif page == "masterplan":
    st.markdown(
        f"""
        <div class="hero-strip">
            <h2>{t('hero_masterplan_title')}</h2>
            <p>{t('hero_masterplan_desc')}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    s1, s2, s3, s4 = st.columns(4)
    s1.metric(t("nze_target"), "2050")
    s2.metric(t("key_driver"), "Solar PV")
    s3.metric(t("emerging_role"), "Wind + Storage")
    s4.metric(t("strategic_need"), "Grid + Storage")

    st.markdown(f"### {t('transition_pathway')}")
    a1, a2 = st.columns(2)

    with a1:
        fig6 = px.line(
            pathway_share_data,
            x="Year",
            y="Renewable Share (%)",
            markers=True,
            title=t("re_share_pathway")
        )
        fig6.update_traces(line=dict(width=3))
        fig6.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.8)")
        st.plotly_chart(fig6, use_container_width=True)

    with a2:
        fig7 = px.line(
            pathway_emission_data,
            x="Year",
            y="CO2 Emissions (MtCO2)",
            markers=True,
            title=t("co2_pathway")
        )
        fig7.update_traces(line=dict(width=3))
        fig7.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.8)")
        st.plotly_chart(fig7, use_container_width=True)

    b1, b2 = st.columns(2)

    with b1:
        fig8 = px.line(
            pathway_demand_data,
            x="Year",
            y="Electricity Demand (GWh)",
            markers=True,
            title=t("demand_projection")
        )
        fig8.update_traces(line=dict(width=3))
        fig8.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.8)")
        st.plotly_chart(fig8, use_container_width=True)

    with b2:
        capacity_long = capacity_pathway_data.melt(id_vars="Year", var_name="Technology", value_name="Capacity")
        fig9 = px.area(
            capacity_long,
            x="Year",
            y="Capacity",
            color="Technology",
            color_discrete_map=color_map,
            title=t("capacity_pathway")
        )
        fig9.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.8)")
        st.plotly_chart(fig9, use_container_width=True)

    st.markdown(f"### {t('storage_pathway')}")
    storage_long = storage_pathway_data.melt(id_vars="Year", var_name="System", value_name="Storage (MWh)")
    fig10 = px.bar(
        storage_long,
        x="Year",
        y="Storage (MWh)",
        color="System",
        barmode="group",
        title=t("storage_pathway")
    )
    fig10.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.8)")
    st.plotly_chart(fig10, use_container_width=True)

    st.markdown(f"### {t('key_messages')}")
    st.markdown(
        f"""
        <div class="soft-card">
            <ul>
                <li>{t('msg1')}</li>
                <li>{t('msg2')}</li>
                <li>{t('msg3')}</li>
                <li>{t('msg4')}</li>
                <li>{t('msg5')}</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f'<p class="mini-note">{t("note_pathway")}</p>', unsafe_allow_html=True)

# =========================================================
# PAGE 3: DATA & INVESTMENT HUB
# =========================================================
elif page == "datacenter":
    st.markdown(
        f"""
        <div class="hero-strip">
            <h2>{t('hero_datacenter_title')}</h2>
            <p>{t('hero_datacenter_desc')}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    left_col, right_col = st.columns([1.05, 1.95])

    with left_col:
        st.markdown(f"### {t('resource_potential')}")
        resource_display = resource_potential_data.copy()
        resource_display.columns = [t("resource"), t("summary")]
        st.dataframe(resource_display, use_container_width=True, hide_index=True)

        st.markdown(f"### {t('investment_opportunities')}")
        invest_display = investment_data.copy()
        invest_display.columns = [t("opportunity"), t("focus_area"), t("stage")]
        st.dataframe(invest_display, use_container_width=True, hide_index=True)

        st.markdown("### Investment Insights")
        st.dataframe(investment_insight_data, use_container_width=True, hide_index=True)

        st.markdown(f"### {t('download_center')}")
        download_display = download_items.copy()
        download_display.columns = [t("dataset"), t("status")]
        st.dataframe(download_display, use_container_width=True, hide_index=True)

        st.download_button(
            label=t("download_project_list"),
            data=project_data.drop(columns=["lat", "lon"]).to_csv(index=False),
            file_name="ntb_project_pipeline.csv",
            mime="text/csv"
        )

        st.download_button(
            label=t("download_pathway_data"),
            data=capacity_pathway_data.to_csv(index=False),
            file_name="ntb_nze_capacity_pathway.csv",
            mime="text/csv"
        )

    with right_col:
        st.markdown(f"### {t('project_map')}")

        tech_filter = st.multiselect(
            t("filter_tech"),
            options=sorted(project_data["Technology"].unique()),
            default=sorted(project_data["Technology"].unique())
        )

        filtered_projects = project_data[project_data["Technology"].isin(tech_filter)].copy()

        m = folium.Map(location=[-8.65, 117.4], zoom_start=8, tiles="CartoDB positron")

        for _, row in filtered_projects.iterrows():
            popup_html = f"""
            <b>{row['Project']}</b><br>
            {t('popup_technology')}: {row['Technology']}<br>
            {t('popup_capacity')}: {row['Capacity (MW)']} MW<br>
            {t('popup_status')}: {row['Status']}<br>
            {t('popup_developer')}: {row['Developer']}<br>
            {t('popup_location')}: {row['Location']}
            """

            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=9,
                popup=folium.Popup(popup_html, max_width=320),
                tooltip=row["Project"],
                color=get_folium_color(row["Technology"]),
                fill=True,
                fill_color=get_folium_color(row["Technology"]),
                fill_opacity=0.85
            ).add_to(m)

        st_folium(m, width=None, height=540)

        st.markdown(
            f"""
            <div class="soft-card">
                <h4>Note</h4>
                <p>{t('note_datacenter')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# FOOTER
# =========================================================
st.markdown(
    f"""
    <div class="footer">
        <hr style="border-color: rgba(255,255,255,0.3);">
        <p>
        <b>NTB Renewable Energy Tracker</b><br>
        {t('footer_developed')} <b>Muhammad Zurhalki</b> | {t('footer_anu')}<br>
        {t('footer_based')}<br>
        <span style="font-size:0.8rem;">{t('footer_illus')}</span>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
