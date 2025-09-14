# Cell 1 — write the module to /content and import its functions --AI Accepted Functions Included

# -*- coding: utf-8 -*-
# Surge planner with optional LLM-assisted:
#   (1) NLG for human brief  (--nlg-ai)
#   (2) Free-text event parsing -> structured multipliers (--ai-events)
# Safe defaults:
# - If AI is disabled or unavailable, falls back to deterministic behavior.
# - Multipliers are capped, departments allow-listed, and merged by max.

import json, math, sys, argparse, os
from datetime import date, timedelta
from collections import defaultdict

BUNDLE_CATALOG = {
    "RESPIRATORY_CARE": ["Neb_kit","Masks","O2_Hours"],
    "DENGUE_CARE": ["Platelet_units","IV_set","Paracetamol_tabs"],
    "MALARIA_CARE": ["Malaria_RDT","Antimalarials","IV_set"],
    "WATERBORNE_CARE": ["ORS","IV_set","Stool_RDT"],
    "TYPHOID_CARE": ["Typhoid_RDT","Antibiotics_typhoid","IV_set"],
    "ILI_FLU_CARE": ["Masks","Antivirals","Neb_kit"],
    "COVID19_CARE": ["RAT_Kit","RT_PCR_Kit","Masks"],
    "CONJUNCTIVITIS_CARE": ["Eye_Lubricants","Antibiotic_Eye_Drops"],
    "DERMATOPHYTE_CARE": ["Topical_Azole","Antifungal_Shampoo"],
    "HEP_A_E_CARE": ["IV_set","ORS","Antiemetics"],
    "LEPTOSPIROSIS_CARE": ["Antibiotics_lepto","IV_set"],
    "SCRUB_TYPHUS_CARE": ["Doxycycline","IV_set"],
    "CHIKUNGUNYA_CARE": ["Analgesics","IV_set"],
    "TB_SCREENING_CARE": ["Sputum_Containers","GeneXpert_Cartridges"],
    "HFMD_CARE": ["Antipyretics","ORS"]
}

DISEASE_THRESHOLDS = {
    "default":             {"active_share_min": 0.05,  "growth_min": 0.20, "pos_min": None, "min_abs": 5},
    "dengue":              {"active_share_min": 0.02,  "growth_min": 0.15, "pos_min": None, "min_abs": 5},
    "malaria":             {"active_share_min": 0.015, "growth_min": 0.15, "pos_min": None, "min_abs": 5},
    "chikungunya":         {"active_share_min": 0.008, "growth_min": 0.25, "pos_min": None, "min_abs": 3},
    "scrub_typhus":        {"active_share_min": 0.008, "growth_min": 0.25, "pos_min": None, "min_abs": 3},
    "leptospirosis":       {"active_share_min": 0.008, "growth_min": 0.25, "pos_min": None, "min_abs": 3},
    "cholera":             {"active_share_min": 0.015, "growth_min": 0.25, "pos_min": 0.10, "min_abs": 5},
    "acute_gastroenteritis":{"active_share_min": 0.03, "growth_min": 0.25, "pos_min": None, "min_abs": 8},
    "typhoid":             {"active_share_min": 0.015, "growth_min": 0.20, "pos_min": None, "min_abs": 5},
    "hepatitis_A_E":       {"active_share_min": 0.008, "growth_min": 0.25, "pos_min": None, "min_abs": 3},
    "influenza_ili":       {"active_share_min": 0.06,  "growth_min": 0.20, "pos_min": None, "min_abs": 10},
    "covid19":             {"active_share_min": 0.03,  "growth_min": 0.20, "pos_min": 0.05, "min_abs": 8},
    "pneumonia_bacterial": {"active_share_min": 0.015, "growth_min": 0.20, "pos_min": None, "min_abs": 5},
    "asthma_copd_exacerb": {"active_share_min": 0.03,  "growth_min": 0.20, "pos_min": None, "min_abs": 8},
    "common_cold":         {"active_share_min": 0.10,  "growth_min": 0.20, "pos_min": None, "min_abs": 15},
    "allergic_rhinitis":   {"active_share_min": 0.07,  "growth_min": 0.20, "pos_min": None, "min_abs": 10},
    "conjunctivitis":      {"active_share_min": 0.04,  "growth_min": 0.30, "pos_min": None, "min_abs": 8},
    "dermatophyte_tinea":  {"active_share_min": 0.05,  "growth_min": 0.20, "pos_min": None, "min_abs": 8},
    "hfmd":                {"active_share_min": 0.015, "growth_min": 0.20, "pos_min": None, "min_abs": 5},
    "tb_suspected":        {"active_share_min": 0.01,  "growth_min": 0.15, "pos_min": None, "min_abs": 5}
}

DISEASE_ACTIONS_MULT = {
    "influenza_ili":         {"dept":{"ER":1.1, "Medicine":1.1}, "bundles":{"ILI_FLU_CARE":1.25}, "diags":{"CBC":1.2}},
    "covid19":               {"dept":{"ER":1.15, "Medicine":1.15}, "bundles":{"COVID19_CARE":1.5, "RESPIRATORY_CARE":1.25}, "diags":{"RAT_Kit":1.5, "RT_PCR_Kit":1.5}, "infra":{"Isolation_Beds":1.1}},
    "pneumonia_bacterial":   {"dept":{"ER":1.1, "Medicine":1.15}, "bundles":{"RESPIRATORY_CARE":1.3}, "diags":{"CBC":1.2, "CXR":1.2}},
    "asthma_copd_exacerb":   {"dept":{"ER":1.2, "Medicine":1.15}, "bundles":{"RESPIRATORY_CARE":1.25}, "diags":{}},
    "common_cold":           {"dept":{"ENT":1.1}, "bundles":{}, "diags":{}},
    "allergic_rhinitis":     {"dept":{"ENT":1.1}, "bundles":{}, "diags":{}},

    "dengue":                {"dept":{"ER":1.1, "Medicine":1.1, "Pediatrics":1.1}, "bundles":{"DENGUE_CARE":2.0}, "diags":{"Dengue_NS1":2.0}},
    "malaria":               {"dept":{"ER":1.1, "Medicine":1.1}, "bundles":{"MALARIA_CARE":1.5}, "diags":{"Malaria_RDT":1.5}},
    "chikungunya":           {"dept":{"Medicine":1.1}, "bundles":{"CHIKUNGUNYA_CARE":1.3}, "diags":{}},
    "scrub_typhus":          {"dept":{"Medicine":1.1}, "bundles":{"SCRUB_TYPHUS_CARE":1.3}, "diags":{}},

    "acute_gastroenteritis": {"dept":{"Pediatrics":1.1, "ER":1.1}, "bundles":{"WATERBORNE_CARE":1.2}, "diags":{"Stool_RDT":1.1}},
    "cholera":               {"dept":{"Pediatrics":1.15, "ER":1.1}, "bundles":{"WATERBORNE_CARE":1.3}, "diags":{"Stool_RDT":1.25}},
    "typhoid":               {"dept":{"Medicine":1.1, "Pediatrics":1.1}, "bundles":{"TYPHOID_CARE":1.25}, "diags":{"Typhoid_RDT":1.25}},
    "hepatitis_A_E":         {"dept":{"Medicine":1.1, "Pediatrics":1.1}, "bundles":{"HEP_A_E_CARE":1.25}, "diags":{"LFT_Panel":1.3}},

    "leptospirosis":         {"dept":{"Medicine":1.15}, "bundles":{"LEPTOSPIROSIS_CARE":1.3}, "diags":{"Lepto_IgM":1.3}},

    "conjunctivitis":        {"dept":{"Ophthalmology":1.2}, "bundles":{"CONJUNCTIVITIS_CARE":1.25}, "diags":{}},
    "dermatophyte_tinea":    {"dept":{"Dermatology":1.2}, "bundles":{"DERMATOPHYTE_CARE":1.25}, "diags":{}},

    "hfmd":                  {"dept":{"Pediatrics":1.15}, "bundles":{"HFMD_CARE":1.2}, "diags":{}},

    "tb_suspected":          {"dept":{"Medicine":1.1}, "bundles":{"TB_SCREENING_CARE":1.3}, "diags":{"GeneXpert":1.5}}
}

ENV_RULES = {
    "HUMID_HEAT": {
        "condition": lambda f, ev=None: f.get("humidity_7d_mean",0) >= 80 and f.get("temp_c_today",0) >= 28,
        "window": "D0–D5",
        "multipliers": {"dept": {"Dermatology":1.2, "ENT":1.2},"bundles": {"DERMATOPHYTE_CARE":1.25},"diags": {},"infra": {}}
    },
    "AQI_SPIKE": {
        "condition": lambda f, ev=None: f.get("pm25_last3_all_ge_200", False),
        "window": "D2–D5",
        "multipliers": {"dept": {"ER":1.2, "Medicine":1.15},"bundles": {"RESPIRATORY_CARE":1.25},"diags": {"CBC":1.2},"infra": {"O2_Hours":1.2}}
    },
    "RAINY_WEEK": {
        "condition": lambda f, ev=None: f.get("rain_7d_sum",0) >= 70,
        "window": "D7–D14",
        "multipliers": {"dept": {"Pediatrics":1.15, "ER":1.1},"bundles": {"WATERBORNE_CARE":1.3},"diags": {"Stool_RDT":1.25},"infra": {}}
    }
}

def derive_features(weather_past_7d):
    rain_7d_sum = sum(d.get("rain_mm",0) for d in weather_past_7d)
    humidity_7d_mean = sum(d.get("humidity_pct",0) for d in weather_past_7d) / max(len(weather_past_7d),1)
    pm_last3 = [d.get("pm25",0) for d in weather_past_7d][-3:]
    temp_today = (weather_past_7d[-1].get("temp_c",0) if weather_past_7d else 0)
    return {"rain_7d_sum": rain_7d_sum,"humidity_7d_mean": humidity_7d_mean,"temp_c_today": temp_today,"pm25_last3_all_ge_200": (len(pm_last3)==3 and all(x>=200 for x in pm_last3))}

def disease_sentinel_normalized(by_disease_daily, visits_daily, thresholds):
    total_by_date = { r.get("date"): (r.get("total_opd",0) or 0) for r in (visits_daily or []) }
    by = {}
    for r in (by_disease_daily or []):
        by.setdefault(r.get("disease"), []).append(r)
    out = []
    for name, rows in by.items():
        rows = sorted(rows, key=lambda x: x.get("date",""))
        last7 = rows[-7:] if len(rows)>=7 else rows
        prev7 = rows[-14:-7] if len(rows)>=14 else []
        active = sum((r.get("cases",0) or 0) for r in last7)
        prev = sum((r.get("cases",0) or 0) for r in prev7)
        tot7 = sum(total_by_date.get(r.get("date"),0) for r in last7)
        totPrev = sum(total_by_date.get(r.get("date"),0) for r in prev7)
        share = (active / tot7) if tot7>0 else 0.0
        sharePrev = (prev / totPrev) if totPrev>0 else 0.0
        growth = ((share/sharePrev)-1.0) if sharePrev>0 else (1.0 if share>0 else 0.0)
        th = thresholds.get(name, thresholds.get("default"))
        posDen = sum((r.get("tests",0) or 0) for r in last7)
        posNum = sum((r.get("positives",0) or 0) for r in last7)
        positivity = (posNum/posDen) if posDen>0 else None
        trigger = (active >= (th.get("min_abs") or 0)) and ((share >= th["active_share_min"]) or (growth >= th["growth_min"]) or (th.get("pos_min") is not None and positivity is not None and positivity >= th["pos_min"]))
        if trigger:
            severity = "high" if (share >= 2*th["active_share_min"] or growth >= 0.5) else "medium"
            out.append({"name": name,"active_cases": int(active),"active_share_pct": round(share*100,1),"growth_share_pct": round(growth*100,1),"positivity_pct": (round(positivity*100,1) if positivity is not None else None),"new_24h": int(last7[-1].get("cases",0)) if last7 else 0,"severity": severity})
    out.sort(key=lambda x: x["active_share_pct"], reverse=True)
    return out

def fire_env_rules(features, events):
    hits = []
    for rid, rule in ENV_RULES.items():
        try:
            if rule["condition"](features, events):
                hits.append({ "id": rid, "window": rule["window"], "multipliers": rule["multipliers"] })
        except Exception:
            pass
    return hits

def map_disease_to_multipliers(sentinel_hits):
    blocks = []
    for d in sentinel_hits:
        actions = DISEASE_ACTIONS_MULT.get(d["name"])
        if not actions:
            continue
        blocks.append({"id": f"DISEASE:{d['name']}","window": "D0–D7","multipliers": {"dept": actions.get("dept",{}),"bundles": actions.get("bundles",{}),"diags": actions.get("diags",{}),"infra": actions.get("infra",{})}})
    return blocks

def merge_max(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = max(out.get(k, 0.0), v)
    return out

def cap_values(d, cap):
    return {k: min(v, cap) for k, v in d.items()}

def merge_multipliers(blocks, cap=2.0):
    by_window = {}
    tags_by_window = defaultdict(list)
    for b in blocks:
        w = b["window"]
        cur = by_window.get(w, {"dept":{}, "bundles":{}, "diags":{}, "infra":{}})
        mp = b["multipliers"]
        cur["dept"]    = merge_max(cur["dept"],    mp.get("dept",{}))
        cur["bundles"] = merge_max(cur["bundles"], mp.get("bundles",{}))
        cur["diags"]   = merge_max(cur["diags"],   mp.get("diags",{}))
        cur["infra"]   = merge_max(cur["infra"],   mp.get("infra",{}))
        by_window[w] = cur
        tags_by_window[w].append(b["id"])
    horizons = []
    for w, m in by_window.items():
        horizons.append({"window": w,"dept_multipliers":   cap_values(m["dept"], cap),"bundle_multipliers": cap_values(m["bundles"], cap),"diag_multipliers":   cap_values(m["diags"], cap),"infra_multipliers":  cap_values(m["infra"], cap),"trigger_tags": tags_by_window[w]})
    def win_key(w):
        import re
        m = re.search(r"D(\d+)", w)
        return int(m.group(1)) if m else 999
    horizons.sort(key=lambda h: win_key(h["window"]))
    return horizons

# --------- LLM helpers ----------
import requests

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def _get_openrouter_headers():
    """
    Reads OPENROUTER_API_KEY from environment; returns headers or None.
    You can optionally set HTTP-Referer and X-Title to identify your app.
    """
    api_key = api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key:
        return None
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        # Optional but recommended:
        # "HTTP-Referer": "https://your-site.example",  # Must be a valid URL if you set it
        # "X-Title": "Surge Planner",
    }

def _openrouter_chat(messages, model="openai/gpt-4o-mini", **extra_payload):
    """
    Minimal helper around OpenRouter chat.completions.
    Returns the string content of the first choice, or None on failure.
    """
    headers = _get_openrouter_headers()
    if not headers:
        return None

    payload = {
        "model": model,
        "messages": messages,
    }
    # carry through any additional OpenAI-compatible fields (e.g., response_format)
    payload.update(extra_payload)

    try:
        resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=45)
        resp.raise_for_status()
        data = resp.json()
        return (data.get("choices") or [{}])[0].get("message", {}).get("content")
    except Exception:
        return None

def make_human_nlg(plan, features, env_blocks, translated=None, model="openai/gpt-4o-mini"):
    facts = {
        "valid_for": plan.get("valid_for"),
        "features": features,
        "env_triggers": env_blocks,
        "disease_sentinel": plan.get("disease_sentinel", []),
        "horizons": plan.get("horizons", []),
        "advisories": plan.get("advisories", []),
        "translated": translated or {}
    }

    messages = [
        {"role": "system", "content": "You are a hospital operations writer for India. Write a concise, actionable surge brief ONLY from the provided facts. Do not invent numbers or dates. Use clear bullets; 200–300 words."},
        {"role": "user", "content": f"FACTS (JSON):\n{json.dumps(facts, ensure_ascii=False)}"}
    ]

    out = _openrouter_chat(messages, model=model)
    return out or human_readable(plan, features, env_blocks, translated)

def parse_event_to_block(event_text, today_iso, cap=2.0, min_conf=0.5, model="openai/gpt-4o-mini"):
    headers = _get_openrouter_headers()
    if not headers:
        return None

    system = (
        "You are a hospital surge planner. Convert the EVENT into a structured block for operational multipliers.\n"
        "Rules:\n"
        "- Output STRICT JSON only, no extra text.\n"
        "- Keys: id, window, confidence, reasoning, multipliers (dept, bundles, diags, infra).\n"
        "- Window must look like: \"D0–D1\", \"D0–D2\", \"D0–D5\", \"D2–D5\", \"D7–D14\".\n"
        "- Allowed departments: ER, Medicine, ENT, Dermatology, Pediatrics, Ophthalmology.\n"
        "- Multiplier values must be floats in [1.0, " + str(cap) + "]\n"
        "- Be conservative if unsure."
    )

    user = f'TODAY="{today_iso}"\nEVENT="{event_text}"\nReturn JSON only.'

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        # Ask for a strict JSON object in the reply
        "response_format": {"type": "json_object"}
    }

    try:
        resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=45)
        resp.raise_for_status()
        data = resp.json()
        raw = (data.get("choices") or [{}])[0].get("message", {}).get("content", "")
        obj = json.loads(raw) if raw else {}
    except Exception:
        return None

    def clamp(x):
        try:
            return max(1.0, min(float(x), cap))
        except:
            return 1.0

    allowed_depts = {"ER","Medicine","ENT","Dermatology","Pediatrics","Ophthalmology"}
    mp = obj.get("multipliers", {}) or {}
    mp.setdefault("dept", {}); mp.setdefault("bundles", {}); mp.setdefault("diags", {}); mp.setdefault("infra", {})
    mp["dept"]    = {k: clamp(v) for k, v in mp["dept"].items() if k in allowed_depts}
    mp["bundles"] = {k: clamp(v) for k, v in mp["bundles"].items()}
    mp["diags"]   = {k: clamp(v) for k, v in mp["diags"].items()}
    mp["infra"]   = {k: clamp(v) for k, v in mp["infra"].items()}



    try:
        conf = float(obj.get("confidence", 0.0))
    except Exception:
        conf = 0.0

    if not obj.get("id") or not obj.get("window"):
        return None
    if not any([mp["dept"], mp["bundles"], mp["diags"], mp["infra"]]):
        return None
    if conf < min_conf:
        return None

    return {
        "id": obj["id"],
        "window": obj["window"],
        "multipliers": mp,
        "confidence": conf,
        "reasoning": obj.get("reasoning","")
    }

# --------- Human readable ----------

def human_readable(plan, features, env_blocks, translated=None):
    lines = []
    lines.append(f"Surge Plan for {plan.get('valid_for','')}")
    lines.append("")
    lines.append("Environment features:")
    lines.append(f"  - Rain 7d sum: {features.get('rain_7d_sum',0)} mm")
    lines.append(f"  - Humidity 7d mean: {features.get('humidity_7d_mean',0):.1f}%")
    lines.append(f"  - Temp today: {features.get('temp_c_today',0)} °C")
    lines.append(f"  - PM2.5 last 3 all >=200: {features.get('pm25_last3_all_ge_200',False)}")
    lines.append("")
    if env_blocks:
        lines.append("Environment triggers fired:")
        for b in env_blocks:
            lines.append(f"  - {b['id']} @ {b['window']}")
        lines.append("")
    ds = plan.get("disease_sentinel",[])
    lines.append("Disease sentinel (share of OPD, last 7d):")
    if not ds:
        lines.append("  - None above thresholds")
    else:
        for d in ds:
            pos = f", Positivity {d['positivity_pct']}%" if d.get("positivity_pct") is not None else ""
            lines.append(f"  - {d['name']}: {d['active_share_pct']}% (WoW +{d['growth_share_pct']}%), new24h {d['new_24h']}, severity {d['severity']}{pos}")
    lines.append("")
    lines.append("Horizon multipliers:")
    for h in plan.get("horizons",[]):
        lines.append(f"  {h['window']} [{', '.join(h.get('trigger_tags',[]))}]")
        if h.get("dept_multipliers"):
            lines.append("    Dept: " + ", ".join(f"{k} {v:.2f}x" for k,v in h["dept_multipliers"].items()))
        if h.get("bundle_multipliers"):
            lines.append("    Bundles: " + ", ".join(f"{k} {v:.2f}x" for k,v in h["bundle_multipliers"].items()))
        if h.get("diag_multipliers"):
            lines.append("    Diagnostics: " + ", ".join(f"{k} {v:.2f}x" for k,v in h["diag_multipliers"].items()))
        if h.get("infra_multipliers"):
            lines.append("    Infra: " + ", ".join(f"{k} {v:.2f}x" for k,v in h["infra_multipliers"].items()))
    lines.append("")
    if plan.get("advisories"):
        lines.append("Advisories:")
        for a in plan["advisories"]:
            lines.append(f"  - [{a['channel']}] {a['audience']}: {a['message']}")
        lines.append("")
    if translated:
        lines.append("Translated actions:")
        if translated.get("rosters"):
            lines.append("  Rosters (final counts):")
            for win, deps in translated["rosters"].items():
                lines.append(f"    {win}:")
                for dname, staff in deps.items():
                    lines.append(f"      - {dname}: Dr {staff['doctors']}, Nurse {staff['nurses']}, Support {staff['support']}")
        if translated.get("infra_peak"):
            lines.append("  Infra peak:")
            for k,v in translated["infra_peak"].items():
                lines.append(f"    - {k}: {v}")
        if translated.get("purchase_orders"):
            lines.append("  Purchase orders (7d cover, max multiplier):")
            for po in translated["purchase_orders"]:
                lines.append(f"    - {po['sku']}: {po['qty']} ({po['urgency']})")
    return "\n".join(lines)

# --------- Plan builder ----------

def build_multiplier_plan(inputs, cap=2.0, ai_events=False, ai_min_conf=0.5, ai_model="gpt-4o-mini"):
    today = inputs.get("meta",{}).get("today")
    end = str(date.fromisoformat(today) + timedelta(days=14)) if today else ""
    features = derive_features(inputs.get("weather_past_7d",[]))
    sentinel = disease_sentinel_normalized(inputs.get("epi_signals",{}).get("by_disease_daily",[]), inputs.get("visits_daily",[]), DISEASE_THRESHOLDS)
    env_blocks = fire_env_rules(features, inputs.get("events",[]))
    dis_blocks = map_disease_to_multipliers(sentinel)
    ai_blocks = []
    ai_trace = []
    if ai_events:
        for txt in inputs.get("free_text_events", []):
            blk = parse_event_to_block(txt, today, cap=cap, min_conf=ai_min_conf, model=ai_model)
            if blk:
                ai_blocks.append({k: blk[k] for k in ["id","window","multipliers"]})
                ai_trace.append({"text": txt, "id": blk["id"], "window": blk["window"], "confidence": blk["confidence"], "reasoning": blk.get("reasoning","")})
    horizons = merge_multipliers(env_blocks + dis_blocks + ai_blocks, cap=cap)
    plan = {
        "valid_for": f"{today}/{end}",
        "disease_sentinel": sentinel,
        "horizons": horizons,
        "assumptions": [f"MAX per target when overlaps; cap multipliers at {cap:.1f}×","Disease multipliers default to D0–D7 window","Environment rules: HUMID_HEAT(D0–D5), AQI_SPIKE(D2–D5), RAINY_WEEK(D7–D14)"],
        "advisories": []
    }
    tags = [t for h in horizons for t in h.get("trigger_tags",[])]
    adv = []
    if "AQI_SPIKE" in tags:
        adv.append({"audience":"COPD/asthma","language":"EN","channel":"SMS","message":"Poor air in 2–5 days. Keep inhalers ready; avoid outdoor exertion; ER if breathless."})
    if "RAINY_WEEK" in tags:
        adv.append({"audience":"All households","language":"EN","channel":"SMS","message":"After heavy rains, waterborne illness risk in 1–2 weeks. Boil water; use ORS for loose stools."})
    if "HUMID_HEAT" in tags:
        adv.append({"audience":"All","language":"EN","channel":"Display","message":"High humidity now → fungal/skin issues. Keep skin dry; change damp clothes; see Dermatology if rash."})
    plan["advisories"] = adv
    if ai_trace:
        plan["ai_event_trace"] = ai_trace
    return plan, features, env_blocks

# --------- Translator ----------

def apply_multipliers(multiplier_plan, baselines, days_cover=7):
    rosters = {}
    for hz in multiplier_plan.get("horizons",[]):
        window = hz["window"]
        rosters[window] = {}
        for dept, m in hz.get("dept_multipliers",{}).items():
            base = baselines.get("departments",{}).get(dept,{}).get("staff")
            if not base:
                continue
            rosters[window][dept] = {"doctors":  max(0, math.ceil(base.get("doctors",0) * m)),"nurses":   max(0, math.ceil(base.get("nurses",0)  * m)),"support":  max(0, math.ceil(base.get("support",0) * m))}
    max_bundle_mult = defaultdict(float); max_diag_mult = defaultdict(float); max_infra_mult = defaultdict(float)
    for hz in multiplier_plan.get("horizons",[]):
        for b, m in hz.get("bundle_multipliers",{}).items(): max_bundle_mult[b] = max(max_bundle_mult[b], m)
        for d, m in hz.get("diag_multipliers",{}).items():   max_diag_mult[d]   = max(max_diag_mult[d], m)
        for i, m in hz.get("infra_multipliers",{}).items():  max_infra_mult[i]  = max(max_infra_mult[i], m)
    sku_need = defaultdict(int); bundles_per_day = baselines.get("bundles_per_day",{})
    for bundle, m in max_bundle_mult.items():
        per_day = bundles_per_day.get(bundle,{})
        for sku, base_per_day in per_day.items():
            sku_need[sku] += math.ceil(base_per_day * m * days_cover)
    diagnostics_per_day = baselines.get("diagnostics_per_day",{})
    for test, m in max_diag_mult.items():
        base_per_day = diagnostics_per_day.get(test,0)
        if base_per_day:
            sku_need[test] += math.ceil(base_per_day * m * days_cover)
    inventory_state = baselines.get("inventory_state",{})
    pos = []
    for sku, needed in sku_need.items():
        inv = inventory_state.get(sku, {"on_hand":0,"on_order":0,"lead_time_days":7})
        gap = max(0, needed - inv.get("on_hand",0) - inv.get("on_order",0))
        if gap == 0:
            continue
        ltd = inv.get("lead_time_days",7)
        urgency = "critical" if ltd > days_cover else ("expedite" if ltd >= days_cover-1 else "routine")
        pos.append({"sku":sku, "qty":gap, "urgency":urgency})
    infra_peak = {}
    for item, m in max_infra_mult.items():
        base = baselines.get("infra",{}).get(item)
        if base:
            infra_peak[item] = math.ceil(base * m)
    return {"rosters": rosters, "purchase_orders": pos, "infra_peak": infra_peak}

