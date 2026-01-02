# Account Object – Synthesis Summary

## What was done

We analyzed the **Account** standard Salesforce object containing several hundred columns without an existing data dictionary.

Each column was reviewed **only using its API name and observed sample values**, and documented into a **working / assumed data dictionary** suitable for client validation.

The goal was not perfect semantic accuracy, but to:

- Make the dataset cognitively manageable
- Identify meaningful signal surfaces
- Prepare for cross-object Fortza layer design

---

## Key observations

### 1. Nature of the data

The Account object is **not just a company profile**.  
It functions as a central **hub object** that aggregates multiple dimensions:

- Identity and classification
- Compliance and consent
- Partner / dealer eligibility
- Service footprint (Frontier, DIRECTV, Spectrum, Optimum, Windstream, etc.)
- Enrichment and data quality metadata
- Fraud and velocity intelligence (Vlocity / CMT)

---

### 2. Semantic groupings identified

Hundreds of columns naturally collapsed into **~9 coherent semantic groups**:

#### 1. Core Salesforce Metadata
- `Id`, `CreatedDate`, `LastModifiedDate`, `OwnerId`, `RecordTypeId`, `IsDeleted`
- Used for lineage, auditability, ownership, and lifecycle analysis

#### 2. Identity & Classification
- `Industry`, `Type`, `IsPartner`, `IsPersonAccount`
- Used for segmentation (partner vs customer vs prospect)

#### 3. Address & Geography
- `Billing*`, `Shipping*`, `Territory__c`, `Region__c`
- Useful for geo-risk, routing, and fulfillment constraints

#### 4. Lifecycle & Onboarding
- `Onboarding_Status__c`, `Onboarding_Denied__c`, `On_Probation__c`
- Strong indicators of account maturity and risk phase

#### 5. Compliance & Consent
- `NDA_Activated_Count__c`, `Do_Not_Email__pc`, `SMS_Opt_Out__pc`, consent flags
- Regulatory and communication constraints

#### 6. Service Footprint & Entitlements
- `Frontier_*`, `DTV_*`, `Spectrum_Only__c`, `Optimum_Only__c`, `Windstream_Activated__c`
- Indicates which services the account is allowed or enabled to sell

#### 7. Partner / POE Eligibility & Gating
- `POE_Blacklist__pc`, `POE_Allow_DTV_Sell__pc`, `POE_Require_TPV__c`
- Binary allow/deny controls, ideal for rule-based decision layers

#### 8. Enrichment & Data Quality
- `salesintelio_*` (Enriched, Verified, Up_to_Date)
- Meta-signals affecting confidence and trustworthiness of data

#### 9. Fraud & Velocity Intelligence (High Value)
- `vlocity_cmt__HasFraud__c / __pc`
- `vlocity_cmt__DaysSinceLastContact__pc`
- Disclosure completion, authorization, activity status  
- ⚠️ Requires careful handling to avoid label leakage

---

## Columns of particular interest for Fortza

The following fields stood out as structurally important or high-signal:

- `vlocity_cmt__HasFraud__c`, `vlocity_cmt__HasFraud__pc`
- `Onboarding_Status__c`, `On_Probation__c`
- `NumberOfEmployees`
- `NDA_Activated_Count__c`
- `POE_Blacklist__pc`
- `POE_Allow_*` (service entitlement flags)
- `salesintelio_*_Verified`, `salesintelio_*_Up_to_Date`
- Ownership and lifecycle timestamps

These are **not all scoring inputs**, but they strongly influence:

- Routing
- Overrides
- Confidence weighting
- Explainability

---

## What was deliberately not done

- No guessing about internal business workflows
- No scoring logic applied
- No assumption that all fields are useful
- No Fortza layer finalized in isolation

---

## Key takeaway

The Account object initially appeared overwhelming (~700+ columns), but after structured analysis it became:

> **9 coherent signal surfaces instead of hundreds of disconnected fields**

This makes it realistic to:

- Design **1–2 custom Fortza layers**
- Explain decisions clearly to the client
- Avoid rework when other objects (Lead, Contact, Opportunity, Order) are added

---

## Next step

Repeat the same lightweight dictionary and grouping exercise for:

- Lead
- Contact
- Opportunity
- Order

Then perform a **single cross-object synthesis** to define:
- Final feature groups
- Custom Fortza layer boundaries
- Client-facing integration narrative
