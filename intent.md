# Payslip Translation & Pay Code Explanation Agent

AI agent that translates payslip pay codes and components into all major European languages, enabling employee self-service and drastically reducing HR Ops effort.

## Business Challenge

HR Operations currently spends approximately 4 hours per payslip translation request when employees need their payslip in a different language. Employees have no way to understand pay code components in their preferred language. The agent should allow employees to self-serve translations and enable HR Ops to cut turnaround from ~4 hours to under 5 minutes, increasing efficiency and employee satisfaction.

## Business Goals & Success Criteria

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Time per payslip translation request | ~4 hours | Under 5 minutes | — | Payroll document translation | user |
| Monthly HR Ops effort on translations | 80–200 hours/month (20–50 requests × ~4h) | Under 5 hours/month | — | HR Operations efficiency | user |
| Employee self-service rate for translations | 0% (HR Ops only) | Employees handle own translation requests | — | Employee self-service capability | user |

## Key Milestones

1. **Payroll Data Retrieval** – Agent connects to SAP S/4HANA Payroll and retrieves the employee's payslip data including all pay codes and amounts for a given period.
2. **Pay Code Translation** – Agent translates all pay code labels into the requested European language using LLM capabilities.
3. **Plain-Language Explanation** – Agent explains each pay code in simple, non-technical language so the employee can fully understand each component.
4. **Follow-up Q&A** – Agent answers follow-up questions from employees or HR Ops about specific deductions, earnings, or payslip line items.
5. **Translated Document & Period Comparison** – Agent generates a translated payslip document (PDF) and supports comparison of payslips across periods upon request.

## Business Architecture (RBA)

### End-to-End Process

Recruit to Retire

### Process Hierarchy

```
Recruit to Retire
└── Manage Workforce (generic)
    └── Manage payroll and reimbursements (generic) [BPS-394]
        └── Process payroll
        └── Manage payroll taxes and legal deductions
        └── Process expense reimbursements
└── Reward to Retain (generic)
    └── Reward and recognize talent (generic) [BPS-390]
        └── Develop and manage reward, recognition and motivation programs
```

### Summary

The payslip translation challenge maps to the Recruit to Retire E2E process, primarily the "Manage payroll and reimbursements" sub-process covering payroll processing and legal deductions. The multilingual explanation and self-service dimension introduces a capability gap that requires a custom AI agent on top of existing SAP payroll infrastructure.

## Fit Gap Analysis

| Requirement (business) | Standard asset(s) found | API ORD ID | MCP Server ORD ID | MCP Server Version | Webhook API ORD ID | Data Product ORD ID | Gap? | Notes / assumptions |
|------------------------|------------------------|------------|-------------------|--------------------|--------------------|---------------------|------|---------------------|
| Retrieve employee payslip data and pay codes | SAP S/4HANA Payroll | `sap.sf:apiResource:ECEmployeeCentralPayroll:v1` | — | — | — | — | No | Standard payroll API available; direct API call from agent |
| Retrieve compensation details | SAP SuccessFactors Employee Central | `sap.sf:apiResource:ECCompensationInformation:v1` | — | — | — | — | No | Available via OData API |
| Translate pay code labels to European languages | No standard SAP feature | — | — | — | — | — | Yes | Custom AI agent with LLM translation required |
| Plain-language explanation of each pay code | No standard SAP feature | — | — | — | — | — | Yes | LLM-powered reasoning in agent |
| Generate translated payslip PDF document | No standard SAP feature | — | — | — | — | — | Yes | Custom document generation in agent |
| Answer follow-up questions on deductions/earnings | No standard SAP feature | — | — | — | — | — | Yes | Conversational AI agent capability |
| Compare payslips across pay periods | No standard SAP feature | — | — | — | — | — | Yes | Agent retrieves and compares multiple periods |

### Key Findings

- SAP SuccessFactors and S/4HANA provide robust payroll management capabilities (Payroll Management SC1291, Reimbursement Management SC1388) but have no native multilingual translation or plain-language explanation features.
- No MCP servers were found for the relevant SAP payroll APIs — the agent will call them directly via OData.
- The primary value of this solution lies entirely in custom AI capabilities: translation, explanation, PDF generation, and conversational Q&A.
- Both employees (self-service) and HR Ops are target users, requiring the agent to handle both simple self-service queries and more detailed HR-level investigations.
- All major European languages must be supported (EN, DE, FR, ES, IT, PT, NL, PL, etc.), which is natively handled by the LLM layer.
- The "Manage Employee Compensation" SOAP API was marked as unavailable and will not be used.

## Recommendations

### AI Agent for Multilingual Payslip Translation and Explanation

#### Executive Summary

Custom Python AI agent connecting to S/4HANA Payroll for translation and Q&A.

#### Recommended Solution

A pro-code Python AI agent (A2A protocol) that:
1. Connects to SAP S/4HANA Payroll via OData APIs to retrieve payslip data for a given employee and pay period.
2. Uses an LLM to translate all pay code labels and amounts into the requested European language.
3. Generates plain-language explanations of each pay component tailored to the employee's language.
4. Engages in a conversational Q&A session to answer follow-up questions on deductions, taxes, bonuses, and other line items.
5. Generates a translated PDF payslip document on demand.
6. Supports comparison of payslips across multiple pay periods.

The agent is deployed on SAP BTP and accessible to both employees (self-service) and HR Ops.

#### Problem Statement

Employees requesting payslip translations in their native language require ~4 hours of manual HR Ops effort per request. There is no self-service option, and the volume of 20–50 requests per month creates a significant operational burden. The manual process is also error-prone and delays employee understanding of their own compensation.

#### Affected User Roles

- **Employees** – Need to understand their payslip in their preferred language without waiting for HR support.
- **HR Operations Staff** – Currently spend 4 hours per translation request; will use agent to deliver results in under 5 minutes.

#### Important Factors

##### Reduces Manual Effort Through Automation
The agent eliminates the manual translation workflow entirely. A task that takes 4 hours is reduced to under 5 minutes by automating retrieval, translation, explanation, and document generation.

##### Employee Self-Service Empowerment
By exposing the agent to employees directly, the solution shifts from a "HR Ops service model" to a "self-service model", giving employees immediate access to translated payslip information in their language at any time.

##### Multilingual LLM Coverage
Modern LLMs natively handle all major European languages with high accuracy, removing the need for separate translation services or language-specific configurations.

#### Potential Risks

##### Payroll API Access and Data Security
Direct access to employee payslip data requires careful authentication, authorization, and data handling. Only the requesting employee's data must be accessible to that employee; HR Ops should have broader but audited access.

##### LLM Translation Accuracy for Legal/Tax Terms
Some pay codes relate to legal or tax terminology that may not translate with sufficient precision. Translated documents should include a disclaimer that the original payslip remains the official record.

#### Recommended Solution Category

AI Agent

#### Intent Fit

92%
