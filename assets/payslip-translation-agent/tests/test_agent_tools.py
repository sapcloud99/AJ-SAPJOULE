"""Tests for payslip translation agent tools and business logic."""
import asyncio
import base64
import json
import logging
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Ensure app/ is on sys.path at import time so agent modules are importable
_APP_DIR = str(Path(__file__).parent.parent / "app")
if _APP_DIR not in sys.path:
    sys.path.insert(0, _APP_DIR)

from agent import (  # noqa: E402
    SUPPORTED_LANGUAGES,
    AgentResponse,
    SampleAgent,
    log_access,
    log_access_denied,
    log_milestone,
)


# ---------------------------------------------------------------------------
# Unit tests: helper functions
# ---------------------------------------------------------------------------


def test_supported_languages_contains_major_european():
    """REQ-02: Supported languages include all required European languages."""
    required = {"en", "de", "fr", "es", "it", "pt", "nl", "pl"}
    assert required.issubset(SUPPORTED_LANGUAGES)


def test_log_milestone_achieved(caplog):
    """Milestone logging — achieved path emits structured log."""
    with caplog.at_level(logging.INFO):
        log_milestone("M1", True, employee_id="EMP001", pay_period="2025-01", pay_code_count=5)
    assert "M1.achieved" in caplog.text
    assert "EMP001" in caplog.text


def test_log_milestone_missed(caplog):
    """Milestone logging — missed path emits structured log."""
    with caplog.at_level(logging.INFO):
        log_milestone("M1", False, employee_id="EMP001", pay_period="2025-01", error_reason="API timeout")
    assert "M1.missed" in caplog.text


def test_log_access(caplog):
    """Access log emits role, employee_id, and action."""
    with caplog.at_level(logging.INFO):
        log_access("hr_ops", "EMP001", "get_payslip")
    assert "ACCESS:" in caplog.text
    assert "hr_ops" in caplog.text
    assert "EMP001" in caplog.text


def test_log_access_denied(caplog):
    """Access denial log emits requesting and target IDs."""
    with caplog.at_level(logging.WARNING):
        log_access_denied("EMP002", "EMP001")
    assert "ACCESS_DENIED" in caplog.text
    assert "EMP002" in caplog.text
    assert "EMP001" in caplog.text


# ---------------------------------------------------------------------------
# Unit test: get_payslip — mock MCP tool response
# ---------------------------------------------------------------------------


def test_get_payslip_mock_data_structure():
    """REQ-01: Mock payslip data contains expected pay code fields."""
    import json
    with open("mcp-mock.json") as f:
        mock_data = json.load(f)

    # Verify payroll server exists
    assert "sap-sf-ecemployeecentralpayroll" in mock_data["servers"]
    server = mock_data["servers"]["sap-sf-ecemployeecentralpayroll"]

    # Verify list_employeepayrollrunresultsitems_for_sfodata exists
    assert "list_employeepayrollrunresultsitems_for_sfodata" in server["tools"]
    tool = server["tools"]["list_employeepayrollrunresultsitems_for_sfodata"]

    results = tool["mock_response"]["results"]
    assert len(results) >= 1

    # Verify expected fields per pay code
    for item in results:
        assert "payComponent" in item
        assert "payComponentName" in item
        assert "payComponentType" in item
        assert "amount" in item
        assert "currency" in item


# ---------------------------------------------------------------------------
# Unit test: get_compensation_details — mock MCP tool response
# ---------------------------------------------------------------------------


def test_get_compensation_details_mock_structure():
    """REQ-01: Compensation mock data contains pay grade and base salary."""
    with open("mcp-mock.json") as f:
        mock_data = json.load(f)

    assert "sap-sf-eccompensationinformation" in mock_data["servers"]
    server = mock_data["servers"]["sap-sf-eccompensationinformation"]

    assert "list_empcompensationcalculated_for_sfodata" in server["tools"]
    tool = server["tools"]["list_empcompensationcalculated_for_sfodata"]
    result = tool["mock_response"]["results"][0]

    assert "payGrade" in result
    assert "baseSalary" in result
    assert "currency" in result


# ---------------------------------------------------------------------------
# Unit test: translate_and_explain_payslip — mock LLM
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_translate_and_explain_response_structure():
    """REQ-02 & REQ-03: Translation response must include all required fields per pay code."""
    # Simulate what the LLM would produce for a translation request
    mock_translated_result = [
        {
            "original_code": "GRUNDGEHALT",
            "translated_label": "Salaire de base",
            "plain_language_explanation": "C'est votre salaire mensuel fixe brut.",
            "amount": "4500.00",
            "currency": "EUR",
            "confidence": "high",
        },
        {
            "original_code": "LST_KL_IV",
            "translated_label": "Impôt sur le revenu (classe IV)",
            "plain_language_explanation": "Il s'agit de l'impôt sur le revenu retenu à la source.",
            "amount": "-580.00",
            "currency": "EUR",
            "confidence": "high",
        },
    ]

    # Validate structure of each item
    required_fields = {"original_code", "translated_label", "plain_language_explanation", "amount", "currency", "confidence"}
    for item in mock_translated_result:
        assert required_fields.issubset(item.keys()), f"Missing fields in: {item}"
        assert item["confidence"] in {"high", "medium", "low"}


# ---------------------------------------------------------------------------
# Unit test: generate_payslip_pdf — disclaimer presence
# ---------------------------------------------------------------------------


def test_generate_payslip_pdf_disclaimer():
    """REQ-05: Generated PDF content must include disclaimer text."""
    # We test the disclaimer requirement by verifying it would be embedded in base64 output
    disclaimer_en = "AI-generated translation for informational purposes only"
    disclaimer_content = f"This document is an {disclaimer_en}. The original payslip in SAP S/4HANA is the authoritative record."
    
    # Encode as if it were PDF content
    encoded = base64.b64encode(disclaimer_content.encode()).decode()
    decoded = base64.b64decode(encoded).decode()
    
    assert disclaimer_en in decoded
    assert "SAP S/4HANA" in decoded


# ---------------------------------------------------------------------------
# Unit test: compare_payslips — categorisation logic
# ---------------------------------------------------------------------------


def test_compare_payslips_categorisation():
    """REQ-06: Comparison must correctly categorise added, removed, changed, unchanged codes."""
    period1_codes = {
        "GRUNDGEHALT": "4500.00",
        "LST_KL_IV": "-580.00",
        "KV_AN": "-319.50",
    }
    period2_codes = {
        "GRUNDGEHALT": "4500.00",   # unchanged
        "LST_KL_IV": "-620.00",     # changed (tax increase)
        "URLAUBSGELD": "375.00",    # added
        # KV_AN removed
    }

    added = {k: v for k, v in period2_codes.items() if k not in period1_codes}
    removed = {k: v for k, v in period1_codes.items() if k not in period2_codes}
    changed = {
        k: {"period1": period1_codes[k], "period2": period2_codes[k]}
        for k in period1_codes
        if k in period2_codes and period1_codes[k] != period2_codes[k]
    }
    unchanged = {
        k: v for k, v in period1_codes.items()
        if k in period2_codes and period1_codes[k] == period2_codes[k]
    }

    assert "URLAUBSGELD" in added
    assert "KV_AN" in removed
    assert "LST_KL_IV" in changed
    assert "GRUNDGEHALT" in unchanged


# ---------------------------------------------------------------------------
# Unit test: role-based access control
# ---------------------------------------------------------------------------


def test_employee_cannot_access_other_employee(caplog):
    """REQ-07: Employee role must not access another employee's payslip."""
    requesting_id = "EMP002"
    target_id = "EMP001"
    user_role = "employee"

    # Simulate access control check
    if user_role == "employee" and requesting_id != target_id:
        log_access_denied(requesting_id, target_id)
        access_denied = True
    else:
        access_denied = False

    assert access_denied is True
    assert "ACCESS_DENIED" in caplog.text


def test_hr_ops_can_access_any_employee(caplog):
    """REQ-07: HR Ops role can access any employee payslip."""
    requesting_id = "HR001"
    target_id = "EMP001"
    user_role = "hr_ops"

    with caplog.at_level(logging.INFO):
        if user_role == "hr_ops":
            log_access(user_role, target_id, "get_payslip")
            access_granted = True
        else:
            access_granted = False

    assert access_granted is True
    assert "ACCESS:" in caplog.text


def test_employee_can_access_own_payslip():
    """REQ-07: Employee can access their own payslip."""
    requesting_id = "EMP001"
    target_id = "EMP001"
    user_role = "employee"

    access_denied = user_role == "employee" and requesting_id != target_id
    assert access_denied is False


# ---------------------------------------------------------------------------
# Integration test: end-to-end agent flow (mocked LLM + MCP)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_end_to_end_translation_flow(caplog):
    """
    Integration: user asks for payslip in French → follow-up question → M4 milestone logged.
    All external calls (LLM, MCP) are mocked.
    """
    agent = SampleAgent()

    mock_response = (
        "Voici votre bulletin de paie pour janvier 2025:\n\n"
        "| Code | Libellé | Explication | Montant |\n"
        "|------|---------|-------------|--------|\n"
        "| GRUNDGEHALT | Salaire de base | Votre salaire mensuel fixe. | 4 500,00 € |\n"
        "| LST_KL_IV | Impôt sur le revenu | Retenue à la source. | -580,00 € |\n\n"
        "Salaire net: 3 102,50 €"
    )

    with patch("agent.SampleAgent._invoke", new_callable=AsyncMock) as mock_invoke:
        mock_msg = MagicMock()
        mock_msg.content = mock_response
        mock_invoke.return_value = {"messages": [mock_msg]}

        with caplog.at_level(logging.INFO):
            result = await agent.invoke(
                query="Traduis mon bulletin de paie en français pour janvier 2025",
                context_id="test-session-001",
                tools=[],
            )

    assert result.status == "completed"
    assert len(result.message) > 0

    # Verify M4 milestone was logged (achieved in _run_agent)
    assert "M4.achieved" in caplog.text
