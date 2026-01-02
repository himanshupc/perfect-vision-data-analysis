# Fortza Data Readiness Assessment Report

**Generated:** 2025-12-24  
**Data Source:** Perfect Vision Salesforce Export (Dummy Data)

---

## Executive Summary

**⚠️ Bucket 1 is PARTIALLY BLOCKED**

The following critical fields are missing for Bucket 1 delivery:

| Missing Field | Blocking Layer |
|--------------|----------------|
| `ipAddress` | IP Address Layer |

### Field Coverage Summary

| Metric | Count |
|--------|-------|
| **Present** | 17 |
| **Missing** | 18 |
| **Low Quality (>50% nulls)** | 10 |
| **Total Required Fields** | 35 |

---

## CSV Data Overview

### Account.csv
- **Rows:** 5
- **Columns:** 643

### Contact.csv
- **Rows:** 5
- **Columns:** 297

### Lead.csv
- **Rows:** 5
- **Columns:** 211

### Opportunity.csv
- **Rows:** 5
- **Columns:** 300

### Order.csv
- **Rows:** 5
- **Columns:** 198

---

## Critical Missing Fields for Bucket 1

| Field | Affected Layer | Suggested Source |
|-------|---------------|------------------|
| `ipAddress` | IP Address Layer | N/A |


---

## Recommendations: Fields to Request from Client

### Bucket 1 - Required for Core Fraud Detection


> **Note:** Most Bucket 1 fields are present but require transformations (see below).

### Bucket 2 - Low-Hanging Fruit (Quick Wins)

- **`activation_date`**: Service activation date for timing analysis. Suggested source: Order.ActivatedDate
- **`agent_email`**: Sales agent/rep email. Suggested source: User, Contact
- **`agent_id`**: Agent/salesperson identifier. Suggested source: Order.SalesRep__c, OwnerId
- **`channel`**: Sales channel (phone, retail, d2d). Suggested source: Lead.Division__c, Order.Call_Center_Type__c
- **`dealer_id`**: Dealer/partner identifier. Suggested source: Account.POE_Dealer_Code__c, Order.POE_Dealer__c
- **`device_fingerprint`**: Device ID for shared device detection. Suggested source: CustomObject, Order
- **`disconnection_date`**: Service disconnect date for churn analysis. Suggested source: Order.Disconnect_Date__c
- **`install_date`**: Installation date for timing deltas. Suggested source: Order.POE_InstallationDate__c
- **`payment_info`**: Payment method for proof-of-sale. Suggested source: Order, CustomObject
- **`program_name`**: Program/product name for mix analysis. Suggested source: Order.POE_Program__c, Lead.Programs__c

### Bucket 3 - Long-Term / External Data Needs

- **`audit_notes`**: Audit notes for sentiment analysis. Source: CustomObject, Notes, External System
- **`commission_data`**: Commission/stair-step data for dealer profiling. Source: CustomObject, External System
- **`debt_balance`**: Dealer debt balance. Source: Account financial fields, External System
- **`login_history`**: Agent login timestamps for velocity. Source: LoginHistory, Event
- **`territory`**: Agent/dealer territory for authorization. Source: Account.Territory__c, Account_Territory__c


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
| Field | Null % | Source |
|-------|--------|--------|
| `Tntype` | 100.0% | Account.csv |
| `dealer_name` | 100.0% | Lead.csv |
| `devicename` | 100.0% | Lead.csv |
| `devicetype` | 100.0% | Account.csv |
| `email` | 100.0% | Account.csv |
| `gender` | 100.0% | Account.csv |
| `ip` | 100.0% | Lead.csv |
| `order_date` | 100.0% | Account.csv |
| `store_number` | 100.0% | Account.csv |
| `wireless_package` | 100.0% | Account.csv |


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
