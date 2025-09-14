# Cell 2 — define your sample_input dict (same content you used before) --------CURR USE
sample_input ={
  "meta": {
    "hospital": "City General, Pune",
    "tz": "Asia/Kolkata",
    "today": "2025-08-15"
  },
  "location": { "city": "Pune", "lat": 18.52, "lon": 73.86 },

  "events": [
    { "name": "Ganesh Chaturthi", "date": "2025-09-07", "type": "festival", "crowd_expected": "high" }
  ],

  "free_text_events": [
    "City marathon on 2025-08-16 6am–12pm around hospital; heat & dehydration expected; partial road closures.",
    "Diwali night (old city) 7pm–1am on 2025-08-25 ; fireworks and large processions expected."
  ],

  "weather_past_7d": [
    {"date":"2025-08-09","rain_mm":10,"humidity_pct":83,"temp_c":29,"pm25":180},
    {"date":"2025-08-10","rain_mm":12,"humidity_pct":84,"temp_c":29,"pm25":190},
    {"date":"2025-08-11","rain_mm":8,"humidity_pct":85,"temp_c":30,"pm25":195},
    {"date":"2025-08-12","rain_mm":15,"humidity_pct":86,"temp_c":29,"pm25":205},
    {"date":"2025-08-13","rain_mm":9,"humidity_pct":82,"temp_c":30,"pm25":210},
    {"date":"2025-08-14","rain_mm":12,"humidity_pct":81,"temp_c":29,"pm25":220},
    {"date":"2025-08-15","rain_mm":10,"humidity_pct":80,"temp_c":30,"pm25":225}
  ],

  "visits_daily": [
    {"date":"2025-08-09","total_opd":900},
    {"date":"2025-08-10","total_opd":920},
    {"date":"2025-08-11","total_opd":880},
    {"date":"2025-08-12","total_opd":910},
    {"date":"2025-08-13","total_opd":940},
    {"date":"2025-08-14","total_opd":960},
    {"date":"2025-08-15","total_opd":950}
  ],

  "epi_signals": {
    "by_disease_daily": [
      {"disease":"dengue","date":"2025-08-09","cases":20},
      {"disease":"dengue","date":"2025-08-10","cases":24},
      {"disease":"dengue","date":"2025-08-11","cases":27},
      {"disease":"dengue","date":"2025-08-12","cases":30},
      {"disease":"dengue","date":"2025-08-13","cases":33},
      {"disease":"dengue","date":"2025-08-14","cases":36},
      {"disease":"dengue","date":"2025-08-15","cases":40},

      {"disease":"malaria","date":"2025-08-09","cases":12},
      {"disease":"malaria","date":"2025-08-10","cases":14},
      {"disease":"malaria","date":"2025-08-11","cases":15},
      {"disease":"malaria","date":"2025-08-12","cases":16},
      {"disease":"malaria","date":"2025-08-13","cases":16},
      {"disease":"malaria","date":"2025-08-14","cases":17},
      {"disease":"malaria","date":"2025-08-15","cases":20},

      {"disease":"cholera","date":"2025-08-09","cases":14,"tests":130,"positives":16},
      {"disease":"cholera","date":"2025-08-10","cases":12,"tests":125,"positives":14},
      {"disease":"cholera","date":"2025-08-11","cases":13,"tests":135,"positives":15},
      {"disease":"cholera","date":"2025-08-12","cases":15,"tests":140,"positives":18},
      {"disease":"cholera","date":"2025-08-13","cases":17,"tests":145,"positives":20},
      {"disease":"cholera","date":"2025-08-14","cases":18,"tests":150,"positives":22},
      {"disease":"cholera","date":"2025-08-15","cases":20,"tests":150,"positives":23},

      {"disease":"influenza_ili","date":"2025-08-09","cases":70},
      {"disease":"influenza_ili","date":"2025-08-10","cases":75},
      {"disease":"influenza_ili","date":"2025-08-11","cases":72},
      {"disease":"influenza_ili","date":"2025-08-12","cases":78},
      {"disease":"influenza_ili","date":"2025-08-13","cases":80},
      {"disease":"influenza_ili","date":"2025-08-14","cases":85},
      {"disease":"influenza_ili","date":"2025-08-15","cases":88},

      {"disease":"common_cold","date":"2025-08-09","cases":200},
      {"disease":"common_cold","date":"2025-08-10","cases":220},
      {"disease":"common_cold","date":"2025-08-11","cases":210},
      {"disease":"common_cold","date":"2025-08-12","cases":230},
      {"disease":"common_cold","date":"2025-08-13","cases":240},
      {"disease":"common_cold","date":"2025-08-14","cases":250},
      {"disease":"common_cold","date":"2025-08-15","cases":260},

      {"disease":"conjunctivitis","date":"2025-08-09","cases":40},
      {"disease":"conjunctivitis","date":"2025-08-10","cases":42},
      {"disease":"conjunctivitis","date":"2025-08-11","cases":44},
      {"disease":"conjunctivitis","date":"2025-08-12","cases":46},
      {"disease":"conjunctivitis","date":"2025-08-13","cases":48},
      {"disease":"conjunctivitis","date":"2025-08-14","cases":50},
      {"disease":"conjunctivitis","date":"2025-08-15","cases":52}
    ]
  },

  "baselines": {
    "departments": {
      "ER":           { "staff": { "doctors": 10, "nurses": 14, "support": 8 } },
      "Medicine":     { "staff": { "doctors": 8,  "nurses": 12, "support": 6 } },
      "ENT":          { "staff": { "doctors": 3,  "nurses": 4,  "support": 2 } },
      "Dermatology":  { "staff": { "doctors": 3,  "nurses": 4,  "support": 2 } },
      "Pediatrics":   { "staff": { "doctors": 5,  "nurses": 8,  "support": 4 } },
      "Ophthalmology":{ "staff": { "doctors": 3,  "nurses": 4,  "support": 2 } }
    },
    "bundles_per_day": {
      "RESPIRATORY_CARE": { "Neb_kit": 40, "Masks": 200, "O2_Hours": 600 },
      "DENGUE_CARE":      { "Platelet_units": 18, "IV_set": 150, "Paracetamol_tabs": 800 },
      "MALARIA_CARE":     { "Malaria_RDT": 45, "Antimalarials": 60, "IV_set": 120 },
      "WATERBORNE_CARE":  { "ORS": 220, "IV_set": 160, "Stool_RDT": 20 },
      "CONJUNCTIVITIS_CARE": { "Eye_Lubricants": 60, "Antibiotic_Eye_Drops": 50 },
      "DERMATOPHYTE_CARE":   { "Topical_Azole": 60, "Antifungal_Shampoo": 30 }
    },
    "diagnostics_per_day": { "CBC": 120, "Dengue_NS1": 25, "Malaria_RDT": 45, "Stool_RDT": 20 },
    "infra": { "Ward_Beds": 300, "ICU_Beds": 40, "Ambulances": 5, "O2_Hours": 6000 },
    "inventory_state": {
      "ORS": { "on_hand": 700, "on_order": 0, "lead_time_days": 5 },
      "IV_set": { "on_hand": 300, "on_order": 100, "lead_time_days": 7 },
      "Neb_kit": { "on_hand": 50, "on_order": 0, "lead_time_days": 10 },
      "Masks": { "on_hand": 1000, "on_order": 0, "lead_time_days": 3 },
      "O2_Hours": { "on_hand": 4000, "on_order": 0, "lead_time_days": 1 },
      "Platelet_units": { "on_hand": 40, "on_order": 0, "lead_time_days": 2 },
      "Paracetamol_tabs": { "on_hand": 3000, "on_order": 0, "lead_time_days": 5 },
      "Malaria_RDT": { "on_hand": 60, "on_order": 0, "lead_time_days": 7 },
      "Antimalarials": { "on_hand": 100, "on_order": 0, "lead_time_days": 5 },
      "Stool_RDT": { "on_hand": 25, "on_order": 0, "lead_time_days": 7 },
      "Eye_Lubricants": { "on_hand": 80, "on_order": 0, "lead_time_days": 6 },
      "Antibiotic_Eye_Drops": { "on_hand": 60, "on_order": 0, "lead_time_days": 6 },
      "Topical_Azole": { "on_hand": 120, "on_order": 0, "lead_time_days": 6 },
      "Antifungal_Shampoo": { "on_hand": 40, "on_order": 0, "lead_time_days": 6 },
      "Dengue_NS1": { "on_hand": 30, "on_order": 0, "lead_time_days": 5 }
    }
  }
}
