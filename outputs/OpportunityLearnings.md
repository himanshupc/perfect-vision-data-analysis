# Opportunity Object — Working Synthesis

## 1. What Was Done

- A working data dictionary for the **Opportunity** object was constructed using:
  - Column API names
  - Observed sample values from client-provided (dummy) data
- No pre-existing data dictionary or business documentation was used.
- Field meaning was inferred strictly from:
  - Naming conventions
  - Data types
  - Repeated observable values (boolean, numeric, categorical, timestamps)
- Descriptions were intentionally kept neutral and reviewable to support client validation before downstream modeling.

---

## 2. Nature of the Opportunity Object

- Opportunity represents a **commercial transaction in progress**.
- It is the system’s primary construct for:
  - Deal tracking
  - Revenue forecasting
  - Sales pipeline management
- Opportunity is **transactional and temporal**, unlike Account (entity) or Contact (identity).

---

## 3. Role of Opportunity in the Salesforce Lifecycle

- Opportunity sits **between Lead conversion and closed revenue**.
- Typical lifecycle positioning:
  - Lead → (converted) → Account / Contact
  - Opportunity created to track a potential sale
  - Opportunity progresses through stages until closed (won/lost)
- Opportunity reflects **sales execution behavior**, not just customer attributes.

---

## 4. Relationship to Other Core Objects

### Relationship to Account
- Each Opportunity is linked to a single Account via `AccountId`.
- Account provides:
  - Organizational context
  - Historical trust and tenure
- Opportunity provides:
  - Transaction-specific intent and value

### Relationship to Contact
- Contacts may influence or participate in an Opportunity.
- Contact-level identity signals contextualize Opportunity behavior.
- Opportunity itself does not store personal identity data directly.

### Relationship to Lead
- Opportunity typically originates after Lead qualification.
- Lead captures early intent; Opportunity captures **committed commercial intent**.
- Opportunity data reflects downstream validation, approvals, and financial structuring.

---

## 5. Semantic Groupings Identified

### 5.1 Ownership, Creation, and Governance
- OwnerId
- CreatedById
- CreatedDate
- LastModifiedById
- LastModifiedDate
- SystemModstamp
- Created_by_VPN_User__c
- IsPrivate
- IsDeleted

Signals related to:
- Who initiated and controls the deal
- Change frequency and audit trail

---

### 5.2 Deal Stage, Status, and Progression
- IsClosed
- IsWon
- ForecastCategory
- Opportunity_Paperwork_Status__c
- LastStageChangeDate
- HasOpenActivity
- HasOverdueTask
- HasOpportunityLineItem
- vlocity_cmt__ValidationStatus__c

Signals related to:
- Pipeline advancement
- Stalling or abnormal stage transitions
- Process completeness

---

### 5.3 Timing and Velocity
- CloseDate
- CreatedDate
- LastStageChangeDate
- Modified_Over_60_days__c
- Fiscal
- FiscalQuarter
- FiscalYear

Signals related to:
- Deal duration
- Velocity anomalies
- Backdated or rushed opportunities

---

### 5.4 Financial Value and Commercial Structure (Vlocity / CMT)
- vlocity_cmt__OpportunityTotal__c
- vlocity_cmt__EffectiveOpportunityTotal__c
- vlocity_cmt__RecurringTotal__c
- vlocity_cmt__OneTimeTotal__c
- vlocity_cmt__EffectiveRecurringTotal__c
- vlocity_cmt__EffectiveOneTimeTotal__c
- vlocity_cmt__EffectiveUsagePriceTotal__c
- vlocity_cmt__EffectiveUsageCostTotal__c
- vlocity_cmt__OpportunityMarginTotal__c
- vlocity_cmt__RecurringMarginTotal__c
- vlocity_cmt__UsageMarginTotal__c
- Probability

Signals related to:
- Deal size
- Margin structure
- Pricing consistency
- Risk exposure

---

### 5.5 Payment, Credit, and Compliance Indicators
- AutoPay__c
- Fortza_Auto_Pay__c
- Full_Credit_Check__c
- POE_CreditFreeze__c
- POE_SSN_Agreement__c
- Ebill_Registration__c
- Documents_Ready__c
- vlocity_cmt__IsContractRequired__c

Signals related to:
- Financial readiness
- Credit risk posture
- Compliance gating

---

### 5.6 Channel, Source, and Origination
- Click2Create_Flag__c
- POE_Clicker_Origin__c
- Inside_Recruiter__c
- Opportunity_Dealer_Office__c
- POE_Dealer__c
- POE_My_Dealer_Flag__c
- Program_Division__c
- RecordTypeId

Signals related to:
- Deal origination path
- Channel risk concentration
- Automation vs human creation

---

### 5.7 Fraud, Exception, and Observation Flags
- POE_FraudObservation__c
- Frontier_911_Terms_Sent__c
- ROI_Analysis_Completed__c
- POE_New_Product_Opportunity__c
- POE_Cross_Sale__c
- POE_Current_VoIP__c

Signals related to:
- Manual review
- Exceptions
- Product or pricing irregularities

---

### 5.8 Enrichment and External Augmentation
- salesintelio__Attempted_Enrichment__c
- salesintelio__SalesIntel_Enriched__c
- salesintelio__SalesIntel_Exported__c
- salesintelio__SalesIntel_Up_to_Date__c

Signals related to:
- Data completeness
- External verification

---

### 5.9 Geographic and Market Context
- Account_Territory__c
- Maps_Country__c
- Maps_PostalCode__c
- Region__c
- vlocity_cmt__AccountRecordType__c
- vlocity_cmt__DefaultCurrencyPaymentMode__c

Signals related to:
- Regional risk
- Market segmentation

---

## 6. Columns of Particular Interest for Fortza

### Deal Legitimacy
- Created_by_VPN_User__c
- Click2Create_Flag__c
- Inside_Recruiter__c
- POE_FraudObservation__c

### Velocity and Stage Progression Anomalies
- CreatedDate
- LastStageChangeDate
- CloseDate
- Modified_Over_60_days__c
- IsClosed / IsWon

### Amount, Discount, and Financial Risk
- vlocity_cmt__OpportunityTotal__c
- vlocity_cmt__EffectiveOpportunityTotal__c
- vlocity_cmt__OpportunityMarginTotal__c
- Probability

### Approval and Exception Patterns
- Documents_Ready__c
- Opportunity_Paperwork_Status__c
- Full_Credit_Check__c
- POE_CreditFreeze__c
- vlocity_cmt__ValidationStatus__c

---

## 7. What Was Deliberately Not Done

- No assumptions were made about:
  - Business rules
  - Approval thresholds
  - Sales methodology semantics
  - Fraud definitions
- No inference was made beyond observable names and values.
- No cross-object joins or historical aggregation was applied at this stage.

---

## 8. Key Takeaways

### How Opportunity Differs from Account, Contact, and Lead
- Account: static organizational identity
- Contact: personal and identity-level signals
- Lead: early intent and acquisition signals
- Opportunity: **transactional, monetary, and execution-driven signals**

### Strengths for Fraud Detection
- Rich timing and progression data
- Explicit financial totals and margins
- Multiple approval, compliance, and exception flags

### Limitations
- Limited direct identity attributes
- Heavily process-dependent
- Some financial fields are system-calculated and opaque

---

## 9. Role of Opportunity in Fortza Layer Design

- Opportunity is a **mid-funnel to transactional risk layer**.
- Primary contributions:
  - Deal-level anomaly detection
  - Velocity and behavior-based risk scoring
  - Financial exposure assessment
- Opportunity signals should:
  - Interact with Account trust history
  - Be contextualized by Contact identity quality
  - Be seeded by Lead-origin intent signals

Opportunity acts as the **execution checkpoint** where intent becomes money, making it a critical layer for Fortza’s fraud and risk detection architecture.
