---
name: payslip-comparison
description: Step-by-step instructions for comparing two payslips across periods - retrieve both, align pay codes, highlight additions, removals, and amount changes.
---

# Payslip Comparison Skill

## When to Use This Skill

Load this skill when the user asks to:
- Compare two payslips from different pay periods
- Find out what changed between two months
- Understand why their net pay changed
- See which pay codes were added or removed

## Prerequisites

- `employee_id` must be available in session context
- Two pay periods must be identified (YYYY-MM format)
- `target_language` must be known

## Instructions

### Step 1: Retrieve Both Payslips

1. Call the `get_payslip` MCP tool for `period_1`.
2. Call the `get_payslip` MCP tool for `period_2`.
3. If either call fails, stop and report the error to the user.

### Step 2: Align Pay Codes

1. Build a map of all unique pay codes across both periods.
2. Categorise each pay code:
   - **Added**: present in period_2, absent in period_1
   - **Removed**: present in period_1, absent in period_2
   - **Changed**: present in both, different amount (compute delta = period_2 amount − period_1 amount)
   - **Unchanged**: present in both, same amount

### Step 3: Translate All Codes

1. Translate all pay code labels for both periods into the target language.
2. Use the payslip-translation skill for translation guidance.

### Step 4: Present Comparison

Present results in the following order:

1. **Summary**: Net pay period_1 → period_2, overall change amount and direction
2. **Added Pay Codes table**: Code | Translated Label | Amount (period_2)
3. **Removed Pay Codes table**: Code | Translated Label | Amount (period_1)
4. **Changed Pay Codes table**: Code | Translated Label | Period 1 Amount | Period 2 Amount | Change (Δ)
5. **Unchanged Pay Codes**: Brief note on count of unchanged codes

### Step 5: Highlight Financial Impact

- Sum of all additions
- Sum of all removals
- Net change in gross pay
- Net change in total deductions
- Net change in net pay

Log: `M5.achieved: period_comparison completed for employee {employee_id}`

### Step 6: Offer Follow-up

Ask: "Would you like me to explain any of these changes in more detail?"

## Error Handling

- If one period has no payslip data: Inform the user and suggest they verify the pay period with HR Ops.
- If a pay code changed by more than 15%: Proactively highlight it as a significant change.
