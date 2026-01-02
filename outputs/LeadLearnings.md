# Lead Object – Working Synthesis (Preliminary)

## 1. What Was Done

- The Salesforce **Lead** object was analyzed using:
  - Column API names
  - Observed sample values from provided screenshots
- No formal data dictionary or schema documentation was available.
- All interpretations were derived strictly from:
  - Field names
  - Data types implied by values (boolean, date, string, numeric)
  - Repetition and variation across sample rows
- No external Salesforce assumptions, business logic, or industry defaults were applied.

This document represents a **working, reviewable synthesis** intended for client validation prior to downstream modeling and Fortza layer design.

---

## 2. Nature of the Lead Object

- The Lead object represents **pre-conversion entities** in Salesforce.
- Leads exist **before**:
  - Account creation
  - Contact creation
  - Opportunity linkage
- Leads typically capture:
  - Early inbound or outbound interest
  - Marketing-driven records
  - Incomplete or unverified identity and firmographic data

Structurally, Leads act as a **staging layer** between raw inbound signals and validated CRM entities.

---

## 3. Role of Lead in the Salesforce Lifecycle

- Entry point for:
  - Marketing campaigns
  - Trade shows
  - Website forms
  - Referrals
  - Data enrichment tools
- Leads may:
  - Be converted into Account + Contact
  - Be disqualified
  - Remain inactive or nurtured

### Structural Differences vs Account and Contact

- Lead data is:
  - Less stable
  - More volatile
  - More incomplete
- Leads combine:
  - Individual-level attributes (email, phone, title)
  - Organization-level attributes (industry, employees)
  - Channel and enrichment metadata
- Many Lead fields are **transient**, disappearing or transforming at conversion.

---

## 4. Semantic Groupings Identified

Lead fields naturally collapse into the following feature groups:

### 4.1 Identity & Contact Signals
- Email
- Phone
- MobilePhone
- Salutation
- Title
- Street, City, StateCode, PostalCode, Country, CountryCode

Focus: **who is claiming interest and how reachable they are**

---

### 4.2 Firmographic & Organizational Context
- Company
- Industry
- NumberOfEmployees
- Division__c
- Region__c
- Territory__c

Focus: **claimed organizational context at time of lead creation**

---

### 4.3 Lifecycle & Status Signals
- Status
- IsConverted
- IsDeleted
- IsPriorityRecord
- IsUnreadByOwner
- QualifiedbyDefault__c
- Rating
- LastActivityDate
- LastTransferDate

Focus: **lead maturity, handling velocity, and internal prioritization**

---

### 4.4 Source & Channel Attribution
- LeadSource
- Website
- Trade show / referral / advertisement indicators (via LeadSource values)

Focus: **origin trust, acquisition channel quality, and funnel entry point**

---

### 4.5 Communication & Consent Flags
- DoNotCall
- Do_Not_Email__c
- HasOptedOutOfEmail
- HasOptedOutOfFax

Focus: **contactability constraints and compliance context**

---

### 4.6 Enrichment & External Intelligence
- salesintelio__Attempted_Enrichment__c
- salesintelio__SalesIntel_Enriched__c
- salesintelio__SalesIntel_Up_to_Date__c
- salesintelio__SalesIntel_Changed_Job__c
- salesintelio__SalesIntel_Machine_Verified__c
- salesintelio__SalesIntel_Exported__c
- pi_Needs_Score_Synced__c
- pi_pardot_hard_bounced__c

Focus: **data freshness, third-party verification, and signal amplification**

---

### 4.7 Product / Capability Interest Signals
- Wireless__c
- Satellite_Installation__c
- Structured_Cabling__c
- Small_Cell_5G_Solutions__c
- Site_Testing_Tools__c
- Safety_PPE__c
- Public_Safety_Communication__c
- Macrocell__c
- Microwave__c
- Reinforcement_Kits__c
- Rigging_Components_Products__c

Focus: **expressed or inferred interest in specific offerings**

---

### 4.8 System, Ownership & Audit Metadata
- Id
- OwnerId
- Lead_Owner__c
- CreatedById
- CreatedDate
- LastModifiedById
- LastModifiedDate
- SystemModstamp
- DB_Created_Date_without_Time__c
- DB_Lead_Age__c

Focus: **temporal, operational, and ownership lineage**

---

## 5. Columns of Particular Interest for Fortza

### 5.1 Early Fraud Detection
- Email
- Phone / MobilePhone
- PostalCode / StateCode
- pi_pardot_hard_bounced__c
- salesintelio__SalesIntel_Machine_Verified__c
- DB_Lead_Age__c

Signals of identity instability, invalid contact paths, or synthetic submissions.

---

### 5.2 Intent Assessment
- Rating
- Status
- LastActivityDate
- Product interest flags (e.g., Wireless__c, Small_Cell_5G_Solutions__c)
- QualifiedbyDefault__c

Used to differentiate genuine interest from low-effort or automated leads.

---

### 5.3 Channel / Source Trust
- LeadSource
- Website
- salesintelio__Attempted_Enrichment__c
- salesintelio__SalesIntel_Enriched__c

Helps weight trustworthiness based on acquisition path and enrichment success.

---

### 5.4 Velocity & Duplication Risk
- DB_Lead_Age__c
- CreatedDate
- SystemModstamp
- IsUnreadByOwner
- Email + Phone reuse patterns (cross-object later)

Critical for detecting rapid lead flooding, replay attacks, or campaign abuse.

---

## 6. What Was Deliberately Not Done

- No assumptions were made about:
  - Salesforce standard semantics beyond field names
  - Lead conversion mappings
  - Business rules or validation logic
  - Meaning of coded values beyond what was observable
- No inferred relationships were created between:
  - Leads and Accounts
  - Leads and Contacts
- No enrichment values were treated as authoritative or correct by default.

All interpretations remain **hypotheses pending client validation**.

---

## 7. Key Takeaways

### Lead vs Account and Contact

- Lead data is:
  - Noisier
  - Less durable
  - More behaviorally rich at creation time
- Accounts emphasize **organizational stability**
- Contacts emphasize **verified individual identity**
- Leads emphasize **intent, source, and timing**

---

### Strengths of Lead Data
- Earliest visibility into inbound behavior
- High sensitivity to automation and abuse
- Rich channel and enrichment metadata
- Useful for preemptive risk scoring

### Limitations of Lead Data
- High false-positive risk
- Frequent data incompleteness
- Volatile lifecycle (conversion or deletion)
- Mixed individual and organizational semantics

---

## 8. Role of Lead in Final Fortza Layer Design

- Lead data should power **early-stage Fortza layers**, such as:
  - Pre-conversion fraud screening
  - Inbound trust scoring
  - Source-quality weighting
  - Velocity and duplication detection
- Lead-derived signals should:
  - Decay or be re-weighted post-conversion
  - Be reconciled with Account and Contact truth once available
- Leads serve as the **first risk checkpoint**, not the final authority.

---

## 9. Summary

The Lead object is best treated as a **high-signal, low-confidence surface**.  
Its value lies in **timing, intent, and anomalies**, not long-term truth.

In Fortza, Leads should:
- Trigger early warnings
- Influence conversion gating
- Inform downstream trust propagation
- Provide context for later Account and Contact validation

This synthesis is intended as a foundational input for cross-object feature grouping and custom Fortza layer construction.
