# Fortress Fraud Detection Layers Documentation

This document provides a comprehensive overview of all fraud detection layers implemented in the Fortress system. Each layer analyzes different aspects of transaction data to identify potential fraudulent activity.

---

## Table of Contents

1. [Historical Data Layers](#historical-data-layers)
2. [Address Validation Layers](#address-validation-layers)
3. [Identity Verification Layers](#identity-verification-layers)
4. [Geolocation Layers](#geolocation-layers)
5. [Machine Learning Layers](#machine-learning-layers)
6. [AI & LLM Layers](#ai--llm-layers)
7. [Network Security Layers](#network-security-layers)
8. [Database Verification Layers](#database-verification-layers)

---

## Historical Data Layers

### 1. Permanent Memory User Details
**Route:** `/permanent_memory_user_details` (Regular), `/api/salesforce/permanent_memory_user_details` (Salesforce)

**Layer Name:** Historical Customer Data (Deterministic)

**Purpose:** Checks if a customer has been previously flagged for suspicious activity in the system's historical database.

**Required Fields:**
- `customer_name`
- `email`

**How It Works:**
1. Queries the internal `database_layer` table for matching customer name or email
2. Checks if either the name or email has been associated with past fraud
3. Returns different scores based on:
   - **No match found (score: 0.05-0.15)**: Customer has no fraud history
   - **Partial match (score: 0.91-0.99)**: Either name or email flagged previously
   - **Full match (score: 0.91-0.99)**: Both name and email associated with past fraud

**Data Source:** Internal PostgreSQL database (deterministic lookup)

**Score Range:** 0.05-0.99

---

### 2. Permanent Memory Geolocation
**Route:** `/permanent_memory_geolocation` (Regular), `/api/salesforce/permanent_memory_geolocation` (Salesforce)

**Layer Name:** Geolocation Hotspot (Deterministic)

**Purpose:** Verifies if a specific address has been associated with fraudulent activity in the past.

**Required Fields:**
- `cust_street`
- `cust_city`
- `cust_state`
- `zip_code`

**How It Works:**
1. Performs database lookup for the complete address
2. If complete address not found, checks individual components (street, city, state, zipcode)
3. Identifies which specific components have fraud associations
4. Returns risk assessment based on matches

**Data Source:** Internal PostgreSQL database (deterministic lookup)

**Score Range:** 0.05-0.99

---

## Address Validation Layers

### 3. Google Address Validation
**Route:** `/google_address_validation` (Regular), `/api/salesforce/google_address_validation` (Salesforce)

**Layer Name:** Address validation (Deterministic)

**Purpose:** Validates the authenticity and completeness of physical addresses using Google's Address Validation API.

**Required Fields:**
- `cust_street`
- `cust_city`
- `cust_state`
- `zip_code`

**How It Works:**
1. Sends address data to Google Address Validation API
2. Analyzes the API response for unconfirmed components
3. Calculates fraud score based on number of unconfirmed components:
   - **0 unconfirmed (score: 0.05-0.15)**: Fully validated address
   - **1 unconfirmed (score: 0.46-0.55)**: Partially validated address
   - **2+ unconfirmed (score: 0.91-0.99)**: Invalid or suspicious address

**External API:** Google Address Validation API (`https://addressvalidation.googleapis.com/v1:validateAddress`)

**Score Range:** 0.05-0.99

---

### 4. Smarty Address Validation
**Route:** `/smarty_address_validation` (Regular), `/api/salesforce/smarty_address_validation` (Salesforce)

**Layer Name:** Address Validation

**Purpose:** Alternative address validation service for verifying physical addresses (Note: Implementation details suggest this may use SmartyStreets or similar service).

**Required Fields:**
- `cust_street`
- `cust_city`
- `cust_state`
- `zip_code`

**How It Works:**
Similar to Google Address Validation, this layer validates addresses using an alternative service provider for redundancy and cross-validation.

**Score Range:** 0.05-0.99

---

## Identity Verification Layers

### 5. AI Prompt Layer (Identity Signal)
**Route:** `/ai_prompt_layer` (Regular), `/api/salesforce/ai_prompt_layer` (Salesforce)

**Layer Name:** Identity Signal

**Purpose:** Uses advanced LLM (GPT-4o-mini) to analyze customer identity data for inconsistencies and fraud patterns.

**Required Fields:**
- `customer_name`
- `email`
- `cust_street`
- `gender`
- `zip_code`
- `cust_city`

**How It Works:**
1. First checks content using OpenAI Moderation API to filter inappropriate input
2. Constructs detailed prompt asking AI to analyze:
   - Inconsistencies in customer information
   - Unusual patterns in transaction details
   - Mismatch between name, email, and gender
   - Geographic inconsistencies (zipcode, address, city)
   - Red flags in email address or contact information
3. GPT-4o-mini provides risk classification (Low/Medium/High) with justification
4. Score mapping:
   - **Low (score: 0.05-0.15)**: Legitimate customer data
   - **Medium (score: 0.46-0.55)**: Some suspicious patterns
   - **High (score: 0.91-0.99)**: High fraud risk

**External API:**
- OpenAI Moderation API (`https://api.openai.com/v1/moderations`)
- OpenAI Chat Completions API (`https://api.openai.com/v1/chat/completions`)

**Model:** GPT-4o-mini with JSON response format

**Score Range:** 0.05-0.99

---

### 6. Gilbert Layer (Domain Validation)
**Route:** `/gilbert_layer` (Regular), `/api/salesforce/gilbert_layer` (Salesforce)

**Layer Name:** Domain Validation

**Purpose:** Comprehensive email validation combining email verification services with AI-powered fraud detection.

**Required Fields:**
- `email`
- `customer_name`

**How It Works:**
1. **Email Validation Phase:**
   - Uses ZeroBounce API to validate email address
   - Retrieves detailed information:
     - Email validation status (valid/invalid)
     - Sub-status details
     - Free vs paid email provider
     - Domain information and age
     - SMTP provider details
     - MX record information

2. **AI Analysis Phase:**
   - Sends email validation data to Google Gemini 2.5 Flash
   - AI evaluates fraud indicators:
     - Gibberish or random letter patterns
     - Famous figures or celebrity names in email
     - Name matching (email should contain parts of user's name)
     - Suspicious domain names (sports teams, celebrities, organizations)
     - Domain status and validation results
   - Returns fraud score with detailed reasoning

**External APIs:**
- ZeroBounce API (email validation service)
- Google Gemini 2.5 Flash API (`https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent`)

**Score Range:** 0.0-1.0

**Special Cases:**
- Famous figures in email: Automatic high fraud score (0.90-0.99)
- No name matching: Flagged as potentially fraudulent

---

### 7. Word Cloud Name Verification
**Route:** `/word_cloud_name_verification` (Regular), `/api/salesforce/word_cloud_name_verification` (Salesforce)

**Layer Name:** Name Recognition

**Purpose:** Analyzes customer names for fraud patterns using machine learning-based name recognition.

**Required Fields:**
- `customer_name`

**How It Works:**
1. Sends customer name to external API endpoint
2. API analyzes name patterns against known fraud patterns
3. Returns fraud status (0 = safe, 1 = suspicious)
4. Score mapping:
   - **Fraud status 0 (score: 0.05-0.15)**: Normal name pattern
   - **Fraud status 1 (score: 0.91-0.99)**: Suspicious name pattern

**External API:** `https://api.projectalphabet.ai/word_cloud_name`

**Score Range:** 0.05-0.99

---

### 8. Word Cloud Email Verification
**Route:** `/word_cloud_email_verification` (Regular), `/api/salesforce/word_cloud_email_verification` (Salesforce)

**Layer Name:** Email Recognition

**Purpose:** Detects fraud patterns in email addresses using pattern recognition algorithms.

**Required Fields:**
- `email`

**How It Works:**
1. Submits email address to external API
2. API analyzes email patterns for fraud indicators
3. Returns fraud status (0 = safe, 1 = suspicious)
4. Score calculation:
   - **Fraud status 0 (score: 0.05-0.15)**: Normal email pattern
   - **Fraud status 1 (score: 0.91-0.99)**: Suspicious email pattern

**External API:** `https://api.projectalphabet.ai/word_cloud_email`

**Score Range:** 0.05-0.99

---

## Geolocation Layers

### 9. Geolocation Hotspot Layer
**Route:** `/geolocation_hotspot_layer` (Regular), `/api/salesforce/geolocation_hotspot_layer` (Salesforce)

**Layer Name:** Zip Code Proximity

**Purpose:** Identifies geographic fraud hotspots by analyzing fraud frequency in specific zip codes.

**Required Fields:**
- `zip_code`

**How It Works:**
1. Queries external API for fraud count in the given zip code
2. Analyzes historical fraud frequency in that geographic area
3. Risk assessment based on fraud count:
   - **≤2 fraud cases (score: 0.05-0.15)**: Low risk area
   - **3 fraud cases (score: 0.46-0.55)**: Moderate risk area
   - **>3 fraud cases (score: 0.91-0.99)**: High risk fraud hotspot

**External API:** `https://api.projectalphabet.ai/geolocation_hotspot_layer`

**Score Range:** 0.05-0.99

**Use Case:** Helps identify areas with concentrated fraudulent activity, useful for location-based risk assessment.

---

## Machine Learning Layers

### 10. Anomaly Layer
**Route:** `/anomaly_layer` (Regular), `/api/salesforce/anomaly_layer` (Salesforce)

**Layer Name:** Anomaly

**Purpose:** Uses Isolation Forest machine learning model to detect anomalous transaction patterns.

**Required Fields:**
- `customer_name`
- `order_date`
- `salesperson_name`
- `cust_state`
- `cust_city`
- `dealer_name`
- `wireless_package`
- `Tntype` (Transaction type: port/new/upgrade)
- `Autopay` (True/False)
- `email`
- `zip_code`
- `devicename`
- `devicetype` (hotspot/smartphone/tablet/wearable)
- `store_number`
- `gender`

**How It Works:**
1. **Feature Engineering:**
   - Extracts temporal features (month, weekday) from order date
   - Calculates fraud rates for:
     - Salesperson
     - State
     - City
     - Customer name
     - Dealer name
   - Calculates frequency metrics for customer names and dealers
   - Encodes categorical variables (wireless package, transaction type, device type)
   - Detects iPhone/Apple devices as binary feature

2. **Model Prediction:**
   - Loads pre-trained Isolation Forest model from pickle file
   - Predicts anomaly: -1 (suspicious) or 1 (normal)
   - Score mapping:
     - **Prediction 1 (score: 0.05-0.15)**: Normal transaction
     - **Prediction -1 (score: 0.91-0.99)**: Anomalous transaction

**Machine Learning Model:** Isolation Forest (unsupervised anomaly detection)

**Data Source:** Local pickle files containing:
- Pre-trained Isolation Forest model
- Fraud rate dictionaries for various features
- Label encoders for categorical variables

**Score Range:** 0.05-0.99

---

### 11. Intenso Layer
**Route:** `/intenso` (Regular), `/api/salesforce/intenso` (Salesforce)

**Layer Name:** Previous Suspicious Activity

**Purpose:** Machine learning-based analysis of transaction data to identify patterns similar to previously detected fraud.

**Required Fields:**
Same as Anomaly Layer (14 transaction-related fields)

**How It Works:**
1. Sends comprehensive transaction data to external ML API
2. API analyzes patterns against historical suspicious activity database
3. Returns fraud status (0 = safe, 1 = suspicious)
4. Score calculation:
   - **Fraud status 0 (score: 0.05-0.15)**: No suspicious activity detected
   - **Fraud status 1 (score: 0.91-0.99)**: Matches previous suspicious patterns

**External API:** `https://api.projectalphabet.ai/intenso`

**Score Range:** 0.05-0.99

**Use Case:** Complements the local Anomaly layer by leveraging external historical fraud pattern database.

---

## AI & LLM Layers

### 12. Energico Layer
**Route:** `/energico` (Regular), `/api/salesforce/energico` (Salesforce)

**Layer Name:** Encoder-Decoder Language

**Purpose:** Advanced fraud detection using Large Language Models (LLMs) with encoder-decoder transformer architecture.

**Required Fields:**
Same as Anomaly and Intenso layers (14 transaction-related fields)

**How It Works:**
1. Submits transaction data to LLM-powered API endpoint
2. LLM processes transaction details using transformer architecture:
   - Encoder interprets transaction context
   - Decoder generates fraud assessment
3. Model trained on extensive fraud datasets to understand transaction nuances
4. Returns fraud status with detailed reasoning
5. Score mapping:
   - **Fraud status 0 (score: 0.05-0.15)**: Legitimate transaction
   - **Fraud status 1 (score: 0.91-0.99)**: High fraud probability

**External API:** `https://api.projectalphabet.ai/energico`

**Technology:** Encoder-Decoder Language Models (Transformers)

**Score Range:** 0.05-0.99

**Detail:** The layer description states: "The Energico layer employs LLMs using the transformer architecture to process text prompts and generate responses. The encoder-decoder mechanism interprets input and creates coherent, relevant text. Trained on extensive datasets, these models understand language nuances and produce accurate outputs based on the given prompt."

---

### 13. AI Layer (Legacy)
**Route:** `/ai_layer` (Regular), `/api/salesforce/ai_layer` (Salesforce)

**Layer Name:** Previous Suspicious Activity

**Purpose:** Combined AI analysis providing both generative AI vision and fusion model predictions.

**Required Fields:**
Same as Anomaly, Intenso, and Energico layers (14 transaction-related fields)

**How It Works:**
1. Processes transaction data through dual AI models:
   - **GenAI Vision**: Generative AI model for fraud pattern recognition
   - **Fusion**: Combined model fusing multiple AI techniques
2. Each model provides independent fraud assessment
3. Updates scores based on fraud status
4. Returns comprehensive analysis with both model outputs

**Score Range:** 0.05-0.99

**Note:** This appears to be a legacy layer that may be superseded by Intenso and Energico layers.

---

## Network Security Layers

### 14. IP Address Layer
**Route:** `/ip_address` (Regular), `/api/salesforce/ip_address` (Salesforce)

**Layer Name:** IP Address

**Purpose:** Analyzes IP addresses to detect VPNs, proxies, hosting providers, and other suspicious network characteristics.

**Required Fields:**
- `ip` or `ipAddress`

**How It Works:**
1. **IP Validation:**
   - Validates IP address format
   - Rejects private, loopback, reserved, and multicast IPs
   - Only accepts public IP addresses

2. **API Analysis:**
   - Queries vpnapi.io for comprehensive IP information
   - Retrieves data about:
     - VPN/Proxy/Tor/Relay detection
     - Autonomous System Organization (ASO)
     - Network prefix length
     - Geographic location (country, timezone, city, region)

3. **Risk Calculation (Weighted Scoring):**
   - **Anonymization (45% weight):** VPN, proxy, Tor, or relay detection
   - **ASN Risk (25% weight):**
     - 1.0: Hosting providers (AWS, GCP, Azure, etc.)
     - 0.8: Backbone providers (Cogent, Hurricane Electric, etc.)
     - 0.5: Unknown/Other providers
     - 0.0: Consumer ISPs (Comcast, Verizon, Rogers, Bell, etc.)
   - **Prefix Risk (10% weight):**
     - 1.0: /24 or larger (suspicious)
     - 0.3: /20-/23 (moderate)
     - 0.1: Smaller than /20 (normal)
   - **Timezone Mismatch (8% weight):** Checks if timezone matches country code
   - **Geo Precision (5% weight):** Availability of city/region information
   - **Base Score (7% weight):** Constant baseline

4. **Risk Classification:**
   - **Low (≤0.20):** Consumer ISP, no suspicious indicators
   - **Review (0.21-0.50):** Moderate risk, requires inspection
   - **High (>0.50):** VPN, proxy, or data center detected

**External API:** `https://vpnapi.io/api/{ip}?key={API_KEY}`

**Score Range:** 0.0-1.0 (normalized)

**Special Features:**
- Detects US and Canadian consumer ISPs with specific pattern matching
- Identifies hosting providers and backbone networks
- Cross-validates timezone with country code for additional verification

---

## Database Verification Layers

### 15. FBI Layer
**Route:** `/fbi_layer` (Regular), `/api/salesforce/fbi_layer` (Salesforce)

**Layer Name:** FBI

**Purpose:** Checks customer information against internal FBI database of known fraudsters.

**Required Fields:**
- `customer_name`
- `gender`

**How It Works:**
1. Queries internal FBIData table for matching records
2. Checks for name and gender matches
3. Risk assessment based on match type:
   - **No match (score: 0.05-0.15):** "Trustful data. Fraud probability - Low! FBI verified."
   - **Name match only (score: 0.46-0.55):** Partial match, moderate risk
   - **Name + Gender match (score: 0.91-0.99):** "Suspicious data. Fraud probability - High! FBI verified."

**Data Source:** Internal PostgreSQL database (FBIData table)

**Score Range:** 0.05-0.99

**Note:** Despite the name "FBI," this appears to be an internal database of known fraudsters, not an actual FBI government database.

---

## Summary Table

| Layer Name | External API | Type | Primary Purpose |
|------------|-------------|------|-----------------|
| Permanent Memory User Details | No | Database | Historical customer fraud check |
| Permanent Memory Geolocation | No | Database | Historical address fraud check |
| Google Address Validation | Yes | Validation | Physical address verification |
| Smarty Address Validation | Yes | Validation | Alternative address verification |
| AI Prompt Layer | Yes (OpenAI) | AI/LLM | Identity inconsistency detection |
| Gilbert Layer | Yes (ZeroBounce + Gemini) | Validation + AI | Email validation & fraud analysis |
| Word Cloud Name | Yes | ML | Name pattern fraud detection |
| Word Cloud Email | Yes | ML | Email pattern fraud detection |
| Geolocation Hotspot | Yes | Geolocation | Zip code fraud hotspot detection |
| Anomaly Layer | No | ML | Transaction anomaly detection |
| Intenso | Yes | ML | Historical suspicious activity matching |
| Energico | Yes | AI/LLM | Transformer-based fraud detection |
| AI Layer | Yes | AI/LLM | Legacy dual AI model analysis |
| IP Address | Yes (vpnapi.io) | Network | VPN/Proxy/Hosting detection |
| FBI Layer | No | Database | Known fraudster verification |

---

## Score Interpretation

All layers return a fraud score between 0 and 1:

- **0.00-0.20:** Low Risk (Safe/Legitimate)
- **0.21-0.45:** Low-Medium Risk
- **0.46-0.60:** Medium Risk (Review Recommended)
- **0.61-0.90:** Medium-High Risk
- **0.91-1.00:** High Risk (Suspicious/Fraudulent)

**Special Score:** `-1` indicates insufficient input data (missing required fields)

---

## API Integration Summary

### External APIs Used:

1. **Google Address Validation API** - Address verification
2. **vpnapi.io** - IP intelligence and VPN/proxy detection
3. **ZeroBounce API** - Email validation service
4. **Google Gemini 2.5 Flash** - LLM-based email fraud analysis
5. **OpenAI GPT-4o-mini** - Identity signal fraud detection
6. **OpenAI Moderation API** - Content filtering
7. **Project Alphabet AI APIs** - Multiple ML services:
   - `/word_cloud_name` - Name pattern analysis
   - `/word_cloud_email` - Email pattern analysis
   - `/geolocation_hotspot_layer` - Zip code fraud mapping
   - `/intenso` - ML-based suspicious activity detection
   - `/energico` - LLM-based fraud detection

### Internal Data Sources:

1. PostgreSQL database tables:
   - `database_layer` - Historical fraud records
   - `FBIData` - Known fraudster database
2. Pickle files (ML models and encoders):
   - `isolation_forest_model.pkl` - Anomaly detection model
   - Various fraud rate dictionaries
   - Label encoders for categorical features

---

## Error Handling

All layers implement consistent error handling:

1. **Missing Required Fields:** Returns score of `-1` with detailed error message listing missing fields
2. **API Failures:** Returns score of `0.5` with "Internal Error" message
3. **Invalid Input:** Returns appropriate error response with validation details

---

## Authentication

- **Regular Routes:** Use `@validate_request` decorator for authentication
- **Salesforce Routes:** Use `@requireSalesforceAuth` decorator with Org-ID header
- **External API Calls:** Use various API keys stored in environment variables

---

## Notes for Developers

1. All layers follow a consistent response format with `score`, `reason`, `Summary`, and `layer` fields
2. Scores are randomized within ranges to prevent exact pattern matching by fraudsters
3. Multiple layers can be combined to create comprehensive fraud detection "builds"
4. The system uses Sentry for error tracking and performance monitoring
5. Most external API calls include timeout configurations and retry logic
6. Database queries are instrumented with Sentry spans for performance tracking

---

**Document Version:** 1.0
**Last Updated:** 2025-12-24
**Maintained By:** Fortress Development Team
