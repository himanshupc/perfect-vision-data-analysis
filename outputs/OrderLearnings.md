# Order Object — Working Synthesis for Fortza Integration

## What Was Done

- A working data dictionary for the **Order** object was constructed using:
  - Column API names
  - Observed sample values only
- No official Salesforce or client-provided data dictionary was referenced.
- Field meanings were inferred strictly from:
  - Naming conventions
  - Data types implied by values
  - Repeated patterns across rows
- All interpretations are intentionally conservative and reviewable.

This synthesis reflects **observed evidence**, not business assumptions.

---

## Nature of the Order Object

- The Order object represents a **post-decision, post-commit transactional record**.
- It captures:
  - Financial commitments
  - Billing and shipping details
  - Fulfillment and installation timing
  - Pricing, discounts, margins, and totals
  - System and external orchestration state (pricing, validation, syncing)
- Compared to Opportunity, Order reflects **execution** rather than intent.

---

## Role of Order in the Salesforce Lifecycle

- Order is created **after Opportunity reaches a committed outcome** (e.g., Closed Won).
- It serves as the authoritative record for:
  - What was sold
  - At what price
  - Under what terms
  - With what fulfillment expectations
- Order bridges Salesforce CRM with:
  - Billing systems
  - Fulfillment / installation workflows
  - External pricing and provisioning engines (e.g., Vlocity / CPQ / partner systems)

---

## Relationship to Opportunity, Account, and Downstream Fulfillment

- **Opportunity**
  - Represents intent and negotiation
  - Order represents finalized execution
- **Account**
  - Order inherits customer identity, address, and ownership context
- **Contact**
  - Contact-level signals appear indirectly via email, phone, ownership, and channel
- **Downstream systems**
  - Installation scheduling
  - External pricing validation
  - Contract enforcement
  - Billing and invoicing

Order is the **handoff point** from sales to operations.

---

## Semantic Groupings Identified

### 1. Identity & Linkage

- Order Id
- OrderNumber
- AccountId
- OpportunityId
- OwnerId
- RecordTypeId
- Pricebook2Id
- vlocity_cmt__AccountId__c

Purpose:
- Cross-object traceability
- Ownership attribution
- Identity consistency checks

---

### 2. Financial Totals, Pricing, and Margins

- TotalAmount
- vlocity_cmt__OrderTotal__c
- vlocity_cmt__EffectiveOrderTotal__c
- vlocity_cmt__OneTimeTotal__c
- vlocity_cmt__OneTimeTotal2__c
- vlocity_cmt__RecurringTotal__c
- vlocity_cmt__RecurringTotal2__c
- vlocity_cmt__EffectiveRecurringTotal__c
- vlocity_cmt__EffectiveOneTimeTotal__c
- vlocity_cmt__UsageMarginTotal__c
- vlocity_cmt__OrderMarginTotal__c
- vlocity_cmt__RecurringMarginTotal__c
- vlocity_cmt__OneTimeMarginTotal__c

Purpose:
- Monetary commitment validation
- Internal consistency across pricing layers
- Detection of anomalous pricing structures

---

### 3. Discounts, Loyalty, and Incentives

- vlocity_cmt__TotalMonthlyDiscount__c
- vlocity_cmt__TotalOneTimeDiscount__c
- vlocity_cmt__OneTimeLoyaltyTotal__c
- vlocity_cmt__EffectiveOneTimeLoyaltyTotal__c

Purpose:
- Incentive abuse detection
- Excessive discounting patterns
- Loyalty misuse across accounts or channels

---

### 4. Billing and Shipping Information

- BillingStreet
- BillingCity
- BillingState
- BillingStateCode
- BillingPostalCode
- BillingCountry
- BillingCountryCode
- ShippingStreet
- ShippingCity
- ShippingState
- ShippingStateCode
- ShippingPostalCode
- ShippingCountry
- ShippingCountryCode
- vlocity_cmt__ShippingState__c
- vlocity_cmt__ShippingPostalCode__c

Purpose:
- Address consistency checks
- Billing vs shipping divergence
- Reuse of addresses across accounts/orders

---

### 5. Fulfillment, Installation, and Timing

- EffectiveDate
- POE_Early_Installation_Date__c
- POE_InstallationDate__c
- Pending_Installation__c
- Activated__c
- Disconnected__c
- DSL_Migration__c

Purpose:
- Fulfillment manipulation detection
- Deliberate activation/disconnection cycles
- Installation timing abuse

---

### 6. Status, Lifecycle, and Control Flags

- Status
- StatusCode
- Draft__c
- Canceled__c
- IsReductionOrder
- vlocity_cmt__OrderStatus__c
- vlocity_cmt__IsActiveOrderVersion__c
- vlocity_cmt__IsChangesAllowed__c
- vlocity_cmt__IsChangesAccepted__c
- vlocity_cmt__IsContractRequired__c
- vlocity_cmt__IsValidated__c
- vlocity_cmt__IsPriced__c
- vlocity_cmt__IsSyncing__c
- vlocity_cmt__ForceSupplementals__c

Purpose:
- Order lifecycle integrity
- Unauthorized modification detection
- Contract bypass signals

---

### 7. External Systems & Partner Context

- vlocity_cmt__ExternalPricingStatus__c
- vlocity_cmt__DeliveryMethod__c
- vlocity_cmt__DefaultCurrencyPaymentMode__c
- POE_Program__c
- POE_OrderId__c
- POE_OrderNumber__c
- POE_TransactionId__c
- POE_Dealer__c
- POE_Call_Order__c
- POE_Is_Shell_Order__c
- POE_isLocked__c

Purpose:
- External pricing failures
- Shell or placeholder order abuse
- Partner or dealer-driven anomalies

---

### 8. Channel, Ownership, and Origination

- vlocity_cmt__OriginatingChannel__c
- POE_RepTitle__c
- CreatedById
- Created_by_Brightspeed_API__c
- LastModifiedById
- CreatedDate
- LastModifiedDate
- SystemModstamp

Purpose:
- Channel-based fraud analysis
- API vs human-originated risk
- Ownership and timing correlations

---

## Columns of Particular Interest for Fortza

### Post-Commit Fraud Detection

- OrderTotal / EffectiveOrderTotal mismatches
- Repeated draft-to-active transitions
- Reduction orders following fulfillment

### Payment, Billing, and Invoicing Risk

- Discount totals vs margins
- Billing vs shipping divergence
- PaymentCalculated__c inconsistencies

### Fulfillment Manipulation or Abuse

- Pending installation loops
- Early installation date manipulation
- Activation/disconnection cycling

### Contractual and Cancellation Anomalies

- Canceled__c with active fulfillment signals
- IsContractRequired__c set false with high-value orders
- ChangesAllowed after submission-ready state

---

## What Was Deliberately Not Done

- No assumptions about:
  - Business rules
  - Approval workflows
  - Contract enforcement logic
  - Industry-specific semantics
- No inference of:
  - Fraud intent
  - Customer legitimacy
  - Policy compliance
- No normalization or deduplication across objects

All interpretations remain **hypotheses for client validation**.

---

## Key Takeaways

### How Order Differs from Opportunity and Earlier Funnel Objects

- Opportunity captures **intent and negotiation**
- Order captures **execution and financial commitment**
- Errors or abuse at Order level have **direct monetary impact**

---

### Strengths of Order Data for Fraud Detection

- Concrete monetary values
- Execution-stage timestamps
- External system integration states
- Fulfillment and billing coupling

### Limitations of Order Data

- Limited customer intent context
- Depends on upstream data quality
- May reflect downstream system errors rather than fraud

---

## Role of Order in Final Fortza Layer Design

- Order should anchor **post-commit and fulfillment risk layers**
- Acts as:
  - A confirmation layer for Opportunity-based signals
  - A trigger for downstream risk escalation
- Best used in combination with:
  - Opportunity velocity and discount patterns
  - Account stability and history
  - Contact identity consistency

---

## Contribution to Post-Commit Risk Scoring

- Detects:
  - Pricing abuse after deal closure
  - Fulfillment manipulation
  - Contractual bypass patterns
- Provides final validation before:
  - Billing
  - Installation
  - Revenue recognition

---

## Interaction with Other Objects

- **Account**: Long-term behavioral baselines
- **Contact**: Identity and channel consistency
- **Opportunity**: Pre-commit intent vs post-commit reality
- **Order**: Ground truth of what actually executed

Order is the **last and most financially sensitive checkpoint** in the Fortza risk model.

