# Contact Object – Working Synthesis for Fortza Integration

## 1. What Was Done

- The Salesforce **Contact** object was analyzed incrementally using screenshots provided by the client.
- Field meanings were inferred **only** from:
  - Column API names
  - Visible sample values
- No external Salesforce documentation, assumptions, or domain interpretations were applied.
- The output prior to this document was a CSV-ready working data dictionary for client validation.
- This document synthesizes that dictionary into higher-level semantic groupings for Fortza design.

---

## 2. Nature of the Contact Object

### 2.1 Role in Salesforce

- Contact represents an **individual person** associated with an Account.
- It is the primary carrier of:
  - Personal identity attributes
  - Communication channels and consent
  - Program, partner, and eligibility flags
  - Enrichment and third-party intelligence markers

### 2.2 Relationship to Account

- Account represents the **entity or organization**.
- Contact represents **people interacting on behalf of or within that entity**.
- Multiple Contacts may exist per Account, each with distinct behavior, status, and risk signals.
- In Salesforce, Contact is the **execution surface** for communication, outreach, and identity resolution.

---

## 3. Semantic Groupings Identified

### 3.1 Core Identity and Record Metadata

- Id  
- AccountId  
- CreatedById  
- CreatedDate  
- LastModifiedById  
- LastModifiedDate  
- SystemModstamp  
- IsDeleted  
- IsPersonAccount  

**Purpose**  
Defines record lifecycle, ownership, and linkage to Account-level entities.

---

### 3.2 Ownership and Internal Classification

- OwnerId  
- Owner__c  
- Principal_Owner__c  
- IsPriorityRecord  

**Purpose**  
Internal routing, prioritization, and ownership signals.

---

### 3.3 Contact Role, Employment, and Relationship Flags

- vlocity_cmt__IsEmployee__c  
- vlocity_cmt__IsPartner__c  
- vlocity_cmt__IsPersonAccount__c  
- POE_Point_Of_Contact__c  
- POE_Belongs_To_Partner__c  
- POE_Existing_Agent_Flag__c  
- SR_Resource__c  

**Purpose**  
Defines how the individual relates to the organization and partner ecosystem.

---

### 3.4 Address and Geographic Attributes

- MailingStreet  
- MailingCity  
- MailingState  
- MailingStateCode  
- MailingPostalCode  
- MailingCountry  
- MailingCountryCode  

**Purpose**  
Geographic anchoring of identity and communication context.

---

### 3.5 Communication Channels and Consent Controls

- Email  
- Fax  
- DoNotCall  
- Do_Not_Email__c  
- HasOptedOutOfEmail  
- HasOptedOutOfFax  
- SMS_Opt_Out__c  
- POE_SMS_Opt_In__c  
- POE_WS_Email__c  
- IsEmailBounced  
- pi_pardot_hard_bounced__c  

**Purpose**  
Consent, deliverability, and communication risk management.

---

### 3.6 Program, Eligibility, and Commercial Controls

- Add_to_Agreements__c  
- My_Dealer_Flag__c  
- Under_Contract__c  
- POE_Allow_DTV_Sell__c  
- POE_IsTmobileAllowed__c  
- POE_Enable_Trial_Period__c  
- Fortza_Auto_Pay__c  

**Purpose**  
Eligibility, monetization, and operational constraints tied to individuals.

---

### 3.7 Activity and Behavioral Proxies

- LastActivityDate  
- vlocity_cmt__DaysSinceLastContact__c  

**Purpose**  
Light-weight behavioral freshness indicators.

---

### 3.8 Enrichment and External Intelligence Signals

- salesintelio__Attempted_Enrichment__c  
- salesintelio__SalesIntel_Enriched__c  
- salesintelio__SalesIntel_Machine_Verified__c  
- salesintelio__SalesIntel_Up_to_Date__c  
- salesintelio__SalesIntel_Changed_Job__c  
- salesintelio__SalesIntel_Exported__c  
- pi_Needs_Score_Synced__c  

**Purpose**  
Third-party verification, freshness, and enrichment state.

---

### 3.9 Compliance, Risk, and Fraud Indicators

- POE_Blacklist__c  
- vlocity_cmt__HasFraud__c  
- vlocity_cmt__Authorized__c  

**Purpose**  
Explicit risk flags and compliance gating at the individual level.

---

## 4. Columns of Particular Interest for Fortza

### 4.1 Identity and Resolution

- Email  
- Mailing address fields  
- Title  
- AccountId  

Critical for person-level identity stitching and disambiguation.

---

### 4.2 Communication Risk and Consent

- IsEmailBounced  
- pi_pardot_hard_bounced__c  
- DoNotCall  
- HasOptedOutOfEmail  
- SMS_Opt_Out__c  

High signal for abuse, spam risk, and regulatory compliance.

---

### 4.3 Fraud and Compliance Indicators

- POE_Blacklist__c  
- vlocity_cmt__HasFraud__c  
- vlocity_cmt__Authorized__c  

Direct inputs into rule-based and ML-driven fraud layers.

---

### 4.4 Enrichment Quality and Freshness

- salesintelio__SalesIntel_Machine_Verified__c  
- salesintelio__SalesIntel_Up_to_Date__c  
- salesintelio__SalesIntel_Changed_Job__c  

Signals data confidence, decay, and identity drift.

---

### 4.5 Behavioral Proxies

- LastActivityDate  
- vlocity_cmt__DaysSinceLastContact__c  

Low-granularity but useful for recency-based risk weighting.

---

## 5. What Was Deliberately Not Done

- No semantic expansion of acronyms (e.g., POE, FSL, Chuzo, LearnUpon).
- No inference of business meaning beyond field names and values.
- No assumptions about workflow, automation, or enforcement logic.
- No normalization or deduplication logic was proposed.
- No cross-object joins were evaluated at this stage.

---

## 6. Key Takeaways

### 6.1 Contact vs Account Signal Quality

- Account:
  - Structural
  - Stable
  - Organizational
- Contact:
  - Volatile
  - Individual-centric
  - Rich in consent, enrichment, and risk signals

Contact data carries **higher noise but higher fraud relevance**.

---

### 6.2 Role of Contact in Fortza Layer Design

- Primary surface for:
  - Identity verification
  - Communication abuse detection
  - Consent and compliance enforcement
  - Individual-level fraud flags
- Enables **per-person risk scoring**, even within the same Account.

---

### 6.3 Complementarity with Account-Level Signals

- Account provides context and baseline trust.
- Contact provides execution-level risk and behavior.
- Fortza layers should:
  - Anchor trust at Account level
  - Modulate risk dynamically at Contact level

---

## 7. Forward Use

- This synthesis will be used in:
  - Cross-object feature normalization
  - Fortza custom layer proposal
  - Signal weighting between Account and Contact
- Contact fields will primarily feed:
  - Identity Risk Layer
  - Communication Abuse Layer
  - Compliance & Consent Layer
  - Enrichment Confidence Layer

---

End of document.
