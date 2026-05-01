# =========================================================
# DATA (BASED ON NTB NET ZERO 2050 PATHWAY / MASTERPLAN)
# =========================================================

current_mix_data = pd.DataFrame({
    "Source": [
        "Diesel (HSD)",
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
    "Technology": [
        "Solar PV",
        "Wind",
        "Hydropower",
        "Geothermal",
        "Bioenergy"
    ],
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

pathway_share_data = pd.DataFrame({
    "Year": [2025, 2030, 2040, 2050],
    "Renewable Share (%)": [19, 69, 99, 100]
})

pathway_demand_data = pd.DataFrame({
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

storage_pathway_data = pd.DataFrame({
    "Year": [2030, 2040, 2050],
    "Lombok Storage (MWh)": [1500, 4000, 6000],
    "Sumbawa Storage (MWh)": [2000, 7000, 12000]
})

resource_potential_data = pd.DataFrame({
    "Resource": [
        "Solar PV",
        "Wind",
        "Hydropower",
        "Bioenergy",
        "Battery Storage"
    ],
    "Summary": [
        "Solar potential is very high, especially in Sumbawa with around 9,628 MW potential and around 1,000 MW in Lombok.",
        "Wind potential is significant, especially onshore wind in Sumbawa with around 1,667 MW potential.",
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

download_items = pd.DataFrame({
    "Dataset / Document": [
        "NTB Energy Masterplan summary",
        "Generation mix 2023",
        "NZE capacity pathway",
        "Resource potential data",
        "Project pipeline sample"
    ],
    "Status": [
        "Extracted",
        "Available",
        "Available",
        "Available",
        "Available"
    ]
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
    "Capacity (MW)": [
        10,
        1.3,
        100,
        2,
        0.3,
        8.4,
        30,
        2.3,
        10,
        1.75,
        10,
        10,
        100,
        100
    ],
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
    "lat": [
        -8.65, -8.60, -8.70, -8.95, -8.50, -8.80,
        -8.55, -8.58, -8.45, -8.65, -8.50, -8.45,
        -8.70, -8.70
    ],
    "lon": [
        116.30, 116.25, 116.35, 117.20, 117.10, 117.30,
        117.45, 116.28, 118.20, 116.30, 118.30, 118.25,
        116.35, 116.40
    ]
})
