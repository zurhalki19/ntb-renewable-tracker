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
# SESSION STATE
# =========================================================
if "lang" not in st.session_state:
    st.session_state.lang = "en"

if "page" not in st.session_state:
    st.session_state.page = "landing"

# =========================================================
# MULTILINGUAL SETUP
# =========================================================
translations = {
    "en": {
        "page_title": "NTB Renewable Energy Tracker",
        "page_subtitle": "A public dashboard tracking renewable energy progress in West Nusa Tenggara.",
        "nav_landing": "Home",
        "nav_situasi": "Current Situation",
        "nav_masterplan": "Energy Transition Masterplan",
        "nav_datacenter": "Data & Investment Hub",

        "landing_kicker": "PUBLIC ENERGY TRANSITION DASHBOARD",
        "landing_title": "Tracking NTB’s renewable energy transition toward net-zero by 2050.",
        "landing_desc": "This dashboard brings together energy system data, net-zero pathway insights, project pipeline information, and investment opportunities for West Nusa Tenggara.",
        "landing_note": "Built as a public-facing prototype for transparency, research, policy discussion, and investment visibility.",
        "landing_cta": "Explore the dashboard",

        "landing_card1_title": "Current Situation",
        "landing_card1_desc": "Understand NTB’s current electricity mix, renewable share, electricity demand, and fossil fuel dependence.",
        "landing_card1_tag": "Energy baseline",

        "landing_card2_title": "NZE Pathway",
        "landing_card2_desc": "Explore the transition pathway toward 2050, including solar, wind, emissions reduction, and storage needs.",
        "landing_card2_tag": "Transition roadmap",

        "landing_card3_title": "Investment Hub",
        "landing_card3_desc": "View resource potential, project pipeline, map-based opportunities, and priority investment areas.",
        "landing_card3_tag": "Investor visibility",

        "landing_big1": "~75%",
        "landing_big1_label": "fossil-based electricity generation",
        "landing_big2": "~13 GW",
        "landing_big2_label": "solar and wind capacity by 2050",
        "landing_big3": "2050",
        "landing_big3_label": "net-zero transition horizon",

        "hero_situasi_title": "NTB Current Energy Situation",
        "hero_situasi_desc": "NTB is still fossil-heavy, while electricity demand continues to grow.",
        "hero_masterplan_title": "NTB Energy Transition Pathway to 2050",
        "hero_masterplan_desc": "The pathway shows a major scale-up of solar, wind, storage, and grid readiness toward net-zero.",
        "hero_datacenter_title": "Data & Investment Opportunities",
        "hero_datacenter_desc": "Resource potential, project pipeline, and investment focus areas for renewable energy in NTB.",

        "metric_re_share": "Renewable Share",
        "metric_re_capacity": "Installed RE Capacity",
        "metric_demand": "Electricity Demand",
        "metric_emissions": "CO₂ Emissions",

        "snapshot_dashboard": "Snapshot Dashboard",
        "generation_mix": "Generation Mix",
        "demand_trend": "Electricity Demand Trend",
        "latest_updates": "Latest Updates",
        "read_more": "Read more →",

        "note_illustrative": "Note: Values are based on extracted NTB Energy Masterplan / Net Zero 2050 pathway data. Some values, especially project coordinates and intermediate years, are indicative.",
        "nze_target": "NZE Target",
        "key_driver": "Key Driver",
        "emerging_role": "Emerging Role",
        "strategic_need": "Strategic Need",

        "capacity_pathway": "Capacity Expansion Pathway",
        "co2_pathway": "CO₂ Emissions Pathway",
        "demand_projection": "Electricity Demand Projection",
        "key_messages": "Key Messages from the Masterplan",

        "msg1": "Electricity demand is projected to reach about 21.8 TWh in the NZE scenario by 2050.",
        "msg2": "Solar PV becomes the backbone of the future electricity system due to high potential and low-cost generation.",
        "msg3": "Wind development, especially in Sumbawa, supports diversification of renewable generation.",
        "msg4": "Battery storage and interconnection become critical as solar and wind penetration increases.",
        "msg5": "The NZE pathway requires fossil power phase-out and wider electrification across end-use sectors.",

        "storage_text": "Battery storage becomes critical after 2030. The NZE pathway indicates storage needs may reach around 6 GWh in Lombok and 12 GWh in Sumbawa by 2050.",
        "note_pathway": "Note: Pathway values are scenario-based. Renewable share and emissions values should be read as indicative because the source data separates Lombok, Sumbawa, power, and end-use sectors.",

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

        "big_fossil": "~75% Fossil-Based Power",
        "big_fossil_sub": "NTB electricity generation is still dominated by fossil fuels, mainly liquid fuels and coal.",
        "big_capacity": "~13 GW Solar + Wind by 2050",
        "big_capacity_sub": "The NZE pathway relies on a massive scale-up of solar PV and wind capacity.",
        "big_invest": "Sumbawa is the Renewable Growth Hub",
        "big_invest_sub": "Solar and wind potential make Sumbawa central to NTB’s long-term energy transition.",

        "insight_current": "NTB’s power system is still heavily dependent on fossil fuels, while electricity demand is expected to grow significantly. This creates both a transition challenge and a major investment opportunity.",
        "insight_masterplan": "The pathway is mainly about scaling solar and wind very fast, while cutting emissions toward net-zero by 2050.",
        "insight_investment": "Investment should focus on solar PV, wind, storage, and grid readiness, especially in Sumbawa and the Lombok-Sumbawa system.",

        "demand_callout": "Electricity demand could increase almost 10x by 2050 under the NZE pathway.",
        "capacity_callout": "Solar PV becomes the dominant technology after 2030, supported by wind and storage.",
        "emission_callout": "The NZE pathway reduces emissions sharply after 2030 and approaches net-zero by 2050.",

        "why_invest": "Why invest in NTB?",
        "why1": "High solar and wind potential, especially in Sumbawa.",
        "why2": "Electricity demand is expected to grow strongly under electrification.",
        "why3": "Storage and grid investment become critical for high renewable penetration.",
        "why4": "The market is still early-stage, so good data visibility can support better investment decisions.",

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
        "nav_landing": "Beranda",
        "nav_situasi": "Situasi Energi Saat Ini",
        "nav_masterplan": "Masterplan Transisi Energi NTB",
        "nav_datacenter": "Data & Investment Hub",

        "landing_kicker": "DASHBOARD PUBLIK TRANSISI ENERGI",
        "landing_title": "Memantau transisi energi terbarukan NTB menuju net-zero 2050.",
        "landing_desc": "Dashboard ini menyatukan data sistem energi, pathway net-zero, pipeline proyek, dan peluang investasi energi terbarukan di Nusa Tenggara Barat.",
        "landing_note": "Dibangun sebagai prototype publik untuk transparansi, riset, diskusi kebijakan, dan visibilitas investasi.",
        "landing_cta": "Jelajahi dashboard",

        "landing_card1_title": "Situasi Saat Ini",
        "landing_card1_desc": "Memahami bauran listrik NTB saat ini, porsi energi terbarukan, kebutuhan listrik, dan ketergantungan pada energi fosil.",
        "landing_card1_tag": "Baseline energi",

        "landing_card2_title": "Pathway NZE",
        "landing_card2_desc": "Melihat jalur transisi menuju 2050, termasuk PLTS, angin, penurunan emisi, dan kebutuhan storage.",
        "landing_card2_tag": "Roadmap transisi",

        "landing_card3_title": "Investment Hub",
        "landing_card3_desc": "Melihat potensi sumber daya, pipeline proyek, peta peluang, dan area prioritas investasi.",
        "landing_card3_tag": "Visibilitas investor",

        "landing_big1": "~75%",
        "landing_big1_label": "pembangkit listrik masih berbasis fosil",
        "landing_big2": "~13 GW",
        "landing_big2_label": "kapasitas surya dan angin pada 2050",
        "landing_big3": "2050",
        "landing_big3_label": "horizon transisi net-zero",

        "hero_situasi_title": "Situasi Energi NTB Saat Ini",
        "hero_situasi_desc": "NTB masih cukup bergantung pada energi fosil, sementara kebutuhan listrik terus meningkat.",
        "hero_masterplan_title": "Jalur Transisi Energi NTB menuju 2050",
        "hero_masterplan_desc": "Pathway menunjukkan peningkatan besar PLTS, angin, storage, dan kesiapan jaringan menuju net-zero.",
        "hero_datacenter_title": "Data dan Peluang Investasi",
        "hero_datacenter_desc": "Potensi sumber daya, pipeline proyek, dan area fokus investasi energi terbarukan di NTB.",

        "metric_re_share": "Bauran Terbarukan",
        "metric_re_capacity": "Kapasitas Terpasang EBT",
        "metric_demand": "Kebutuhan Listrik",
        "metric_emissions": "Emisi CO₂",

        "snapshot_dashboard": "Dasbor Kilat",
        "generation_mix": "Bauran Pembangkit",
        "demand_trend": "Tren Kebutuhan Listrik",
        "latest_updates": "Update Terbaru",
        "read_more": "Baca selengkapnya →",

        "note_illustrative": "Catatan: Nilai berasal dari ekstraksi Masterplan Energi NTB / Net Zero 2050 pathway. Beberapa nilai, terutama koordinat proyek dan tahun antara, masih indikatif.",
        "nze_target": "Target NZE",
        "key_driver": "Penggerak Utama",
        "emerging_role": "Peran yang Muncul",
        "strategic_need": "Kebutuhan Strategis",

        "capacity_pathway": "Proyeksi Kapasitas",
        "co2_pathway": "Proyeksi Emisi CO₂",
        "demand_projection": "Proyeksi Kebutuhan Listrik",
        "key_messages": "Pesan Utama dari Masterplan",

        "msg1": "Kebutuhan listrik diproyeksikan mencapai sekitar 21,8 TWh dalam skenario NZE pada 2050.",
        "msg2": "PLTS menjadi tulang punggung sistem kelistrikan masa depan karena potensi tinggi dan biaya yang kompetitif.",
        "msg3": "Pengembangan angin, terutama di Sumbawa, mendukung diversifikasi pembangkit terbarukan.",
        "msg4": "Penyimpanan baterai dan interkoneksi menjadi penting ketika penetrasi PLTS dan angin meningkat.",
        "msg5": "Jalur NZE membutuhkan phase-out pembangkit fosil dan elektrifikasi yang lebih luas di sektor pengguna akhir.",

        "storage_text": "Battery storage menjadi penting setelah 2030. Dalam pathway NZE, kebutuhan storage indikatif dapat mencapai sekitar 6 GWh di Lombok dan 12 GWh di Sumbawa pada 2050.",
        "note_pathway": "Catatan: Nilai pathway berbasis skenario. Nilai bauran EBT dan emisi perlu dibaca sebagai indikatif karena data sumber memisahkan Lombok, Sumbawa, sektor listrik, dan sektor pengguna akhir.",

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

        "big_fossil": "~75% Listrik Masih Berbasis Fosil",
        "big_fossil_sub": "Produksi listrik NTB masih didominasi bahan bakar fosil, terutama BBM dan batubara.",
        "big_capacity": "~13 GW Surya + Angin pada 2050",
        "big_capacity_sub": "Pathway NZE bergantung pada peningkatan besar kapasitas PLTS dan angin.",
        "big_invest": "Sumbawa adalah Pusat Pertumbuhan EBT",
        "big_invest_sub": "Potensi surya dan angin membuat Sumbawa penting dalam transisi energi jangka panjang NTB.",

        "insight_current": "Sistem kelistrikan NTB masih sangat bergantung pada energi fosil, sementara kebutuhan listrik diperkirakan meningkat signifikan. Ini menciptakan tantangan transisi sekaligus peluang investasi besar.",
        "insight_masterplan": "Pathway ini terutama tentang peningkatan cepat PLTS dan angin, sambil menurunkan emisi menuju net-zero pada 2050.",
        "insight_investment": "Investasi perlu difokuskan pada PLTS, angin, storage, dan kesiapan jaringan, terutama di Sumbawa dan sistem Lombok-Sumbawa.",

        "demand_callout": "Kebutuhan listrik dapat meningkat hampir 10 kali lipat pada 2050 dalam pathway NZE.",
        "capacity_callout": "PLTS menjadi teknologi dominan setelah 2030, didukung oleh angin dan storage.",
        "emission_callout": "Pathway NZE menurunkan emisi secara tajam setelah 2030 dan mendekati net-zero pada 2050.",

        "why_invest": "Mengapa investasi di NTB?",
        "why1": "Potensi surya dan angin tinggi, terutama di Sumbawa.",
        "why2": "Kebutuhan listrik diperkirakan tumbuh kuat karena elektrifikasi.",
        "why3": "Storage dan jaringan menjadi penting untuk penetrasi EBT tinggi.",
        "why4": "Pasar masih tahap awal, sehingga visibilitas data dapat mendukung keputusan investasi yang lebih baik.",

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
# BACKGROUND AND CSS
# =========================================================
def get_base64_image(image_path: str):
    path = Path(image_path)
    if path.exists():
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


bg_gradient = "background: linear-gradient(145deg, #d4e9ff 0%, #b8f0e6 40%, #f2f9e9 100%);"
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

st.markdown(
    f"""
    <style>
    .stApp {{ {bg_css} }}

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
        border-radius: 30px;
        padding: 8px 22px;
        color: #0a2e4b;
        font-weight: 600;
    }}

    .landing-hero {{
        background:
            radial-gradient(circle at 15% 20%, rgba(255,255,255,0.55), transparent 28%),
            linear-gradient(135deg, rgba(15,76,117,0.98), rgba(50,130,184,0.94), rgba(27,152,176,0.92));
        color: white;
        border-radius: 34px;
        padding: 52px 54px;
        margin-bottom: 26px;
        box-shadow: 0 20px 45px rgba(15,76,117,0.28);
        position: relative;
        overflow: hidden;
    }}

    .landing-hero::after {{
        content: "";
        position: absolute;
        right: -70px;
        bottom: -80px;
        width: 280px;
        height: 280px;
        border-radius: 50%;
        background: rgba(255,255,255,0.12);
    }}

    .landing-kicker {{
        display: inline-block;
        background: rgba(255,255,255,0.18);
        border: 1px solid rgba(255,255,255,0.25);
        color: white;
        border-radius: 999px;
        padding: 8px 15px;
        font-size: 0.82rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        margin-bottom: 18px;
    }}

    .landing-title {{
        color: white !important;
        font-size: 3.4rem;
        line-height: 1.04;
        font-weight: 880;
        letter-spacing: -0.055em;
        max-width: 920px;
        margin-bottom: 18px;
    }}

    .landing-desc {{
        color: rgba(255,255,255,0.93);
        font-size: 1.22rem;
        line-height: 1.65;
        max-width: 790px;
        margin-bottom: 18px;
    }}

    .landing-note {{
        color: rgba(255,255,255,0.82);
        font-size: 0.98rem;
        max-width: 760px;
        line-height: 1.55;
    }}

    .landing-stats-wrap {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 18px;
        margin-bottom: 26px;
    }}

    .landing-stat {{
        background: rgba(255,255,255,0.86);
        border: 1px solid rgba(255,255,255,0.75);
        border-radius: 26px;
        padding: 24px;
        box-shadow: 0 10px 26px rgba(25,80,120,0.12);
    }}

    .landing-stat-number {{
        color: #0f4c75;
        font-size: 2.3rem;
        font-weight: 850;
        letter-spacing: -0.04em;
        margin-bottom: 4px;
    }}

    .landing-stat-label {{
        color: #1e4a6b;
        font-size: 1rem;
        font-weight: 600;
    }}

    .landing-card {{
        background: rgba(255,255,255,0.88);
        border: 1px solid rgba(255,255,255,0.75);
        border-radius: 28px;
        padding: 28px;
        min-height: 270px;
        box-shadow: 0 12px 28px rgba(25,80,120,0.13);
        transition: transform 0.22s ease, box-shadow 0.22s ease, background 0.22s ease;
        margin-bottom: 18px;
    }}

    .landing-card:hover {{
        transform: translateY(-5px);
        background: rgba(255,255,255,0.96);
        box-shadow: 0 16px 34px rgba(25,80,120,0.18);
    }}

    .landing-card-tag {{
        display: inline-block;
        background: linear-gradient(135deg, #0f4c75, #3282b8);
        color: white;
        border-radius: 999px;
        padding: 6px 13px;
        font-size: 0.8rem;
        font-weight: 750;
        margin-bottom: 16px;
    }}

    .landing-card h3 {{
        font-size: 1.55rem;
        margin-bottom: 10px;
        color: #0a2e4b;
    }}

    .landing-card p {{
        color: #1e4a6b;
        line-height: 1.6;
        font-size: 1rem;
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

    .big-number-card {{
        background: rgba(255,255,255,0.82);
        border: 1px solid rgba(255,255,255,0.75);
        border-radius: 28px;
        padding: 24px 28px;
        margin-bottom: 22px;
        box-shadow: 0 10px 26px rgba(25,80,120,0.13);
    }}

    .big-number {{
        font-size: 3rem;
        line-height: 1.05;
        font-weight: 850;
        color: #0f4c75;
        letter-spacing: -0.04em;
    }}

    .big-sub {{
        font-size: 1.08rem;
        color: #1e4a6b;
        margin-top: 8px;
    }}

    .big-tag {{
        display: inline-block;
        background: linear-gradient(135deg, #0f4c75, #3282b8);
        color: white;
        border-radius: 999px;
        padding: 6px 13px;
        font-size: 0.82rem;
        font-weight: 700;
        margin-bottom: 12px;
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
        margin-bottom: 15px;
    }}

    .news-card {{
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255,255,255,0.7);
        border-radius: 24px;
        padding: 18px;
        margin-bottom: 15px;
        box-shadow: 0 8px 22px rgba(25,80,120,0.1);
        border-left: 6px solid #3282b8;
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

    .insight-box {{
        background: linear-gradient(135deg, #0f4c75, #3282b8);
        color: white;
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 20px;
        font-size: 1.05rem;
        box-shadow: 0 10px 24px rgba(15,76,117,0.23);
    }}

    .insight-title {{
        font-weight: 800;
        margin-bottom: 10px;
    }}

    .rotating-insights {{
        position: relative;
        min-height: 62px;
    }}

    .rotating-insights span {{
        position: absolute;
        left: 0;
        right: 0;
        top: 0;
        opacity: 0;
        animation: rotateInsight 50s infinite;
        line-height: 1.55;
        font-weight: 600;
    }}

    .rotating-insights span:nth-child(1) {{ animation-delay: 0s; }}
    .rotating-insights span:nth-child(2) {{ animation-delay: 10s; }}
    .rotating-insights span:nth-child(3) {{ animation-delay: 20s; }}
    .rotating-insights span:nth-child(4) {{ animation-delay: 30s; }}
    .rotating-insights span:nth-child(5) {{ animation-delay: 40s; }}

    @keyframes rotateInsight {{
        0% {{ opacity: 0; transform: translateY(8px); }}
        4% {{ opacity: 1; transform: translateY(0); }}
        16% {{ opacity: 1; transform: translateY(0); }}
        20% {{ opacity: 0; transform: translateY(-8px); }}
        100% {{ opacity: 0; transform: translateY(-8px); }}
    }}

    .chart-callout {{
        background: rgba(255,255,255,0.74);
        border-left: 6px solid #1b98b0;
        border-radius: 18px;
        padding: 12px 16px;
        margin: 8px 0 14px 0;
        color: #0a2e4b;
        font-weight: 650;
    }}

    .resource-list li {{
        margin-bottom: 8px;
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
    }}

    .stButton button {{
        background: linear-gradient(135deg, #0f4c75, #3282b8);
        color: white;
        border: none;
        border-radius: 40px;
        padding: 10px 28px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(15,76,117,0.3);
        width: 100%;
    }}

    .stButton button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 7px 16px rgba(15,76,117,0.32);
    }}

    @media (max-width: 900px) {{
        .landing-title {{
            font-size: 2.35rem;
        }}

        .landing-hero {{
            padding: 34px 28px;
        }}

        .landing-stats-wrap {{
            grid-template-columns: 1fr;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# DATA BASED ON NTB NET ZERO 2050 PATHWAY EXTRACTION
# =========================================================
current_mix_data = pd.DataFrame({
    "Source": ["HSD / Diesel", "MFO", "Biodiesel", "Coal", "Hydropower", "Solar PV", "Biomass / Cofiring"],
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

pathway_emission_data = pd.DataFrame({
    "Year": [2025, 2030, 2035, 2040, 2045, 2050],
    "CO2 Emissions (MtCO2)": [4.5, 3.0, 1.5, 1.0, 0.5, 0.06]
})

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

resource_summary = [
    ("Solar PV", "Very high potential, especially Sumbawa: around 9,628 MW; Lombok: around 1,000 MW."),
    ("Wind", "Strong onshore potential, especially Sumbawa: around 1,667 MW."),
    ("Hydropower", "Limited remaining potential, around 52 MW total across Lombok and Sumbawa."),
    ("Bioenergy", "Potential around 297 MW in Lombok and 19 MW in Sumbawa."),
    ("Storage", "Critical for high solar and wind integration after 2030.")
]

investment_data = pd.DataFrame({
    "Opportunity": ["Utility-scale Solar PV", "Onshore Wind Development", "Battery Storage", "Grid Interconnection", "Bioenergy Development"],
    "Potential Focus Area": ["Sumbawa and Lombok", "Sumbawa", "Lombok and Sumbawa systems", "Lombok-Sumbawa integration", "Lombok and agricultural areas"],
    "Stage": ["Priority", "Strategic", "Critical support", "Critical infrastructure", "Selective"]
})

download_items = pd.DataFrame({
    "Dataset / Document": ["NTB Energy Masterplan summary", "Generation mix 2023", "NZE capacity pathway", "Project pipeline sample"],
    "Status": ["Extracted", "Available", "Available", "Available"]
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
        "Sumbawa-Bima Biomass",
        "Sumbawa-Bima Geothermal",
        "Lombok 3 EBT Base"
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
        "Biomass",
        "Geothermal",
        "Renewable Base"
    ],
    "Capacity (MW)": [10, 1.3, 100, 2, 0.3, 8.4, 30, 2.3, 10, 10, 10, 100],
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
        "Plan"
    ],
    "Developer": ["PLN", "IPP", "PLN", "PLN", "PLN", "IPP", "PLN", "IPP", "IPP", "IPP", "PLN", "PLN"],
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
        "Sumbawa-Bima",
        "Sumbawa-Bima",
        "Lombok"
    ],
    "lat": [-8.65, -8.60, -8.70, -8.95, -8.50, -8.80, -8.55, -8.58, -8.45, -8.50, -8.45, -8.70],
    "lon": [116.30, 116.25, 116.35, 117.20, 117.10, 117.30, 117.45, 116.28, 118.20, 118.30, 118.25, 116.35]
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
    "HSD / Diesel": "#2c7fb8",
    "MFO": "#64748b",
    "Biodiesel": "#14b8a6",
    "Coal": "#475569",
    "Natural Gas": "#38bdf8",
    "Gas": "#38bdf8",
    "Renewable Base": "#22c55e"
}


def get_folium_color(tech: str) -> str:
    return {
        "Solar PV": "orange",
        "Wind": "purple",
        "Hydropower": "blue",
        "Biomass": "green",
        "Bioenergy": "green",
        "Geothermal": "red",
        "Gas": "lightblue",
        "Coal": "darkgray",
        "Renewable Base": "green"
    }.get(tech, "gray")


def rotating_insight_box(insights, title="Key Insight:"):
    insight_spans = "".join([f"<span>{item}</span>" for item in insights])
    st.markdown(
        f"""
        <div class="insight-box">
            <div class="insight-title">{title}</div>
            <div class="rotating-insights">
                {insight_spans}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def go_to_page(page_name: str):
    st.session_state.page = page_name
    st.rerun()


# =========================================================
# HEADER AND NAVIGATION
# =========================================================
col_title, _ = st.columns([4, 1])

with col_title:
    st.markdown(f'<div class="top-title">{t("page_title")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="top-subtitle">{t("page_subtitle")}</div>', unsafe_allow_html=True)

page_options = ["landing", "situasi", "masterplan", "datacenter"]

page_label = {
    "landing": t("nav_landing"),
    "situasi": t("nav_situasi"),
    "masterplan": t("nav_masterplan"),
    "datacenter": t("nav_datacenter")
}

selected_page = st.radio(
    "Main navigation",
    page_options,
    index=page_options.index(st.session_state.page),
    format_func=lambda x: page_label[x],
    horizontal=True,
    label_visibility="collapsed",
    key="main_navigation"
)

st.session_state.page = selected_page
page = st.session_state.page

st.markdown("---")

# =========================================================
# PAGE 0: LANDING PAGE
# =========================================================
if page == "landing":
    st.markdown(
        f"""
        <div class="landing-hero">
            <div class="landing-kicker">{t('landing_kicker')}</div>
            <div class="landing-title">{t('landing_title')}</div>
            <div class="landing-desc">{t('landing_desc')}</div>
            <div class="landing-note">{t('landing_note')}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="landing-stats-wrap">
            <div class="landing-stat">
                <div class="landing-stat-number">{t('landing_big1')}</div>
                <div class="landing-stat-label">{t('landing_big1_label')}</div>
            </div>
            <div class="landing-stat">
                <div class="landing-stat-number">{t('landing_big2')}</div>
                <div class="landing-stat-label">{t('landing_big2_label')}</div>
            </div>
            <div class="landing-stat">
                <div class="landing-stat-number">{t('landing_big3')}</div>
                <div class="landing-stat-label">{t('landing_big3_label')}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="landing-card">
                <div class="landing-card-tag">{t('landing_card1_tag')}</div>
                <h3>{t('landing_card1_title')}</h3>
                <p>{t('landing_card1_desc')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button(t("nav_situasi"), key="go_current"):
            go_to_page("situasi")

    with c2:
        st.markdown(
            f"""
            <div class="landing-card">
                <div class="landing-card-tag">{t('landing_card2_tag')}</div>
                <h3>{t('landing_card2_title')}</h3>
                <p>{t('landing_card2_desc')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button(t("nav_masterplan"), key="go_masterplan"):
            go_to_page("masterplan")

    with c3:
        st.markdown(
            f"""
            <div class="landing-card">
                <div class="landing-card-tag">{t('landing_card3_tag')}</div>
                <h3>{t('landing_card3_title')}</h3>
                <p>{t('landing_card3_desc')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button(t("nav_datacenter"), key="go_datacenter"):
            go_to_page("datacenter")

    st.markdown(
        f"""
        <div class="soft-card" style="margin-top: 14px;">
            <h3 style="margin-bottom: 8px;">{t('landing_cta')}</h3>
            <p style="color:#1e4a6b; line-height:1.6;">
                This platform is designed to connect energy data, transition planning, and investment visibility in one place.
                It is still a prototype, but it can support a more transparent discussion about NTB's renewable energy future.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# PAGE 1: CURRENT SITUATION
# =========================================================
elif page == "situasi":
    st.markdown(
        f"""
        <div class="hero-strip">
            <h2>{t('hero_situasi_title')}</h2>
            <p>{t('hero_situasi_desc')}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="big-number-card">
            <div class="big-tag">CURRENT SYSTEM</div>
            <div class="big-number">{t('big_fossil')}</div>
            <div class="big-sub">{t('big_fossil_sub')}</div>
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

    rotating_insight_box([
        t("insight_current"),
        "~75% of NTB electricity generation is still fossil-based.",
        t("demand_callout"),
        "Solar PV and wind create the main long-term investment story.",
        "Data visibility is important for public trust and investor confidence."
    ])

    left, right = st.columns([2.1, 1])

    with left:
        st.markdown(f"<div class='chart-callout'>{t('big_fossil_sub')}</div>", unsafe_allow_html=True)

        fig_mix = px.pie(
            current_mix_data,
            names="Source",
            values="Share",
            color="Source",
            color_discrete_map=color_map,
            hole=0.45
        )

        fig_mix.update_traces(
            textinfo="percent+label",
            textfont_size=13,
            pull=[0.06 if v >= 20 else 0 for v in current_mix_data["Share"]],
            hovertemplate="<b>%{label}</b><br>Share: %{value:.2f}%<extra></extra>"
        )

        fig_mix.update_layout(
            title=t("generation_mix"),
            height=560,
            margin=dict(t=55, b=90, l=20, r=20),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.18,
                xanchor="center",
                x=0.5,
                font=dict(size=12)
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        fig_mix.add_annotation(
            text="Energy<br>Mix",
            x=0.5,
            y=0.5,
            font_size=17,
            font_color="#0f4c75",
            showarrow=False
        )

        st.plotly_chart(fig_mix, use_container_width=True, config={"displayModeBar": True})

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

    st.markdown(f"### {t('demand_trend')}")
    st.markdown(f"<div class='chart-callout'>{t('demand_callout')}</div>", unsafe_allow_html=True)

    fig_demand = px.line(
        current_demand_data,
        x="Year",
        y="Electricity Demand (GWh)",
        markers=True,
        title=t("demand_trend")
    )

    fig_demand.update_traces(
        line=dict(width=4),
        marker=dict(size=9),
        hovertemplate="Year: %{x}<br>Demand: %{y:,.0f} GWh<extra></extra>"
    )

    fig_demand.update_layout(
        height=500,
        margin=dict(t=60, b=40, l=20, r=20),
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.8)"
    )

    st.plotly_chart(fig_demand, use_container_width=True, config={"displayModeBar": True})

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

    st.markdown(
        f"""
        <div class="big-number-card">
            <div class="big-tag">2050 PATHWAY</div>
            <div class="big-number">{t('big_capacity')}</div>
            <div class="big-sub">{t('big_capacity_sub')}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    s1, s2, s3, s4 = st.columns(4)
    s1.metric(t("nze_target"), "2050")
    s2.metric(t("key_driver"), "Solar PV")
    s3.metric(t("emerging_role"), "Wind + Storage")
    s4.metric(t("strategic_need"), "Grid + Storage")

    rotating_insight_box([
        t("insight_masterplan"),
        t("capacity_callout"),
        t("emission_callout"),
        "Solar PV could reach around 9.7 GW in the NZE pathway by 2050.",
        t("storage_text")
    ])

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(f"<div class='chart-callout'>{t('capacity_callout')}</div>", unsafe_allow_html=True)

        capacity_long = capacity_pathway_data.melt(
            id_vars="Year",
            var_name="Technology",
            value_name="Capacity"
        )

        fig_capacity = px.area(
            capacity_long,
            x="Year",
            y="Capacity",
            color="Technology",
            color_discrete_map=color_map,
            title=t("capacity_pathway"),
            hover_data={"Capacity": ":,.0f", "Year": True, "Technology": True}
        )

        fig_capacity.update_traces(
            mode="lines",
            line=dict(width=1.5),
            hovertemplate="<b>%{fullData.name}</b><br>Year: %{x}<br>Capacity: %{y:,.0f} MW<extra></extra>"
        )

        fig_capacity.update_layout(
            height=520,
            margin=dict(t=60, b=40, l=20, r=20),
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.28,
                xanchor="center",
                x=0.5
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.8)"
        )

        st.plotly_chart(fig_capacity, use_container_width=True, config={"displayModeBar": True})

    with c2:
        st.markdown(f"<div class='chart-callout'>{t('emission_callout')}</div>", unsafe_allow_html=True)

        fig_emission = px.line(
            pathway_emission_data,
            x="Year",
            y="CO2 Emissions (MtCO2)",
            markers=True,
            title=t("co2_pathway")
        )

        fig_emission.update_traces(
            line=dict(width=4),
            marker=dict(size=9),
            hovertemplate="Year: %{x}<br>Emissions: %{y:.2f} MtCO₂<extra></extra>"
        )

        fig_emission.update_layout(
            height=520,
            margin=dict(t=60, b=40, l=20, r=20),
            hovermode="x unified",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.8)"
        )

        st.plotly_chart(fig_emission, use_container_width=True, config={"displayModeBar": True})

    st.markdown(f"### {t('demand_projection')}")
    st.markdown(f"<div class='chart-callout'>{t('demand_callout')}</div>", unsafe_allow_html=True)

    fig_demand2 = px.line(
        current_demand_data,
        x="Year",
        y="Electricity Demand (GWh)",
        markers=True,
        title=t("demand_projection")
    )

    fig_demand2.update_traces(
        line=dict(width=4),
        marker=dict(size=9),
        hovertemplate="Year: %{x}<br>Demand: %{y:,.0f} GWh<extra></extra>"
    )

    fig_demand2.update_layout(
        height=500,
        margin=dict(t=60, b=40, l=20, r=20),
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.8)"
    )

    st.plotly_chart(fig_demand2, use_container_width=True, config={"displayModeBar": True})

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
            <p><b>Storage:</b> {t('storage_text')}</p>
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

    st.markdown(
        f"""
        <div class="big-number-card">
            <div class="big-tag">INVESTMENT FOCUS</div>
            <div class="big-number">{t('big_invest')}</div>
            <div class="big-sub">{t('big_invest_sub')}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    rotating_insight_box([
        t("insight_investment"),
        t("big_invest_sub"),
        t("why1"),
        t("why3"),
        "The project map is indicative and should be updated with official project coordinates."
    ])

    left_col, right_col = st.columns([1.05, 1.95])

    with left_col:
        st.markdown(f"### {t('why_invest')}")

        st.markdown(
            f"""
            <div class="soft-card">
                <ul>
                    <li>{t('why1')}</li>
                    <li>{t('why2')}</li>
                    <li>{t('why3')}</li>
                    <li>{t('why4')}</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(f"### {t('resource_potential')}")

        resource_html = "<div class='soft-card'><ul class='resource-list'>"
        for resource, summary in resource_summary:
            resource_html += f"<li><b>{resource}:</b> {summary}</li>"
        resource_html += "</ul></div>"

        st.markdown(resource_html, unsafe_allow_html=True)

        st.markdown(f"### {t('investment_opportunities')}")

        invest_display = investment_data.copy()
        invest_display.columns = [t("opportunity"), t("focus_area"), t("stage")]
        st.dataframe(invest_display, use_container_width=True, hide_index=True)

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

        m = folium.Map(
            location=[-8.65, 117.4],
            zoom_start=8,
            tiles="CartoDB positron"
        )

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

        st_folium(m, width=None, height=580)

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
