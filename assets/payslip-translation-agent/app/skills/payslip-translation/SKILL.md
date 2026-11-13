---
name: payslip-translation
description: Step-by-step instructions for retrieving, translating, and explaining an employee payslip including language detection, pay code lookup, and disclaimer injection.
---

# Payslip Translation Skill

## When to Use This Skill

Load this skill when the user asks to:
- Translate their payslip into a specific language
- Understand what a pay code means
- Get an explanation of their payslip components
- Generate a translated PDF payslip

## Prerequisites

Before starting:
- Confirm the employee_id is available in session context
- Confirm the pay_period is specified (YYYY-MM format; default to current month if not provided)
- Confirm the target_language is known (detect from user input language if not explicit)

## Supported Languages

| BCP-47 Code | Language    |
|-------------|-------------|
| en          | English     |
| de          | German      |
| fr          | French      |
| es          | Spanish     |
| it          | Italian     |
| pt          | Portuguese  |
| nl          | Dutch       |
| pl          | Polish      |

If the requested language is not in this list, inform the user politely and ask them to choose one of the supported languages.

## Instructions

### Step 1: Retrieve Payslip Data

1. Call the `get_payslip` MCP tool with `employee_id` and `pay_period`.
2. If the tool returns an error, stop and report the exact error to the user.
3. Log: `M1.achieved: payslip data retrieved successfully for employee {employee_id}, period {pay_period}, {pay_code_count} pay codes found`
4. If retrieval fails: `M1.missed: payslip data retrieval failed for employee {employee_id}, period {pay_period} — reason: {error_reason}`

### Step 2: Translate Pay Codes

1. For each pay code in the retrieved payslip, translate the label into the target language.
2. Use the pay code glossary (load `skills/payslip-translation/references/pay-code-glossary.md`) for common codes.
3. For legal and tax codes, use the precise legal terminology in the target language.
4. If a translation confidence is medium or low, set the confidence flag and note it for the user.
5. Log: `M2.achieved: {pay_code_count} pay codes translated to {target_language} for employee {employee_id}`
6. If incomplete: `M2.missed: translation incomplete for employee {employee_id} — {untranslated_count} pay codes could not be translated to {target_language}`

### Step 3: Generate Plain-Language Explanations

1. For each pay code, write a 1–3 sentence explanation in the target language.
2. Explain what the pay code represents and why it appears on the payslip.
3. Use simple, everyday language — avoid technical jargon.
4. Example: "This is your statutory pension contribution. It is required by law and funds your future retirement benefits."
5. Log: `M3.achieved: plain-language explanations generated for all {pay_code_count} pay codes in {target_language}`

### Step 4: Anomaly Detection

1. If prior period data is available, compare amounts.
2. Flag any pay code where the amount changed by more than 15% or where a new deduction code appeared.
3. Present flagged anomalies at the start of the response: "I noticed the following changes compared to last month: [list]."

### Step 5: Present Results

1. Present the translated payslip in a clear table format:
   - Column 1: Original Code
   - Column 2: Translated Label
   - Column 3: Plain-Language Explanation
   - Column 4: Amount
2. Show totals: Gross Pay, Total Deductions, Net Pay.
3. Ask if the user has follow-up questions.

### Step 6: PDF Generation (if requested)

1. Call the `generate_payslip_pdf` tool with the translated payslip data.
2. The PDF must include:
   - Employee name and pay period header
   - Translated pay code table
   - Totals row
   - Disclaimer in both target language and English: "This document is an AI-generated translation for informational purposes only. The original payslip in SAP S/4HANA is the authoritative record."
3. Return the download link or base64 content to the user.
4. Log: `M5.achieved: pdf_generated completed for employee {employee_id}`

## Error Handling

- If payslip data cannot be retrieved: Stop and direct the user to contact HR Ops.
- If translation fails for a specific code: Flag it as untranslated and continue with the rest.
- If PDF generation fails: Provide the translated content as text and note the PDF could not be generated.
