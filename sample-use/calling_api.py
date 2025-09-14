import requests

API_URL = "http://surge-planner-production.up.railway.app/plan"

# Minimal sample payload matching what your API expects
sample_input = {
    "meta": {"today": "2025-09-14"},
    "baselines": {
        "departments": {
            "ER": {"staff": {"doctors": 4, "nurses": 8, "support": 4}}
        },
        "bundles_per_day": {},
        "diagnostics_per_day": {},
        "inventory_state": {},
        "infra": {}
    },
    "weather_past_7d": [],
    "visits_daily": [],
    "epi_signals": {"by_disease_daily": []}
}

resp = requests.post(API_URL, json=sample_input)

print("Status:", resp.status_code)
print("Response JSON:\n", resp.json())
