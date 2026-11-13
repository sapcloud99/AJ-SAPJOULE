# Product Requirements Document (PRD)

**Title:** Payslip Translation & Pay Code Explanation Agent
**Date:** 2026-11-13
**Owner:** HR Operations
**Solution Category:** AI Agent

---

## Product Purpose & Value Proposition

**Elevator Pitch:**
Employees across the company receive payslips filled with technical pay codes in a language they may not understand. Getting a translation and explanation today means waiting hours for HR Ops to respond manually. This AI agent eliminates that wait — employees can instantly ask for their payslip translated and explained in their language, and HR Ops can serve requests in minutes instead of hours.

**Business Need:**
HR Operations currently spends approximately 4 hours per payslip translation request. With 20–50 such requests per month, this creates 80–200 hours of monthly HR Ops effort on a non-strategic, repetitive task. Employees lack access to self-service, creating frustration and delays in understanding their own compensation. There is no standard SAP capability to translate or explain payslip pay codes in natural language.

**Expected Value:**
- Reduce per-request handling time from ~4 hours to under 5 minutes
- Free up 75–195 hours of HR Ops capacity per month
- Enable 100% of employees to self-serve payslip translations in their preferred European language

**Product Objectives (Prioritised):**
1. Retrieve payslip data from SAP S/4HANA Payroll and translate all pay codes into the employee's requested European language
2. Explain each pay code in plain, non-technical language so any employee can understand their compensation
3. Support conversational follow-up Q&A on deductions, taxes, and earnings
4. Generate a downloadable translated payslip document (PDF)
5. Enable payslip comparison across pay periods

---

## Business Metrics

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Time per payslip translation request | ~4 hours | Under 5 minutes | — | Payroll document translation | user |
| Monthly HR Ops effort on translations | 80–200 hours/month (20–50 requests × ~4h) | Under 5 hours/month | — | HR Operations efficiency | user |
| Employee self-service rate for translations | 0% (HR Ops only) | Employees handle own translation requests | — | Employee self-service capability | user |

---

## User Profiles & Personas

### Primary Persona: Maria — International Employee

Maria is a 34-year-old software engineer who joined the company from Spain. Her company's payroll system generates payslips in German, which she can read partially but struggles with technical tax and deduction codes like "LSt KL IV", "KV AG", or "SV Abzug". Every month she has a few questions about her net pay, and occasionally she needs a formal explanation in Spanish for a bank loan application. Today she sends an email to HR Ops and waits up to two days for a response. She wants immediate answers in her language — she's comfortable with chat interfaces and digital tools.

**Pain Points:**
- Does not understand deduction codes and their legal meaning
- Has to wait 1–2 business days for HR Ops to respond
- Cannot provide translated payslip documentation to third parties (banks, authorities) quickly

**Success for Maria:** She types her question in Spanish, instantly receives a full explanation of each pay code in Spanish, and can download a translated PDF to share with her bank — all in under 5 minutes.

---

### Secondary Persona: James — HR Operations Specialist

James is a 41-year-old HR Ops Specialist managing payroll queries for a workforce of ~1,200 employees across 8 countries. Each month he fields 20–50 payslip translation requests, each taking around 4 hours to research, translate, and document correctly. He is meticulous about accuracy — especially for tax and legal deduction terminology — but the manual process is draining. He wants a tool he can trust to handle routine translation and explanation requests so he can focus on complex HR cases.

**Pain Points:**
- Spends up to 200 hours/month on a repetitive, low-complexity task
- Risk of translation errors for legal and tax terms under time pressure
- No audit trail for translated payslip requests

**Success for James:** He uses the agent to handle all routine translation requests in minutes, reviews only flagged or complex cases, and has a full audit log of what was translated and delivered to whom.

---

### Other User Types

- **HR Manager / HRBP** — May access the agent to assist employees during performance reviews or offboarding conversations involving compensation clarification.
- **Finance Audit Team** — May require translated payslip records for audit purposes; benefits from the agent's audit trail.

---

## User Goals & Tasks

### For Maria (Employee):

**Goals:**
- Understand every component of her payslip in her preferred language without waiting for HR
- Obtain a translated payslip document for official third-party use (e.g. bank, government)
- Ask follow-up questions about specific deductions or bonuses

**Key Tasks:**
- Request translation of current or past payslip into a specified European language
- Ask plain-language questions like "What is this deduction for?" or "Why did my net pay change this month?"
- Download a PDF of the translated payslip

---

### For James (HR Ops Specialist):

**Goals:**
- Handle payslip translation requests in minutes instead of hours
- Ensure translation accuracy for legal and tax terminology
- Maintain an audit record of all translations delivered

**Key Tasks:**
- Use the agent on behalf of an employee to generate a translated payslip
- Compare an employee's payslip across two periods to identify changes
- Review the agent's output before forwarding to the employee

---

## Product Principles

1. **Employee First:** The agent must be usable directly by employees without any HR Ops involvement for standard cases.
2. **Accuracy over Speed:** For legal and tax pay codes, translations must be precise. When uncertain, the agent should flag the term rather than guess.
3. **Data Minimisation:** The agent retrieves only the payslip data needed to answer the current request — no bulk data access.
4. **Transparency:** All translated documents include a disclaimer that the original payslip in the system of record remains authoritative.
5. **Language Neutrality:** The agent responds in the language the user communicates in, without requiring explicit configuration.

---

## Business Context

**Current State:**
Payslip translation is a fully manual process. HR Ops receives translation requests via email, looks up the payslip in SAP S/4HANA, manually translates each pay code using internal glossaries and judgment, and returns a response — a process taking approximately 4 hours per request. There is no self-service channel, no translation audit trail, and no consistency guarantee across HR specialists.

**Strategic Alignment:**
This solution directly supports the company's HR digital transformation agenda by eliminating a high-effort, low-value manual process and enabling employee self-service — a core principle of the HR Operations modernisation roadmap.

---

## Goals and Non-Goals

### Goals (In Scope)

- Retrieve payslip data for a specific employee and pay period from SAP S/4HANA Payroll
- Translate all pay code labels, descriptions, and amounts into any major European language
- Explain each pay component in plain, non-technical language in the employee's language
- Support conversational follow-up questions about payslip line items
- Generate a translated payslip as a downloadable PDF document
- Compare payslips across two or more pay periods and highlight differences
- Enforce role-based data access: employees access only their own payslips; HR Ops has broader access

### Non-Goals (Out of Scope)

- Modifying, correcting, or recalculating payslip data in SAP S/4HANA
- Payroll processing or payroll run management
- Support for non-European languages in Phase 1
- Integration with external translation services (the LLM layer handles translation natively)
- Replacing the authoritative payslip document stored in SAP S/4HANA

---

## Requirements

### Must-Have Requirements

**REQ-01: Payslip Data Retrieval**

- **Problem to Solve:** Employees and HR Ops need access to structured payslip data including all pay codes and amounts for a given pay period in order to request a translation.
- **User Story:** As an employee or HR Ops specialist, I need the agent to retrieve my payslip data from SAP S/4HANA Payroll for a specified period so that it can be translated and explained.
- **Acceptance Criteria:**
  - Given I provide my employee ID and a pay period, when I ask for my payslip, then the agent retrieves all pay codes, descriptions, and amounts for that period from SAP S/4HANA.
  - Given I am an employee, when I request data, then I can only access my own payslip; HR Ops can access any employee's payslip.
- **Maps to Objective:** Objective 1
- **Priority Rank:** 1

---

**REQ-02: Pay Code Translation**

- **Problem to Solve:** Pay code labels in SAP S/4HANA are system codes or abbreviated terms in one language. Employees cannot understand them in their preferred language.
- **User Story:** As an employee, I need all pay code labels on my payslip translated into my preferred European language so that I can understand what each line means.
- **Acceptance Criteria:**
  - Given a payslip retrieved from SAP S/4HANA, when I request translation into French, then all pay code labels are translated into French accurately.
  - Given a pay code with legal or tax significance, when translated, then the agent uses the correct legal terminology in the target language.
  - Supported languages: English, German, French, Spanish, Italian, Portuguese, Dutch, Polish, and other major European languages.
- **Maps to Objective:** Objective 1
- **Priority Rank:** 2

---

**REQ-03: Plain-Language Pay Code Explanation**

- **Problem to Solve:** Even translated pay code labels may still be technical. Employees need a human-readable explanation of what each component means and why it appears on their payslip.
- **User Story:** As an employee, I need each pay code explained in simple, everyday language in my preferred language so that I can fully understand my compensation and deductions.
- **Acceptance Criteria:**
  - Given a translated payslip, when the employee asks for explanations, then each pay code includes a 1–3 sentence plain-language description of what it represents.
  - Given a deduction code, when explained, then the explanation includes the reason for the deduction (e.g. "This is your statutory pension contribution, which is required by law in Germany.").
- **Maps to Objective:** Objective 2
- **Priority Rank:** 3

---

**REQ-04: Conversational Follow-up Q&A**

- **Problem to Solve:** After seeing a translated payslip, employees and HR Ops often have follow-up questions about specific items that require contextual answers beyond a static explanation.
- **User Story:** As an employee, I need to ask the agent follow-up questions about specific deductions or earnings on my payslip so that I fully understand any changes or unexpected amounts.
- **Acceptance Criteria:**
  - Given a translated payslip has been presented, when the employee asks "Why did my tax deduction increase this month?", then the agent provides a contextual explanation referencing the payslip data.
  - Given a follow-up question, when the agent cannot determine the answer from payslip data alone, then it clearly states the limitation and suggests contacting HR Ops.
- **Maps to Objective:** Objective 3
- **Priority Rank:** 4

---

**REQ-05: Translated Payslip PDF Generation**

- **Problem to Solve:** Employees sometimes need a formal translated payslip document to submit to banks, government agencies, or other third parties.
- **User Story:** As an employee, I need to download a translated version of my payslip as a PDF so that I can submit it to a third party (e.g. a bank for a loan application).
- **Acceptance Criteria:**
  - Given a translated payslip, when the employee requests a PDF, then the agent generates a downloadable PDF containing all pay codes, translated labels, amounts, and a disclaimer that the original payslip in SAP remains the official record.
  - Given a PDF is generated, when the employee downloads it, then it is clearly labelled as a translation and includes the original pay period and employee name.
- **Maps to Objective:** Objective 4
- **Priority Rank:** 5

---

**REQ-06: Payslip Period Comparison**

- **Problem to Solve:** Employees and HR Ops often need to understand why net pay changed between two periods — identifying which pay codes changed, were added, or were removed.
- **User Story:** As an employee or HR Ops specialist, I need to compare two payslips from different periods side by side so that I can identify what changed and why.
- **Acceptance Criteria:**
  - Given two pay periods, when comparison is requested, then the agent retrieves both payslips and presents a structured comparison showing added, removed, and changed pay codes with their translated labels and amounts.
  - Given a comparison result, when a pay code value changed between periods, then the change is clearly highlighted with the delta amount.
- **Maps to Objective:** Objective 5
- **Priority Rank:** 6

---

**REQ-07: Role-Based Data Access Control**

- **Problem to Solve:** Payslip data is sensitive personal and financial data. Employees must only see their own payslips; HR Ops must have audited access to any employee's data.
- **User Story:** As a system, I must enforce that employees can only retrieve and translate their own payslip data, while HR Ops can access any employee's payslip for support purposes.
- **Acceptance Criteria:**
  - Given an employee is authenticated, when they request a payslip, then the agent retrieves only their own payslip data.
  - Given an HR Ops user is authenticated, when they request a payslip for a named employee, then the agent retrieves that employee's data and logs the access event.
  - All access events are logged with user identity, timestamp, employee ID accessed, and action taken.
- **Maps to Objective:** Objective 1
- **Priority Rank:** 1

---

### High-Want Requirements

**REQ-08: Proactive Anomaly Flagging**

- **Problem to Solve:** Unusual deductions or unexpected changes in pay codes often go unnoticed until the employee is confused. The agent could proactively flag these.
- **User Story:** As an employee, I need the agent to proactively highlight any unusual or significantly changed pay code amounts so that I notice important changes without having to ask.
- **Priority Rank:** 1

---

**REQ-09: Language Auto-Detection**

- **Problem to Solve:** Requiring the employee to explicitly specify their preferred language adds unnecessary friction.
- **User Story:** As an employee, I need the agent to detect the language I am writing in and respond in that language automatically so that I do not need to configure any language preference.
- **Priority Rank:** 2

---

## Non-Functional Requirements

### Performance

- **Latency:** The agent must return a full translated payslip explanation in under 60 seconds for a standard payslip (up to 30 pay codes).
- **Throughput:** The agent must handle at least 10 concurrent translation requests without degradation.

### Reliability

- **Availability:** The agent must be available during standard business hours (Monday–Friday, 07:00–19:00 local time) with 99% uptime.
- **Fallback:** If the SAP S/4HANA Payroll API is unavailable, the agent must return a clear error message and suggest the employee contact HR Ops directly.

### Security

- **Authentication:** All users must authenticate via the company's identity provider (SAP BTP Identity Authentication).
- **Data isolation:** Payslip data must never be stored in the agent's memory beyond the duration of a single session.
- **PII handling:** Payslip data is classified as sensitive personal data and must be processed in accordance with GDPR.

### Explainability

- **Traceability:** Each translated pay code explanation must be traceable to the original pay code value retrieved from SAP S/4HANA.
- **Disclaimer:** All generated PDFs and translated outputs must include a disclaimer that the translation is AI-generated and the original SAP record remains authoritative.

---

## Solution Architecture

**Architecture Overview:**
A Python AI agent (A2A protocol) deployed on SAP BTP acts as the central orchestrator. It connects to SAP S/4HANA Payroll via OData APIs to retrieve payslip data, uses SAP Generative AI Hub for LLM-powered translation and explanation, generates PDF documents, and exposes a conversational interface to both employees and HR Ops.

**Key Components:**

- **Payslip Translation Agent (Python, A2A):** Core agent deployed on SAP BTP; orchestrates all capabilities and manages conversation state.
- **SAP Generative AI Hub:** Provides the LLM for translation, plain-language explanation, and conversational Q&A across all major European languages.
- **SAP S/4HANA Payroll OData API:** Source of payslip data including pay codes, descriptions, and amounts (`ECEmployeeCentralPayroll`, `ECCompensationInformation`).
- **PDF Generation Module:** Converts the translated payslip content into a downloadable, formatted PDF document.
- **SAP BTP Identity Authentication Service (IAS):** Manages user authentication and role-based access control.

**Integration Points:**

- SAP S/4HANA Payroll (OData, read-only): Retrieves payslip records per employee and pay period — called on demand per user request.
- SAP Generative AI Hub (REST): Invokes the LLM for translation and explanation — called per payslip retrieval.
- Identity Provider (IAS): Validates user identity and role (employee vs. HR Ops) at session start.

**Deployment Environments:**

- **Development:** SAP BTP dev subaccount with anonymised payslip test data
- **Production:** SAP BTP production subaccount with full access to SAP S/4HANA Payroll; GDPR-compliant data processing

---

### Agent Extensibility & Instrumentation

**Agent Extensibility:**
The agent is designed with clear extension points to allow future capabilities to be added without rebuilding the core:
- New language support: adding additional language targets requires no code changes — handled natively by the LLM layer.
- New data sources: additional payroll or compensation APIs can be integrated as new tools registered with the agent.
- New output formats: additional document formats (e.g. Word, HTML) can be added as output modules alongside the PDF generator.
- New skill packages: domain-specific pay code glossaries (e.g. country-specific tax codes) can be injected as skill resources to improve explanation accuracy.

**Business Step Instrumentation:**
Each key business step emits structured log statements to support observability, debugging, and SLA monitoring in production. All log messages follow the pattern: `[MILESTONE_ID].[achieved|missed]: [description]`.

---

### Automation & Agent Behaviour

**Automation Level:** Autonomous agent with human-in-the-loop for high-sensitivity outputs (PDF generation and delivery)

**Actions the system performs without human approval:**
- Retrieve payslip data for the authenticated user
- Translate pay code labels and explanations
- Answer conversational follow-up questions
- Generate translated payslip PDF (delivered to the requesting user's session)

**Actions that require human review or approval:**
- HR Ops reviewing and forwarding a translated payslip to a third party on behalf of an employee (HR Ops decision, not automated)

**Model or engine used:** SAP Generative AI Hub (GPT-4o or equivalent LLM available in the hub)

**Knowledge & data sources accessed:**

- SAP S/4HANA Payroll (OData API): Payslip data including pay codes, amounts, and periods — read-only
- SAP SuccessFactors Employee Central Compensation API (`ECCompensationInformation`): Supplementary compensation context — read-only

**Tools or connectors invoked:**

- `get_payslip`: Retrieves payslip data for an employee and pay period from SAP S/4HANA Payroll (read-only)
- `get_compensation_details`: Retrieves additional compensation context from SAP SuccessFactors EC (read-only)
- `translate_and_explain_payslip`: Invokes LLM via SAP Generative AI Hub to translate and explain all pay codes in the target language
- `generate_payslip_pdf`: Generates a formatted, translated PDF of the payslip
- `compare_payslips`: Retrieves and compares two payslips from different periods, highlighting changes

**Guardrails & fail-safes:**

- The agent never modifies, writes, or updates any payslip data in SAP S/4HANA — all API calls are strictly read-only.
- Employees cannot request payslip data for other employees — enforced by identity validation at every tool call.
- All generated translations include a disclaimer that the AI translation is informational and the original SAP record is authoritative.
- If the LLM confidence on a legal/tax term translation is low, the agent flags the term and recommends the employee verify with HR Ops.
- If the SAP payroll API is unavailable, the agent halts gracefully and instructs the user to retry or contact HR Ops.

---

## Milestones

### M1: Payroll Data Retrieval

- **Description:** The agent successfully connects to SAP S/4HANA Payroll and retrieves the employee's payslip data including all pay codes, descriptions, and amounts for the requested pay period.
- **Achieved when:** The payslip data has been retrieved and contains at least one pay code entry.
- **Log on achievement:** `M1.achieved: payslip data retrieved successfully for employee {employee_id}, period {pay_period}, {pay_code_count} pay codes found`
- **Log on miss:** `M1.missed: payslip data retrieval failed for employee {employee_id}, period {pay_period} — reason: {error_reason}`

---

### M2: Pay Code Translation

- **Description:** All pay code labels in the retrieved payslip have been translated into the employee's requested European language.
- **Achieved when:** Every pay code label has a corresponding translated label in the target language.
- **Log on achievement:** `M2.achieved: {pay_code_count} pay codes translated to {target_language} for employee {employee_id}`
- **Log on miss:** `M2.missed: translation incomplete for employee {employee_id} — {untranslated_count} pay codes could not be translated to {target_language}`

---

### M3: Plain-Language Explanation

- **Description:** Each translated pay code has been accompanied by a plain-language explanation in the employee's language.
- **Achieved when:** All pay codes have a non-empty explanation text in the target language.
- **Log on achievement:** `M3.achieved: plain-language explanations generated for all {pay_code_count} pay codes in {target_language}`
- **Log on miss:** `M3.missed: explanation generation incomplete — {unexplained_count} pay codes missing explanations for employee {employee_id}`

---

### M4: Follow-up Q&A

- **Description:** The agent has successfully answered a conversational follow-up question from the employee or HR Ops about a specific payslip line item.
- **Achieved when:** The agent returns a contextually relevant answer referencing payslip data.
- **Log on achievement:** `M4.achieved: follow-up question answered for employee {employee_id}, question topic: {topic}`
- **Log on miss:** `M4.missed: follow-up question could not be answered for employee {employee_id} — escalated to HR Ops`

---

### M5: Translated Document & Period Comparison

- **Description:** The agent has either generated a translated PDF payslip for download, or completed a period comparison and presented the result to the user.
- **Achieved when:** PDF is generated and available for download, or comparison results are presented with changes highlighted.
- **Log on achievement:** `M5.achieved: {action} completed for employee {employee_id} — action: [pdf_generated | period_comparison]`
- **Log on miss:** `M5.missed: {action} failed for employee {employee_id} — reason: {error_reason}`

---

## Governance, Risk & Compliance

**Data Handling:**
- Payslip data is classified as sensitive personal data (GDPR Article 9 — financial data)
- Data must be processed within the EU and must not be stored beyond the active session
- No payslip data may be logged in plain text in application logs

**Compliance Frameworks:**
- GDPR: Applies to all payslip data processing for EU employees
- Country-specific payroll regulations: Translation disclaimers are required to prevent the translated document from being treated as an official payroll record

**Approval Flows:**
- HR Ops review is recommended (not enforced) before forwarding translated PDFs to third parties on behalf of employees

---

## Risks, Assumptions, and Dependencies

### Risks

- **LLM translation accuracy for legal/tax codes:** Some country-specific tax codes may not translate with full legal precision. Mitigated by flagging uncertain translations and including a disclaimer on all outputs.
- **Payroll API access:** The agent requires read access to SAP S/4HANA Payroll OData APIs. If API access is restricted or unavailable, the agent cannot function. This must be provisioned as part of deployment.
- **GDPR compliance of LLM provider:** The LLM invoked via SAP Generative AI Hub must process data within GDPR-compliant infrastructure. Verify SAP's data processing agreements cover payroll data.

### Assumptions

- SAP S/4HANA Payroll OData APIs (`ECEmployeeCentralPayroll`, `ECCompensationInformation`) are accessible from SAP BTP in the customer's landscape.
- SAP Generative AI Hub is available and provisioned for this tenant.
- Employee identity management is handled by SAP BTP Identity Authentication Service (IAS).
- The agent will be accessed via a chat interface embedded in an existing HR portal or SAP Build Work Zone.

### Dependencies

- SAP S/4HANA Payroll API access provisioning
- SAP Generative AI Hub subscription and model availability
- SAP BTP subaccount with Python runtime support
- Identity provider (IAS) configuration for employee and HR Ops roles

---

## Appendix

### Glossary

- **Pay Code:** A system-generated identifier for a payroll line item (e.g. "LSt KL IV" = wage tax class IV in Germany)
- **A2A Protocol:** Agent-to-Agent protocol — the standard communication protocol for AI agents deployed on SAP BTP
- **OData:** Open Data Protocol — the REST-based API standard used by SAP systems to expose business data
- **SAP Generative AI Hub:** SAP's managed LLM service on SAP BTP, providing access to large language models for enterprise use cases
- **IAS:** SAP Identity Authentication Service — the identity provider used for authentication and role management on SAP BTP

### References

- SAP SuccessFactors Employee Central Payroll API: `sap.sf:apiResource:ECEmployeeCentralPayroll:v1`
- SAP SuccessFactors Compensation Information API: `sap.sf:apiResource:ECCompensationInformation:v1`
- SAP Generative AI Hub documentation: https://help.sap.com/docs/sap-ai-core
- GDPR Article 9 — Processing of special categories of personal data
