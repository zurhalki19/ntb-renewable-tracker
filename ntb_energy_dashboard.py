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
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'  # default: English

translations = {
    'en': {
        'page_title': 'NTB Renewable Energy Tracker',
        'page_subtitle': 'A public dashboard tracking renewable energy progress in West Nusa Tenggara.',
        'nav_situasi': 'Current Situation',
        'nav_masterplan': 'Energy Transition Masterplan',
        'nav_datacenter': 'Data Center & Investment Opportunities',
        'hero_situasi_title': 'NTB Current Energy Situation',
        'hero_situasi_desc': 'Summary of the energy system, generation mix, demand, emissions, and renewable energy progress.',
        'hero_masterplan_title': 'NTB Energy Transition Masterplan',
        'hero_masterplan_desc': 'This page summarizes NTB’s energy transition pathway towards a cleaner, low-carbon system by 2050.',
        'hero_datacenter_title': 'Data Center & Investment Opportunities',
        'hero_datacenter_desc': 'Documents, sample data, project map, and summary of renewable energy investment opportunities in NTB.',
        'metric_re_share': 'Renewable Share',
        'metric_re_capacity': 'Installed RE Capacity',
        'metric_demand': 'Electricity Demand',
        'metric_emissions': 'CO₂ Emissions',
        'snapshot_dashboard': 'Snapshot Dashboard',
        'tab_re_capacity': 'Renewable Capacity',
        'tab_re_trend': 'Renewable Share Trend',
        'tab_generation_mix': 'Generation Mix',
        'tab_demand_emissions': 'Demand and Emissions',
        'latest_updates': 'Latest Updates',
        'read_more': 'Read more →',
        'demand_trend': 'Electricity Demand Trend',
        'emissions_trend': 'CO₂ Emissions Trend',
        'note_illustrative': 'Note: The figures shown are still illustrative and should later be replaced with updated official values.',
        'nze_target': 'NZE Target',
        'key_driver': 'Key Driver',
        'emerging_role': 'Emerging Role',
        'strategic_need': 'Strategic Need',
        'transition_pathway': 'Transition Pathway',
        're_share_pathway': 'Renewable Share Pathway',
        'co2_pathway': 'CO₂ Emissions Pathway',
        'demand_projection': 'Electricity Demand Projection',
        'capacity_pathway': 'Capacity Expansion Pathway',
        'key_messages': 'Key Messages from the Masterplan',
        'msg1': 'Electricity demand in NTB is expected to grow significantly over time.',
        'msg2': 'Solar PV is likely to become the backbone of the renewable electricity system.',
        'msg3': 'Wind, especially in selected areas such as Sumbawa, may support system diversification.',
        'msg4': 'Battery storage becomes more important as variable renewable energy increases.',
        'msg5': 'The long-term pathway aims for strong emissions reduction toward net-zero by 2050.',
        'note_pathway': 'Note: The pathway values shown here are still illustrative, but the structure follows the logic of the NTB Energy Masterplan.',
        'resource_potential': 'Resource Potential',
        'investment_opportunities': 'Investment Opportunities',
        'download_center': 'Download Center',
        'download_project_list': 'Download sample project list (CSV)',
        'download_pathway_data': 'Download sample pathway data (CSV)',
        'project_map': 'Project Map',
        'filter_tech': 'Filter by technology',
        'note_datacenter': 'This page can later include official project coordinates, downloadable reports, GIS layers, and more detailed investment pipeline information.',
        'footer_developed': 'Developed by',
        'footer_anu': 'Australian National University',
        'footer_based': 'Based on NTB Energy Masterplan (2023)',
        'footer_illus': 'Current values are still illustrative and for prototype purposes.',
        'resource': 'Resource',
        'summary': 'Summary',
        'opportunity': 'Opportunity',
        'focus_area': 'Potential Focus Area',
        'stage': 'Stage',
        'dataset': 'Dataset / Document',
        'status': 'Status',
        # News items (English)
        'news1_title': 'Renewable energy visibility matters for NTB',
        'news1_text': 'This dashboard aims to improve transparency for the public, researchers, and investors.',
        'news2_title': 'Solar and wind are central in the transition pathway',
        'news2_text': 'The masterplan highlights solar PV, wind, and storage as key drivers of future decarbonisation.',
        'news3_title': 'Electricity demand is expected to continue growing',
        'news3_text': 'Rising demand means NTB needs more generation capacity and stronger transition planning.',
    },
    'id': {
        'page_title': 'NTB Renewable Energy Tracker',
        'page_subtitle': 'Dasbor publik untuk memantau perkembangan energi terbarukan di Nusa Tenggara Barat.',
        'nav_situasi': 'Situasi dan Angka Terupdate',
        'nav_masterplan': 'Masterplan Transisi Energi NTB',
        'nav_datacenter': 'Pusat Data & Peluang Investasi',
        'hero_situasi_title': 'Situasi Energi NTB Saat Ini',
        'hero_situasi_desc': 'Ringkasan kondisi sistem energi, bauran listrik, demand, emisi, dan perkembangan energi terbarukan.',
        'hero_masterplan_title': 'Masterplan Transisi Energi NTB',
        'hero_masterplan_desc': 'Halaman ini merangkum arah transisi energi NTB menuju sistem energi yang lebih bersih dan rendah emisi hingga 2050.',
        'hero_datacenter_title': 'Pusat Data & Peluang Investasi',
        'hero_datacenter_desc': 'Dokumen, data contoh, peta proyek, dan ringkasan peluang investasi energi terbarukan di NTB.',
        'metric_re_share': 'Bauran Terbarukan',
        'metric_re_capacity': 'Kapasitas Terpasang EBT',
        'metric_demand': 'Kebutuhan Listrik',
        'metric_emissions': 'Emisi CO₂',
        'snapshot_dashboard': 'Dasbor Kilat',
        'tab_re_capacity': 'Kapasitas EBT',
        'tab_re_trend': 'Tren Bauran EBT',
        'tab_generation_mix': 'Bauran Pembangkit',
        'tab_demand_emissions': 'Kebutuhan dan Emisi',
        'latest_updates': 'Update Terbaru',
        'read_more': 'Baca selengkapnya →',
        'demand_trend': 'Tren Kebutuhan Listrik',
        'emissions_trend': 'Tren Emisi CO₂',
        'note_illustrative': 'Catatan: Angka yang ditampilkan masih bersifat ilustratif dan nantinya akan diganti dengan nilai resmi terkini.',
        'nze_target': 'Target NZE',
        'key_driver': 'Penggerak Utama',
        'emerging_role': 'Peran yang Muncul',
        'strategic_need': 'Kebutuhan Strategis',
        'transition_pathway': 'Jalur Transisi',
        're_share_pathway': 'Proyeksi Bauran EBT',
        'co2_pathway': 'Proyeksi Emisi CO₂',
        'demand_projection': 'Proyeksi Kebutuhan Listrik',
        'capacity_pathway': 'Proyeksi Kapasitas',
        'key_messages': 'Pesan Utama dari Masterplan',
        'msg1': 'Kebutuhan listrik di NTB diperkirakan akan tumbuh signifikan dari waktu ke waktu.',
        'msg2': 'PLTS diperkirakan menjadi tulang punggung sistem kelistrikan terbarukan.',
        'msg3': 'Angin, terutama di daerah tertentu seperti Sumbawa, dapat mendukung diversifikasi sistem.',
        'msg4': 'Penyimpanan baterai menjadi semakin penting seiring peningkatan EBT variabel.',
        'msg5': 'Jalur transisi jangka panjang menargetkan pengurangan emisi menuju net-zero pada 2050.',
        'note_pathway': 'Catatan: Nilai jalur transisi yang ditampilkan masih ilustratif, namun strukturnya mengikuti logika Masterplan Energi NTB.',
        'resource_potential': 'Potensi Sumber Daya',
        'investment_opportunities': 'Peluang Investasi',
        'download_center': 'Pusat Unduhan',
        'download_project_list': 'Unduh contoh daftar proyek (CSV)',
        'download_pathway_data': 'Unduh contoh data jalur transisi (CSV)',
        'project_map': 'Peta Proyek',
        'filter_tech': 'Filter berdasarkan teknologi',
        'note_datacenter': 'Halaman ini nantinya dapat memuat koordinat proyek resmi, laporan yang dapat diunduh, lapisan GIS, dan informasi pipeline investasi yang lebih rinci.',
        'footer_developed': 'Dikembangkan oleh',
        'footer_anu': 'Australian National University',
        'footer_based': 'Berdasarkan Masterplan Energi NTB (2023)',
        'footer_illus': 'Nilai saat ini masih bersifat ilustratif untuk keperluan purwarupa.',
        'resource': 'Sumber Daya',
        'summary': 'Ringkasan',
        'opportunity': 'Peluang',
        'focus_area': 'Area Fokus Potensial',
        'stage': 'Tahap',
        'dataset': 'Dataset / Dokumen',
        'status': 'Status',
        # News items (Indonesian)
        'news1_title': 'Visibilitas energi terbarukan penting bagi NTB',
        'news1_text': 'Dasbor ini bertujuan meningkatkan transparansi bagi publik, peneliti, dan investor.',
        'news2_title': 'PLTS dan angin menjadi kunci dalam jalur transisi',
        'news2_text': 'Masterplan menyoroti PLTS, angin, dan penyimpanan sebagai penggerak utama dekarbonisasi masa depan.',
        'news3_title': 'Kebutuhan listrik diperkirakan terus meningkat',
        'news3_text': 'Peningkatan kebutuhan berarti NTB memerlukan kapasitas pembangkit lebih dan perencanaan transisi yang lebih kuat.',
    }
}

def t(key):
    """Return translation for the current language."""
    return translations[st.session_state.lang].get(key, key)

# =========================================================
# BACKGROUND GRADIENT (LEBIH BERWARNA)
# =========================================================
bg_gradient = """
background: linear-gradient(145deg, #d4e9ff 0%, #b8f0e6 40%, #f2f9e9 100%);
"""

def get_base64_image(image_path: str):
    path = Path(image_path)
    if path.exists():
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

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
# CUSTOM CSS DENGAN WARNA LEBIH CERAH
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
    div[data-baseweb="radio"] label[data-selected="true"] {{
        background: linear-gradient(135deg, #0f4c75, #3282b8);
        color: white !important;
        box-shadow: 0 4px 10px rgba(15,76,117,0.3);
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
        background: rgba(255,255,255,0.5);
        padding: 6px 12px;
        border-radius: 30px;
        display: inline-block;
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

    .dataframe {{
        background: rgba(255,255,255,0.8);
        backdrop-filter: blur(2px);
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.7);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# DATA (ILLUSTRATIVE / PLACEHOLDER)
# =========================================================
current_mix_data = pd.DataFrame({
    "Source": ["Diesel", "Coal", "Solar PV", "Hydropower", "Biomass"],
    "Share": [50, 25, 15, 8, 2]
})

current_re_capacity_data = pd.DataFrame({
    "Technology": ["Solar PV", "Wind", "Hydropower", "Biomass", "Biogas", "Battery Storage"],
    "Capacity (MW)": [90, 25, 40, 10, 5, 15]
})

current_demand_data = pd.DataFrame({
    "Year": [2019, 2020, 2021, 2022, 2023, 2024],
    "Electricity Demand (GWh)": [1650, 1800, 1950, 2080, 2180, 2300]
})

current_emission_data = pd.DataFrame({
    "Year": [2019, 2020, 2021, 2022, 2023, 2024],
    "CO2 Emissions (MtCO2)": [1.95, 1.90, 1.88, 1.84, 1.80, 1.76]
})

current_re_share_data = pd.DataFrame({
    "Year": [2019, 2020, 2021, 2022, 2023, 2024],
    "Renewable Share (%)": [15, 17, 18, 20, 22, 23]
})

pathway_share_data = pd.DataFrame({
    "Year": [2020, 2025, 2030, 2040, 2050],
    "Renewable Share (%)": [15, 23, 35, 65, 95]
})

pathway_demand_data = pd.DataFrame({
    "Year": [2020, 2025, 2030, 2040, 2050],
    "Electricity Demand (GWh)": [1800, 2200, 2800, 4200, 6000]
})

pathway_emission_data = pd.DataFrame({
    "Year": [2020, 2025, 2030, 2040, 2050],
    "CO2 Emissions (MtCO2)": [1.80, 1.70, 1.30, 0.60, 0.10]
})

capacity_pathway_data = pd.DataFrame({
    "Year": [2020, 2025, 2030, 2040, 2050],
    "Solar PV": [20, 90, 180, 420, 700],
    "Wind": [0, 25, 60, 130, 220],
    "Hydropower": [25, 40, 45, 50, 55],
    "Biomass": [5, 10, 18, 25, 30],
    "Biogas": [2, 5, 8, 12, 15],
    "Battery Storage": [0, 15, 50, 120, 220]
})

resource_potential_data = pd.DataFrame({
    "Resource": ["Solar PV", "Wind", "Hydropower", "Biomass / Bioenergy", "Battery Storage"],
    "Summary": [
        "High solar irradiation across NTB makes solar PV the most strategic resource.",
        "Wind potential is promising in selected areas, especially Sumbawa.",
        "Small and micro hydro remain relevant for local and distributed systems.",
        "Agricultural and organic residues may support bioenergy development.",
        "Storage becomes critical as solar and wind penetration increases."
    ]
})

investment_data = pd.DataFrame({
    "Opportunity": ["Utility-scale Solar", "Wind Development", "Small/Micro Hydro", "Battery Storage", "Data & GIS Support"],
    "Potential Focus Area": ["Lombok and Sumbawa", "Sumbawa", "Distributed areas", "System flexibility", "Planning and monitoring"],
    "Stage": ["Priority", "Emerging", "Selective", "Critical support", "Supporting function"]
})

download_items = pd.DataFrame({
    "Dataset / Document": [
        "NTB Energy Masterplan summary",
        "Technology dataset sample",
        "Project list sample",
        "Pathway data sample"
    ],
    "Status": ["Draft", "Available", "Available", "Available"]
})

project_data = pd.DataFrame({
    "Project": [
        "PLTS Sengkol",
        "Wind Pilot Sumbawa",
        "PLTMH Sumbawa",
        "Biomass Pilot Bima",
        "Biogas Lombok Tengah"
    ],
    "Technology": [
        "Solar PV",
        "Wind",
        "Hydropower",
        "Biomass",
        "Biogas"
    ],
    "Capacity (MW)": [5, 10, 2, 1.5, 0.8],
    "Status": ["Operational", "Planned", "Operational", "Planned", "Pilot"],
    "Location": ["Lombok", "Sumbawa", "Sumbawa", "Bima", "Lombok Tengah"],
    "lat": [-8.89, -8.54, -8.65, -8.45, -8.75],
    "lon": [116.29, 117.45, 117.40, 118.73, 116.30]
})

# News items in both languages
news_items = {
    'en': [
        {
            "title": t('news1_title'),
            "text": t('news1_text'),
            "link": "https://example.com/update1"
        },
        {
            "title": t('news2_title'),
            "text": t('news2_text'),
            "link": "https://example.com/update2"
        },
        {
            "title": t('news3_title'),
            "text": t('news3_text'),
            "link": "https://example.com/update3"
        }
    ],
    'id': [
        {
            "title": t('news1_title'),
            "text": t('news1_text'),
            "link": "https://example.com/update1"
        },
        {
            "title": t('news2_title'),
            "text": t('news2_text'),
            "link": "https://example.com/update2"
        },
        {
            "title": t('news3_title'),
            "text": t('news3_text'),
            "link": "https://example.com/update3"
        }
    ]
}

color_map = {
    "Solar PV": "#f3c742",
    "Wind": "#8b5cf6",
    "Hydropower": "#3b82f6",
    "Biomass": "#7cb342",
    "Biogas": "#14b8a6",
    "Battery Storage": "#f97316",
    "Diesel": "#2c7fb8",
    "Coal": "#5c6f82"
}

def get_folium_color(tech):
    if tech == "Solar PV":
        return "orange"
    elif tech == "Wind":
        return "purple"
    elif tech == "Hydropower":
        return "blue"
    elif tech == "Biomass":
        return "green"
    elif tech == "Biogas":
        return "darkgreen"
    return "gray"

# =========================================================
# HEADER with language selector
# =========================================================
col_title, col_lang = st.columns([4,1])
with col_title:
    st.markdown(f'<div class="top-title">{t("page_title")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="top-subtitle">{t("page_subtitle")}</div>', unsafe_allow_html=True)
with col_lang:
    lang_choice = st.selectbox('Language', ['English', 'Bahasa Indonesia'], label_visibility='collapsed', key='lang_selector')
    if lang_choice == 'English':
        st.session_state.lang = 'en'
    else:
        st.session_state.lang = 'id'

# Navigation (using translated options)
page = st.radio(
    "Main navigation",
    [t('nav_situasi'), t('nav_masterplan'), t('nav_datacenter')],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("---")

# =========================================================
# PAGE 1
# =========================================================
if page == t('nav_situasi'):
    st.markdown(
        f"""
        <div class="hero-strip">
            <h2>{t('hero_situasi_title')}</h2>
            <p>{t('hero_situasi_desc')}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    k1, k2, k3, k4 = st.columns(4)
    k1.metric(t('metric_re_share'), "23%")
    k2.metric(t('metric_re_capacity'), "145 MW")
    k3.metric(t('metric_demand'), "2,300 GWh")
    k4.metric(t('metric_emissions'), "1.76 MtCO₂")

    st.markdown(f"### {t('snapshot_dashboard')}")
    left, right = st.columns([2.1, 1])

    with left:
        t1, t2, t3 = st.tabs([
            t('tab_re_capacity'),
            t('tab_re_trend'),
            t('tab_generation_mix')
        ])

        with t1:
            fig1 = px.bar(
                current_re_capacity_data,
                x="Technology",
                y="Capacity (MW)",
                color="Technology",
                color_discrete_map=color_map,
                title=t('tab_re_capacity')
            )
            fig1.update_layout(
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(255,255,255,0.8)"
            )
            st.plotly_chart(fig1, use_container_width=True)

        with t2:
            fig2 = px.line(
                current_re_share_data,
                x="Year",
                y="Renewable Share (%)",
                markers=True,
                title=t('tab_re_trend')
            )
            fig2.update_traces(line=dict(width=3))
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(255,255,255,0.8)"
            )
            st.plotly_chart(fig2, use_container_width=True)

        with t3:
            fig3 = px.pie(
                current_mix_data,
                names="Source",
                values="Share",
                title=t('tab_generation_mix'),
                color="Source",
                color_discrete_map=color_map
            )
            fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig3, use_container_width=True)

    with right:
        st.markdown(f"### {t('latest_updates')}")
        for item in news_items[st.session_state.lang]:
            st.markdown(
                f"""
                <div class="news-card">
                    <h4 style="margin-bottom:6px;">{item['title']}</h4>
                    <p style="margin-bottom:8px;">{item['text']}</p>
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
            title=t('demand_trend')
        )
        fig4.update_traces(line=dict(width=3))
        fig4.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.8)"
        )
        st.plotly_chart(fig4, use_container_width=True)

    with c2:
        fig5 = px.line(
            current_emission_data,
            x="Year",
            y="CO2 Emissions (MtCO2)",
            markers=True,
            title=t('emissions_trend')
        )
        fig5.update_traces(line=dict(width=3))
        fig5.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.8)"
        )
        st.plotly_chart(fig5, use_container_width=True)

    st.markdown(
        f'<p class="mini-note">{t("note_illustrative")}</p>',
        unsafe_allow_html=True
    )

# =========================================================
# PAGE 2
# =========================================================
elif page == t('nav_masterplan'):
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
    s1.metric(t('nze_target'), "2050")
    s2.metric(t('key_driver'), "Solar PV")
    s3.metric(t('emerging_role'), "Wind + Storage")
    s4.metric(t('strategic_need'), t('demand_projection'))

    st.markdown(f"### {t('transition_pathway')}")
    a1, a2 = st.columns(2)

    with a1:
        fig6 = px.line(
            pathway_share_data,
            x="Year",
            y="Renewable Share (%)",
            markers=True,
            title=t('re_share_pathway')
        )
        fig6.update_traces(line=dict(width=3))
        fig6.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.8)"
        )
        st.plotly_chart(fig6, use_container_width=True)

    with a2:
        fig7 = px.line(
            pathway_emission_data,
            x="Year",
            y="CO2 Emissions (MtCO2)",
            markers=True,
            title=t('co2_pathway')
        )
        fig7.update_traces(line=dict(width=3))
        fig7.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.8)"
        )
        st.plotly_chart(fig7, use_container_width=True)

    b1, b2 = st.columns(2)

    with b1:
        fig8 = px.line(
            pathway_demand_data,
            x="Year",
            y="Electricity Demand (GWh)",
            markers=True,
            title=t('demand_projection')
        )
        fig8.update_traces(line=dict(width=3))
        fig8.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.8)"
        )
        st.plotly_chart(fig8, use_container_width=True)

    with b2:
        capacity_long = capacity_pathway_data.melt(
            id_vars="Year",
            var_name="Technology",
            value_name="Capacity"
        )

        fig9 = px.area(
            capacity_long,
            x="Year",
            y="Capacity",
            color="Technology",
            color_discrete_map=color_map,
            title=t('capacity_pathway')
        )
        fig9.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.8)"
        )
        st.plotly_chart(fig9, use_container_width=True)

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

    st.markdown(
        f'<p class="mini-note">{t("note_pathway")}</p>',
        unsafe_allow_html=True
    )

# =========================================================
# PAGE 3
# =========================================================
elif page == t('nav_datacenter'):
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
        # Translate dataframe column headers
        resource_display = resource_potential_data.copy()
        resource_display.columns = [t('resource'), t('summary')]
        st.dataframe(resource_display, use_container_width=True, hide_index=True)

        st.markdown(f"### {t('investment_opportunities')}")
        invest_display = investment_data.copy()
        invest_display.columns = [t('opportunity'), t('focus_area'), t('stage')]
        st.dataframe(invest_display, use_container_width=True, hide_index=True)

        st.markdown(f"### {t('download_center')}")
        download_display = download_items.copy()
        download_display.columns = [t('dataset'), t('status')]
        st.dataframe(download_display, use_container_width=True, hide_index=True)

        st.download_button(
            label=t('download_project_list'),
            data=project_data.drop(columns=["lat", "lon"]).to_csv(index=False),
            file_name="ntb_projects_sample.csv",
            mime="text/csv"
        )

        st.download_button(
            label=t('download_pathway_data'),
            data=capacity_pathway_data.to_csv(index=False),
            file_name="ntb_pathway_sample.csv",
            mime="text/csv"
        )

    with right_col:
        st.markdown(f"### {t('project_map')}")

        tech_filter = st.multiselect(
            t('filter_tech'),
            options=project_data["Technology"].unique(),
            default=list(project_data["Technology"].unique())
        )

        filtered_projects = project_data[project_data["Technology"].isin(tech_filter)].copy()

        m = folium.Map(
            location=[-8.65, 117.4],
            zoom_start=8,
            tiles="CartoDB positron"
        )

        for _, row in filtered_projects.iterrows():
            popup_html = f"""
            <b>{row['Project']}</b><br>
            Technology: {row['Technology']}<br>
            Capacity: {row['Capacity (MW)']} MW<br>
            Status: {row['Status']}<br>
            Location: {row['Location']}
            """

            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=9,
                popup=folium.Popup(popup_html, max_width=300),
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
                <p>
                {t('note_datacenter')}
                </p>
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