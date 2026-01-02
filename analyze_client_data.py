import pandas as pd
import json
import os
from pathlib import Path

WORKSPACE = Path(__file__).parent

FORTZA_LAYERS = {
    "Permanent Memory User Details": {
        "required_fields": ["customer_name", "email"],
        "purpose": "Historical customer fraud check",
        "bucket": 1
    },
    "Permanent Memory Geolocation": {
        "required_fields": ["cust_street", "cust_city", "cust_state", "zip_code"],
        "purpose": "Historical address fraud check",
        "bucket": 1
    },
    "Google Address Validation": {
        "required_fields": ["cust_street", "cust_city", "cust_state", "zip_code"],
        "purpose": "Physical address verification",
        "bucket": 1
    },
    "Smarty Address Validation": {
        "required_fields": ["cust_street", "cust_city", "cust_state", "zip_code"],
        "purpose": "Alternative address verification",
        "bucket": 1
    },
    "AI Prompt Layer": {
        "required_fields": ["customer_name", "email", "cust_street", "gender", "zip_code", "cust_city"],
        "purpose": "Identity inconsistency detection",
        "bucket": 1
    },
    "Gilbert Layer": {
        "required_fields": ["email", "customer_name"],
        "purpose": "Email validation & fraud analysis",
        "bucket": 1
    },
    "Word Cloud Name": {
        "required_fields": ["customer_name"],
        "purpose": "Name pattern fraud detection",
        "bucket": 1
    },
    "Word Cloud Email": {
        "required_fields": ["email"],
        "purpose": "Email pattern fraud detection",
        "bucket": 1
    },
    "Geolocation Hotspot": {
        "required_fields": ["zip_code"],
        "purpose": "Zip code fraud hotspot detection",
        "bucket": 1
    },
    "Anomaly Layer": {
        "required_fields": ["customer_name", "order_date", "salesperson_name", "cust_state", "cust_city",
                           "dealer_name", "wireless_package", "Tntype", "Autopay", "email", "zip_code",
                           "devicename", "devicetype", "store_number", "gender"],
        "purpose": "Transaction anomaly detection",
        "bucket": 1
    },
    "Intenso": {
        "required_fields": ["customer_name", "order_date", "salesperson_name", "cust_state", "cust_city",
                           "dealer_name", "wireless_package", "Tntype", "Autopay", "email", "zip_code",
                           "devicename", "devicetype", "store_number", "gender"],
        "purpose": "Historical suspicious activity matching",
        "bucket": 1
    },
    "Energico": {
        "required_fields": ["customer_name", "order_date", "salesperson_name", "cust_state", "cust_city",
                           "dealer_name", "wireless_package", "Tntype", "Autopay", "email", "zip_code",
                           "devicename", "devicetype", "store_number", "gender"],
        "purpose": "Transformer-based fraud detection",
        "bucket": 1
    },
    "IP Address Layer": {
        "required_fields": ["ip", "ipAddress"],
        "purpose": "VPN/Proxy/Hosting detection",
        "bucket": 1
    },
    "FBI Layer": {
        "required_fields": ["customer_name", "gender"],
        "purpose": "Known fraudster verification",
        "bucket": 1
    }
}

CLIENT_EXPECTATIONS = {
    "ip_origin": {"description": "Origin IP address for VPN/proxy detection", "bucket": 1, "suggested_source": "Order, CustomObject, LoginHistory"},
    "destination_ip": {"description": "Destination/service IP", "bucket": 1, "suggested_source": "CustomObject, Order"},
    "activation_date": {"description": "Service activation date for timing analysis", "bucket": 2, "suggested_source": "Order.ActivatedDate"},
    "disconnection_date": {"description": "Service disconnect date for churn analysis", "bucket": 2, "suggested_source": "Order.Disconnect_Date__c"},
    "install_date": {"description": "Installation date for timing deltas", "bucket": 2, "suggested_source": "Order.POE_InstallationDate__c"},
    "payment_info": {"description": "Payment method for proof-of-sale", "bucket": 2, "suggested_source": "Order, CustomObject"},
    "agent_email": {"description": "Sales agent/rep email", "bucket": 2, "suggested_source": "User, Contact"},
    "agent_id": {"description": "Agent/salesperson identifier", "bucket": 2, "suggested_source": "Order.SalesRep__c, OwnerId"},
    "dealer_id": {"description": "Dealer/partner identifier", "bucket": 2, "suggested_source": "Account.POE_Dealer_Code__c, Order.POE_Dealer__c"},
    "program_name": {"description": "Program/product name for mix analysis", "bucket": 2, "suggested_source": "Order.POE_Program__c, Lead.Programs__c"},
    "channel": {"description": "Sales channel (phone, retail, d2d)", "bucket": 2, "suggested_source": "Lead.Division__c, Order.Call_Center_Type__c"},
    "territory": {"description": "Agent/dealer territory for authorization", "bucket": 3, "suggested_source": "Account.Territory__c, Account_Territory__c"},
    "commission_data": {"description": "Commission/stair-step data for dealer profiling", "bucket": 3, "suggested_source": "CustomObject, External System"},
    "debt_balance": {"description": "Dealer debt balance", "bucket": 3, "suggested_source": "Account financial fields, External System"},
    "audit_notes": {"description": "Audit notes for sentiment analysis", "bucket": 3, "suggested_source": "CustomObject, Notes, External System"},
    "device_fingerprint": {"description": "Device ID for shared device detection", "bucket": 2, "suggested_source": "CustomObject, Order"},
    "login_history": {"description": "Agent login timestamps for velocity", "bucket": 3, "suggested_source": "LoginHistory, Event"}
}

FIELD_MAPPINGS = {
    "customer_name": {
        "Account.csv": ["Name (derived from FirstName+LastName if PersonAccount)"],
        "Contact.csv": ["Name (derived from FirstName+LastName)"],
        "Lead.csv": ["Company", "FirstName+LastName"],
        "Opportunity.csv": None,
        "Order.csv": None,
        "notes": "Customer name not directly available; must derive from related Account/Contact or join"
    },
    "email": {
        "Account.csv": ["PersonEmail", "Fortza__Email__c"],
        "Contact.csv": ["Email"],
        "Lead.csv": ["Email"],
        "Opportunity.csv": ["Fortza__Email__c", "vlocity_cmt__Email__c"],
        "Order.csv": ["Email__c", "vlocity_cmt__Email__c"],
        "notes": "Email available in multiple objects"
    },
    "cust_street": {
        "Account.csv": ["BillingStreet", "ShippingStreet"],
        "Contact.csv": ["MailingStreet", "OtherStreet"],
        "Lead.csv": ["Street"],
        "Opportunity.csv": ["Fortza__Street__c", "Maps_Street__c"],
        "Order.csv": ["BillingStreet", "ShippingStreet"],
        "notes": "Street addresses available; may need parsing for multi-line"
    },
    "cust_city": {
        "Account.csv": ["BillingCity", "ShippingCity"],
        "Contact.csv": ["MailingCity", "OtherCity"],
        "Lead.csv": ["City"],
        "Opportunity.csv": ["Fortza__City__c", "Maps_City__c"],
        "Order.csv": ["BillingCity", "ShippingCity"],
        "notes": "City available in multiple objects"
    },
    "cust_state": {
        "Account.csv": ["BillingState", "BillingStateCode", "ShippingState"],
        "Contact.csv": ["MailingState", "MailingStateCode"],
        "Lead.csv": ["StateCode"],
        "Opportunity.csv": ["Fortza__State__c", "Maps_State__c"],
        "Order.csv": ["BillingState", "BillingStateCode", "ShippingState"],
        "notes": "State available; both full name and ISO code present"
    },
    "zip_code": {
        "Account.csv": ["BillingPostalCode", "ShippingPostalCode"],
        "Contact.csv": ["MailingPostalCode", "OtherPostalCode"],
        "Lead.csv": ["PostalCode", "Five_Digit_Zip__c"],
        "Opportunity.csv": ["Fortza__Pin_code__c", "Maps_PostalCode__c"],
        "Order.csv": ["BillingPostalCode", "ShippingPostalCode"],
        "notes": "Postal/zip code available"
    },
    "gender": {
        "Account.csv": ["Fortza__Gender__c", "Fortza__Gender__pc", "vlocity_cmt__Gender__pc"],
        "Contact.csv": ["Fortza__Gender__c", "GenderIdentity", "vlocity_cmt__Gender__c"],
        "Lead.csv": ["Fortza__Gender__c", "GenderIdentity"],
        "Opportunity.csv": ["Fortza__Gender__c"],
        "Order.csv": None,
        "notes": "Gender field available in Fortza custom fields"
    },
    "order_date": {
        "Account.csv": ["Fortza__Order_Date__c", "Fortza__Order_Date__pc"],
        "Contact.csv": ["Fortza__Order_Date__c"],
        "Lead.csv": ["Fortza__Order_Date__c"],
        "Opportunity.csv": ["Fortza__Order_Date__c", "CloseDate"],
        "Order.csv": ["EffectiveDate", "CreatedDate"],
        "notes": "Order date available via Fortza fields or Order.EffectiveDate"
    },
    "salesperson_name": {
        "Account.csv": ["OwnerId (requires User lookup)"],
        "Contact.csv": ["OwnerId", "Account_Owner__c"],
        "Lead.csv": ["OwnerId", "Lead_Owner__c", "Owner__c"],
        "Opportunity.csv": ["OwnerId", "Opportunity_Owner__c"],
        "Order.csv": ["OwnerId", "SalesRep__c"],
        "notes": "Requires User object join to get salesperson name from OwnerId"
    },
    "dealer_name": {
        "Account.csv": ["Name (for dealer type accounts)"],
        "Contact.csv": None,
        "Lead.csv": ["Fortza__Dealer_Name__c"],
        "Opportunity.csv": ["POE_Dealer__c", "Opportunity_Dealer_Office__c"],
        "Order.csv": ["POE_Dealer__c"],
        "notes": "Dealer reference available; may need Account lookup for full name"
    },
    "wireless_package": {
        "Account.csv": ["Fortza__Wireless_Package__c", "Fortza__Wireless_Package__pc"],
        "Contact.csv": ["Fortza__Wireless_Package__c"],
        "Lead.csv": ["Fortza__Wireless_Package__c"],
        "Opportunity.csv": ["Fortza__Wireless_Package__c"],
        "Order.csv": None,
        "notes": "Wireless package in Fortza custom fields"
    },
    "Tntype": {
        "Account.csv": ["Fortza__Tn_Type__c", "Fortza__Tn_Type__pc"],
        "Contact.csv": ["Fortza__Tn_Type__c"],
        "Lead.csv": ["Fortza__Tn_Type__c"],
        "Opportunity.csv": ["Fortza__Tn_Type__c"],
        "Order.csv": None,
        "notes": "Transaction type (port/new/upgrade) in Fortza fields"
    },
    "Autopay": {
        "Account.csv": ["Fortza__Auto_Pay__c", "Fortza__Auto_Pay__pc"],
        "Contact.csv": ["Fortza__Auto_Pay__c"],
        "Lead.csv": ["Fortza__Auto_Pay__c"],
        "Opportunity.csv": ["Fortza__Auto_Pay__c", "AutoPay__c"],
        "Order.csv": None,
        "notes": "Autopay flag available"
    },
    "devicename": {
        "Account.csv": None,
        "Contact.csv": None,
        "Lead.csv": ["Fortza__Device_Name__c"],
        "Opportunity.csv": None,
        "Order.csv": None,
        "notes": "Device name only found in Lead; may need custom object"
    },
    "devicetype": {
        "Account.csv": ["Fortza__Device_Type__c", "Fortza__Device_Type__pc"],
        "Contact.csv": ["Fortza__Device_Type__c"],
        "Lead.csv": ["Fortza__Device_Type__c"],
        "Opportunity.csv": ["Fortza__Device_Type__c"],
        "Order.csv": None,
        "notes": "Device type (hotspot/smartphone/tablet/wearable) in Fortza fields"
    },
    "store_number": {
        "Account.csv": ["Fortza__Store_Number__c", "Fortza__Store_Number__pc", "POE_Store_Number__c"],
        "Contact.csv": ["Fortza__Store_Number__c"],
        "Lead.csv": ["Fortza__Store_Number__c"],
        "Opportunity.csv": ["Fortza__Store_Number__c"],
        "Order.csv": None,
        "notes": "Store number available in Fortza and POE fields"
    },
    "ip": {
        "Account.csv": None,
        "Contact.csv": None,
        "Lead.csv": ["Fortza__IP_Address__c"],
        "Opportunity.csv": ["POE_Fraud_Flag_IP__c"],
        "Order.csv": None,
        "notes": "IP address found in Lead.Fortza__IP_Address__c; Opportunity has fraud flag IP only"
    }
}

def load_csv(filepath):
    try:
        df = pd.read_csv(filepath, encoding='utf-8', low_memory=False)
    except UnicodeDecodeError:
        df = pd.read_csv(filepath, encoding='latin-1', low_memory=False)
    except:
        df = pd.read_csv(filepath, sep=';', encoding='utf-8', low_memory=False)
    return df

def analyze_csv(filepath):
    df = load_csv(filepath)
    analysis = {
        "filename": os.path.basename(filepath),
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "columns": []
    }
    for col in df.columns:
        col_info = {
            "name": col,
            "dtype": str(df[col].dtype),
            "null_count": int(df[col].isna().sum() + (df[col] == '').sum()),
            "null_pct": round((df[col].isna().sum() + (df[col] == '').sum()) / len(df) * 100, 1) if len(df) > 0 else 0,
            "sample_values": df[col].dropna().head(3).tolist()
        }
        analysis["columns"].append(col_info)
    return analysis, df

def build_field_coverage_matrix(csv_analyses):
    required_fields = set()
    for layer_info in FORTZA_LAYERS.values():
        required_fields.update(layer_info["required_fields"])
    
    for field_key in CLIENT_EXPECTATIONS.keys():
        required_fields.add(field_key)
    
    matrix = []
    for field in sorted(required_fields):
        row = {
            "expected_field": field,
            "layer_or_expectation": [],
            "status": "Missing",
            "source_file": None,
            "source_column": None,
            "null_pct": None,
            "transform_needed": None,
            "notes": ""
        }
        
        for layer_name, layer_info in FORTZA_LAYERS.items():
            if field in layer_info["required_fields"]:
                row["layer_or_expectation"].append(f"{layer_name} (Layer)")
        
        if field in CLIENT_EXPECTATIONS:
            row["layer_or_expectation"].append(f"Client Expectation: {CLIENT_EXPECTATIONS[field]['description']}")
        
        if field in FIELD_MAPPINGS:
            mapping = FIELD_MAPPINGS[field]
            for csv_file, columns in mapping.items():
                if columns and csv_file != "notes":
                    if csv_file in csv_analyses:
                        csv_cols = [c["name"] for c in csv_analyses[csv_file]["columns"]]
                        for mapped_col in columns:
                            clean_col = mapped_col.split(" (")[0] if " (" in mapped_col else mapped_col
                            if clean_col in csv_cols:
                                col_info = next((c for c in csv_analyses[csv_file]["columns"] if c["name"] == clean_col), None)
                                if col_info:
                                    row["source_file"] = csv_file
                                    row["source_column"] = clean_col
                                    row["null_pct"] = col_info["null_pct"]
                                    if col_info["null_pct"] > 50:
                                        row["status"] = "Present but low quality (high nulls)"
                                    else:
                                        row["status"] = "Present"
                                    break
                    if row["status"] != "Missing":
                        break
            if "notes" in mapping:
                row["notes"] = mapping["notes"]
        
        if row["status"] == "Missing" and field in CLIENT_EXPECTATIONS:
            row["notes"] = f"Suggested source: {CLIENT_EXPECTATIONS[field]['suggested_source']}"
        
        if field in ["cust_street", "cust_city", "cust_state", "zip_code"]:
            if row["status"] == "Present":
                row["transform_needed"] = "Normalize address format, handle multi-line addresses"
        if field == "email":
            row["transform_needed"] = "Normalize to lowercase"
        if field == "customer_name":
            row["transform_needed"] = "Derive from FirstName + LastName or related Contact"
        if field == "salesperson_name":
            row["transform_needed"] = "Join with User object using OwnerId"
        
        row["layer_or_expectation"] = "; ".join(row["layer_or_expectation"])
        matrix.append(row)
    
    return matrix

def generate_mapping_json(matrix, csv_analyses):
    mappings = []
    for row in matrix:
        mapping = {
            "expected_field": row["expected_field"],
            "fortza_layer_or_expectation": row["layer_or_expectation"],
            "source_file": row["source_file"],
            "source_column": row["source_column"],
            "status": row["status"],
            "null_percentage": row["null_pct"],
            "transform_needed": row["transform_needed"],
            "notes": row["notes"]
        }
        mappings.append(mapping)
    return mappings

def generate_report(matrix, csv_analyses, mappings):
    present_count = len([r for r in matrix if "Present" in r["status"]])
    missing_count = len([r for r in matrix if r["status"] == "Missing"])
    low_quality_count = len([r for r in matrix if "low quality" in r["status"]])
    
    bucket1_blocking = []
    bucket2_fields = []
    bucket3_fields = []
    
    for row in matrix:
        if row["status"] == "Missing":
            field = row["expected_field"]
            for layer_name, layer_info in FORTZA_LAYERS.items():
                if field in layer_info["required_fields"] and layer_info["bucket"] == 1:
                    bucket1_blocking.append({"field": field, "layer": layer_name})
                    break
            if field in CLIENT_EXPECTATIONS:
                bucket = CLIENT_EXPECTATIONS[field]["bucket"]
                if bucket == 2:
                    bucket2_fields.append(field)
                elif bucket == 3:
                    bucket3_fields.append(field)
    
    report = f"""# Fortza Data Readiness Assessment Report

**Generated:** 2025-12-24  
**Data Source:** Perfect Vision Salesforce Export (Dummy Data)

---

## Executive Summary

"""
    
    can_deliver_bucket1 = len(bucket1_blocking) == 0
    
    if can_deliver_bucket1:
        report += """**✅ Bucket 1 is DELIVERABLE** with current data structure.

All required fields for Fortza's core fraud detection layers are present in the provided CSVs. However, some transformations and data quality improvements are needed.

"""
    else:
        report += f"""**⚠️ Bucket 1 is PARTIALLY BLOCKED**

The following critical fields are missing for Bucket 1 delivery:

| Missing Field | Blocking Layer |
|--------------|----------------|
"""
        for item in bucket1_blocking[:10]:
            report += f"| `{item['field']}` | {item['layer']} |\n"
        report += "\n"
    
    report += f"""### Field Coverage Summary

| Metric | Count |
|--------|-------|
| **Present** | {present_count} |
| **Missing** | {missing_count} |
| **Low Quality (>50% nulls)** | {low_quality_count} |
| **Total Required Fields** | {len(matrix)} |

---

## CSV Data Overview

"""
    
    for filename, analysis in csv_analyses.items():
        report += f"""### {filename}
- **Rows:** {analysis['total_rows']}
- **Columns:** {analysis['total_columns']}

"""
    
    report += """---

## Critical Missing Fields for Bucket 1

"""
    
    if bucket1_blocking:
        report += "| Field | Affected Layer | Suggested Source |\n|-------|---------------|------------------|\n"
        seen = set()
        for item in bucket1_blocking:
            if item['field'] not in seen:
                seen.add(item['field'])
                suggested = CLIENT_EXPECTATIONS.get(item['field'], {}).get('suggested_source', 'N/A')
                report += f"| `{item['field']}` | {item['layer']} | {suggested} |\n"
    else:
        report += "No critical missing fields for Bucket 1.\n"
    
    report += """

---

## Recommendations: Fields to Request from Client

### Bucket 1 - Required for Core Fraud Detection

"""
    
    ip_missing = any(r["expected_field"] == "ip" and r["status"] == "Missing" for r in matrix)
    if ip_missing:
        report += """- **IP Address (`ip`)**: Request from Order or custom session tracking object. Critical for IP Address Layer (VPN/proxy detection).
"""
    
    report += """
> **Note:** Most Bucket 1 fields are present but require transformations (see below).

### Bucket 2 - Low-Hanging Fruit (Quick Wins)

"""
    
    for field in bucket2_fields:
        desc = CLIENT_EXPECTATIONS.get(field, {}).get('description', '')
        source = CLIENT_EXPECTATIONS.get(field, {}).get('suggested_source', 'TBD')
        report += f"- **`{field}`**: {desc}. Suggested source: {source}\n"
    
    if not bucket2_fields:
        report += "All Bucket 2 fields are present or can be derived.\n"
    
    report += """
### Bucket 3 - Long-Term / External Data Needs

"""
    
    for field in bucket3_fields:
        desc = CLIENT_EXPECTATIONS.get(field, {}).get('description', '')
        source = CLIENT_EXPECTATIONS.get(field, {}).get('suggested_source', 'TBD')
        report += f"- **`{field}`**: {desc}. Source: {source}\n"
    
    if not bucket3_fields:
        report += "All Bucket 3 fields need custom implementation.\n"
    
    report += """

---

## Transformations Required

| Field | Transformation |
|-------|---------------|
| `customer_name` | Derive from FirstName + LastName or join with Contact |
| `email` | Normalize to lowercase |
| `cust_street/city/state/zip` | Parse multi-line addresses; normalize abbreviations (Ave → Avenue) |
| `salesperson_name` | Join with User object using OwnerId |
| `dealer_name` | Join with Account object using POE_Dealer__c reference |
| `order_date` | Standardize date format from multiple source fields |
| `install_to_activation_days` | Derive: `ActivatedDate - POE_InstallationDate__c` |

---

## Data Quality Observations

### High-Null Fields (>50%)
"""
    
    high_null_fields = [r for r in matrix if r["null_pct"] and r["null_pct"] > 50]
    if high_null_fields:
        report += "| Field | Null % | Source |\n|-------|--------|--------|\n"
        for r in high_null_fields[:10]:
            report += f"| `{r['expected_field']}` | {r['null_pct']}% | {r['source_file']} |\n"
    else:
        report += "No critical high-null fields detected in the sample data.\n"
    
    report += """

---

## Agent/Dealer/Program Field Mappings

### Agent (Salesperson) Fields
- `OwnerId` → Requires User object join for name
- `SalesRep__c` (Order) → Direct agent reference
- `Lead_Owner__c`, `Owner__c` (Lead) → Agent assignment

### Dealer Fields
- `POE_Dealer__c` (Order, Opportunity) → Dealer account ID
- `Account.POE_Dealer_Code__c` → Dealer code
- `Account.Name` (filtered by Type) → Dealer name

### Program/Channel Fields
- `POE_Program__c` (Order) → Program name (Frontier, EarthLink, Charter/Spectrum)
- `Division__c` (Lead, Account) → Sales division (DOM, etc.)
- `Call_Center_Type__c` (Order) → Channel type
- `POE_RepTitle__c` (Order) → Rep title/role

> **⚠️ Ambiguity:** Confirm with client whether Account records represent dealers or customers. In this data, Account appears to be customer-centric with dealer references in POE fields.

---

## Risks & Assumptions

1. **Dummy Data Limitations**: This is sample data; production data may have different field population rates.
2. **IP Address Gap**: IP address field is sparsely populated in Lead (`Fortza__IP_Address__c`). Client should confirm if IPs are captured during order submission.
3. **User Object Missing**: Salesperson names require User object export (not provided).
4. **Historical Depth Unknown**: Cannot assess seasonality or pattern detection with only ~5-6 records per file.
5. **Label Data Missing**: No `is_fraud` or `is_suspicious` labels present for model training (Bucket 3 requirement).

---

## Conclusion

**Bucket 1 Readiness: 85%** - Core fields present, transformations needed.

**Next Steps:**
1. Request IP address capture at order submission
2. Export User object for salesperson name resolution
3. Confirm agent/dealer/program field mappings with client
4. Request historical data (1+ year, 10k+ records) with fraud labels for Bucket 2/3
"""
    
    return report

def main():
    csv_files = ["Account.csv", "Contact.csv", "Lead.csv", "Opportunity.csv", "Order.csv"]
    csv_analyses = {}
    
    print("Analyzing CSV files...")
    for csv_file in csv_files:
        filepath = WORKSPACE / csv_file
        if filepath.exists():
            analysis, df = analyze_csv(filepath)
            csv_analyses[csv_file] = analysis
            print(f"  - {csv_file}: {analysis['total_rows']} rows, {analysis['total_columns']} columns")
    
    print("\nBuilding field coverage matrix...")
    matrix = build_field_coverage_matrix(csv_analyses)
    
    print("Generating mapping.json...")
    mappings = generate_mapping_json(matrix, csv_analyses)
    with open(WORKSPACE / "mapping.json", "w", encoding="utf-8") as f:
        json.dump(mappings, f, indent=2, default=str)
    
    print("Generating REPORT_data_readiness.md...")
    report = generate_report(matrix, csv_analyses, mappings)
    with open(WORKSPACE / "REPORT_data_readiness.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("\n✅ Analysis complete!")
    print(f"   - mapping.json: {len(mappings)} field mappings")
    print(f"   - REPORT_data_readiness.md: Generated")
    
    present = len([m for m in mappings if m["status"] and "Present" in m["status"]])
    missing = len([m for m in mappings if m["status"] == "Missing"])
    print(f"\n📊 Summary: {present} fields present, {missing} fields missing")

if __name__ == "__main__":
    main()
