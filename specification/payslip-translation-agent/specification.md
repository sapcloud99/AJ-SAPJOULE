# Specification: payslip-translation-agent

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-agent.md](../guidelines-agent.md) — Universal agent patterns
> - [guidelines-agent-python.md](../guidelines-agent-python.md) — Python implementation details
> - [guidelines-agent-skills.md](../guidelines-agent-skills.md) — Runtime skills patterns
> - [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) — MCP integration patterns

---

## Basic Setup

- [x] Read `product-requirements-document.md` and `intent.md` as the primary source of requirements, milestones, and guardrails
- [x] Bootstrap agent code in `assets/payslip-translation-agent/` using instructions from the `sap-agent-bootstrap` section (invoke from inside `assets/payslip-translation-agent/`, use copy commands — do NOT create files manually)
- [x] Install dependencies and validate the agent starts and responds at `/.well-known/agent.json`

---

## Runtime Skills

The agent handles two distinct, complex workflows that benefit from runtime skills:

- [x] Create `assets/payslip-translation-agent/app/skills/payslip-translation/SKILL.md` — step-by-step instructions for retrieving, translating, and explaining a payslip including language detection, pay code lookup, and disclaimer injection
- [x] Create `assets/payslip-translation-agent/app/skills/payslip-comparison/SKILL.md` — step-by-step instructions for comparing two payslips across periods: retrieve both, align pay codes, highlight additions, removals, and amount changes
- [x] Create `assets/payslip-translation-agent/app/skills/payslip-translation/references/pay-code-glossary.md` — reference table of common pay code patterns across major European payroll systems (generic, not customer-specific) to help the LLM produce accurate plain-language explanations

---

## Project-Specific Tasks

### REQ-01 — Payslip Data Retrieval

- [x] Implement `get_payslip` tool logic: accept `employee_id` and `pay_period` (YYYY-MM format), retrieve payslip line items (pay codes, descriptions, amounts) from SAP S/4HANA via the generated MCP server for `ECEmployeeCentralPayroll`
- [x] Implement `get_compensation_details` tool logic: accept `employee_id`, retrieve supplementary compensation context (base salary, pay grade, pay scale) from the generated MCP server for `ECCompensationInformation`
- [x] Enforce data access control in the system prompt: instruct the agent that it must only retrieve payslip data for the currently authenticated employee unless the HR Ops role is active; never return another employee's data to a non-HR user
- [x] Add system prompt instruction: "When calling tools that support pagination, always set the page size parameter to a maximum of 100. Never fabricate or invent payslip data — always retrieve it via tools."

### REQ-02 — Pay Code Translation

- [x] Implement `translate_and_explain_payslip` tool logic: accept the raw payslip data (list of pay code objects) and `target_language` (BCP-47 language tag, e.g. `de`, `fr`, `es`, `it`, `pt`, `nl`, `pl`, `en`), return a structured list with each pay code entry containing: `original_code`, `translated_label`, `plain_language_explanation`, `amount`, `currency`, `confidence` (high/medium/low)
- [x] Add system prompt instruction: "Translate all pay code labels into the target language using correct legal and tax terminology. If confidence in a legal term translation is medium or low, set the confidence field accordingly and surface the uncertainty to the user."
- [x] Load the `payslip-translation` skill when handling translation requests using the `load(path)` tool
- [x] Validate supported languages: EN, DE, FR, ES, IT, PT, NL, PL — reject unsupported language codes with a clear message

### REQ-03 — Plain-Language Pay Code Explanation

- [x] Ensure `translate_and_explain_payslip` includes `plain_language_explanation` for each pay code — a 1–3 sentence, jargon-free explanation in the target language describing what the pay code represents and why it appears on the payslip
- [x] Load `skills/payslip-translation/references/pay-code-glossary.md` for context when generating explanations
- [x] Add system prompt instruction: "When explaining pay codes, use simple, everyday language that a non-finance employee can understand. Avoid acronyms unless they are immediately explained."

### REQ-04 — Conversational Follow-up Q&A

- [x] Design the agent's system prompt to retain payslip context across conversation turns within a session so follow-up questions (e.g. "Why did my pension deduction increase?") are answered using the already-retrieved payslip data — no redundant API calls
- [x] Add system prompt instruction: "When answering follow-up questions about the payslip, reference specific pay code values and amounts from the retrieved data. If the question cannot be answered from the payslip data, clearly state the limitation and suggest the employee contact HR Ops."
- [x] Implement graceful escalation: when the agent cannot answer a follow-up question with confidence, return a structured response with `escalate: true` and a suggested HR Ops contact message

### REQ-05 — Translated Payslip PDF Generation

- [x] Implement `generate_payslip_pdf` tool: accept the translated payslip data structure, employee name, pay period, and target language; generate a formatted PDF document containing a header, translated pay code table (columns: original code, translated label, explanation, amount), totals row, and a mandatory disclaimer: "This document is an AI-generated translation for informational purposes only. The original payslip in SAP S/4HANA is the authoritative record."
- [x] Add `reportlab` or `fpdf2` to `requirements.txt` for PDF generation (no external PDF service)
- [x] Return the PDF as a base64-encoded string with a suggested filename in the tool response so the calling interface can offer a download
- [x] The disclaimer must appear in both the target language AND English on every generated PDF

### REQ-06 — Payslip Period Comparison

- [x] Implement `compare_payslips` tool: accept `employee_id`, `period_1` (YYYY-MM), `period_2` (YYYY-MM), and `target_language`; retrieve both payslips, translate both, and return a structured comparison object containing: `added_codes` (present in period_2, absent in period_1), `removed_codes` (absent in period_2, present in period_1), `changed_codes` (present in both, amount changed with delta), `unchanged_codes`
- [x] Load the `payslip-comparison` skill when handling comparison requests
- [x] Format the comparison result clearly for the user, highlighting financial impact (sum of additions, sum of removals, net change)

### REQ-07 — Role-Based Data Access Control

- [x] Add access control logic to the agent's system prompt: "You have two user roles: `employee` and `hr_ops`. An `employee` may only access their own payslip (their `employee_id` is provided in the session context). An `hr_ops` user may access any employee's payslip. Never return another employee's payslip data to an `employee` role user under any circumstances."
- [x] Log all payslip data access events with the pattern: `ACCESS: role={role}, accessed_employee_id={id}, action={action}, timestamp={ts}`
- [x] If an employee attempts to access another employee's payslip, return a clear denial message and log: `ACCESS_DENIED: employee {requesting_id} attempted to access {target_id}`

### REQ-08 — Proactive Anomaly Flagging (High-Want)

- [x] Implement anomaly detection in `translate_and_explain_payslip`: compare current period amounts to prior period amounts (if available) and flag any pay code where the amount changed by more than 15% or where a new deduction code appeared; surface these as `anomalies[]` in the tool response
- [x] Present flagged anomalies at the start of the translated payslip response: "I noticed the following changes compared to last month: [list]. Would you like me to explain any of these?"

### REQ-09 — Language Auto-Detection (High-Want)

- [x] Add system prompt instruction: "Detect the language the user is writing in and respond in that language. If the user has not specified a target language for the payslip translation, use their detected input language as the default target language."

---

## Data Dependencies

No Data Product ORD IDs — API integration via MCP servers.

**APIs integrated:**

- `sap.sf:apiResource:ECEmployeeCentralPayroll:v1` — payslip line items, pay codes, amounts
- `sap.sf:apiResource:ECCompensationInformation:v1` — compensation details, pay grade context

**API spec files:**

- `specification/payslip-translation-agent/api-specs/ECEmployeeCentralPayroll.edmx`
- `specification/payslip-translation-agent/api-specs/ECCompensationInformation.edmx`

**MCP tool scope:**

```text
MCP API: sap.sf:apiResource:ECEmployeeCentralPayroll:v1
MCP tool scope: read-only
Resources in scope: PayrollTimeSheetActivity, EmployeePayrollRunResults, PayComponentRecurring, PayComponentNonRecurring
```

```text
MCP API: sap.sf:apiResource:ECCompensationInformation:v1
MCP tool scope: read-only
Resources in scope: CompensationInformation, CompensationInformationNav, CompensationSalaryRateType
```

---

## Business Instrumentation

- [x] Implement structured logging and OpenTelemetry spans for all 5 milestones from the PRD:

  **M1 — Payroll Data Retrieval:**
  - Log on achievement: `M1.achieved: payslip data retrieved successfully for employee {employee_id}, period {pay_period}, {pay_code_count} pay codes found`
  - Log on miss: `M1.missed: payslip data retrieval failed for employee {employee_id}, period {pay_period} — reason: {error_reason}`

  **M2 — Pay Code Translation:**
  - Log on achievement: `M2.achieved: {pay_code_count} pay codes translated to {target_language} for employee {employee_id}`
  - Log on miss: `M2.missed: translation incomplete for employee {employee_id} — {untranslated_count} pay codes could not be translated to {target_language}`

  **M3 — Plain-Language Explanation:**
  - Log on achievement: `M3.achieved: plain-language explanations generated for all {pay_code_count} pay codes in {target_language}`
  - Log on miss: `M3.missed: explanation generation incomplete — {unexplained_count} pay codes missing explanations for employee {employee_id}`

  **M4 — Follow-up Q&A:**
  - Log on achievement: `M4.achieved: follow-up question answered for employee {employee_id}, question topic: {topic}`
  - Log on miss: `M4.missed: follow-up question could not be answered for employee {employee_id} — escalated to HR Ops`

  **M5 — Translated Document & Period Comparison:**
  - Log on achievement: `M5.achieved: {action} completed for employee {employee_id} — action: [pdf_generated | period_comparison]`
  - Log on miss: `M5.missed: {action} failed for employee {employee_id} — reason: {error_reason}`

- [x] Use `@tracer.start_as_current_span` decorator on regular async helper methods (not inside generators)
- [x] Extract all business logic from `stream()` into a plain async helper `_run_agent()` and instrument that method
- [x] Verify `bootstrap(app)` is called after `app = server.build()` in `main.py`

---

## MCP Tool Integration

- [x] Verify `specification/payslip-translation-agent/api-specs/ECEmployeeCentralPayroll.edmx` and `ECCompensationInformation.edmx` exist (downloaded in spec generation step)
- [x] Invoke `mcp-translation-file` skill for `ECEmployeeCentralPayroll.edmx` — outputs to `specification/payslip-translation-agent/mcps/ECEmployeeCentralPayroll/`
- [x] Invoke `mcp-translation-file` skill for `ECCompensationInformation.edmx` — outputs to `specification/payslip-translation-agent/mcps/ECCompensationInformation/`
- [x] Invoke `setup-solution` skill to register both MCP server assets in `solution.yaml`
- [x] Extract the exact `ordId` values from the generated `asset.yaml` files for both MCP servers — do NOT invent ORD IDs
- [x] Wire MCP tool loading in `agent.py` using `get_mcp_tools()` from the `mcp_tools` module (bootstrap-generated indirection layer) — see `guidelines-agent-python.md` for canonical pattern
- [x] Add both MCP server entries to `assets/payslip-translation-agent/asset.yaml` under `requires` using the exact ORD IDs from the generated assets
- [x] Lastly, generate `mcp-mock.json` using the `mcp-mock-config` skill (required before tests can run)

---

## Testing

- [x] `conftest.py` sets only `IBD_TESTING=true` — the fixture monkey-patches `mcp_tools.get_mcp_tools` to use mock data from `mcp-mock.json`
- [x] Write unit test for `get_payslip` tool: mock MCP tool response with a sample payslip containing 5 pay codes; assert all pay codes are returned correctly
- [x] Write unit test for `get_compensation_details` tool: mock MCP tool response; assert compensation fields are returned
- [x] Write unit test for `translate_and_explain_payslip` tool: mock LLM response; assert each pay code has `translated_label`, `plain_language_explanation`, `amount`, `currency`, and `confidence` fields
- [x] Write unit test for `generate_payslip_pdf` tool: assert PDF bytes are returned as base64, filename is included, and disclaimer text is present in the PDF
- [x] Write unit test for `compare_payslips` tool: mock two payslips with one added code, one removed code, and one changed amount; assert the comparison output correctly categorises all three
- [x] Write unit test for access control: assert employee role cannot request payslip for a different employee ID; assert hr_ops role can
- [x] Write one integration test: end-to-end agent flow where a user asks for their payslip in French, then asks a follow-up question about a deduction, then requests a PDF — mock LLM and MCP tool responses; assert all three milestones M1, M2, M3 log messages are emitted
- [x] Run `pytest` from `assets/payslip-translation-agent/` (no args) — fix any failures before proceeding
- [x] If coverage < 70%, add targeted tests until threshold is met
- [x] Run `pytest` again from `assets/payslip-translation-agent/` (no args) to generate final `test_report.json`
- [x] Verify `test_report.json` exists in `assets/payslip-translation-agent/`
