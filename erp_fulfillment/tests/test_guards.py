"""pytest-compatible offline guard tests (no Frappe)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from erp_fulfillment.guards import (
    ERR_DN_CANCEL,
    ERR_OFFLINE_PUSH,
    assert_delivery_note_cancel_allowed,
    assert_platform_push_allowed,
    is_offline_channel,
)
from erp_fulfillment.guards.sales_order_validate import validate_sales_order
from erp_fulfillment.adapters.mock_channel.push_shipment import push_platform_shipment


def test_offline_prefix():
    assert is_offline_channel("OFFLINE_POS")
    assert not is_offline_channel("EC_TAOBAO")
    assert not is_offline_channel(None)


def test_g1_rejects_offline():
    with pytest.raises(PermissionError, match=ERR_OFFLINE_PUSH):
        assert_platform_push_allowed("OFFLINE_MOCK", 0)


def test_g1_rejects_push_flag_zero():
    with pytest.raises(PermissionError, match=ERR_OFFLINE_PUSH):
        assert_platform_push_allowed("EC_MOCK", 0)


def test_g1_allows_ec():
    assert_platform_push_allowed("EC_MOCK", 1)


def test_g2_default_ban():
    with pytest.raises(PermissionError, match=ERR_DN_CANCEL):
        assert_delivery_note_cancel_allowed(False)


def test_g2_admin_override():
    assert_delivery_note_cancel_allowed(True)


def test_g3a_offline_platform_no():
    with pytest.raises(PermissionError, match="OFFLINE_PLATFORM_ORDER_NO"):
        validate_sales_order(
            {
                "channel_type": "OFFLINE_DEALER",
                "platform_order_no": "BAD",
                "requires_platform_push": 0,
            }
        )


def test_push_adapter_uses_g1():
    with pytest.raises(PermissionError, match=ERR_OFFLINE_PUSH):
        push_platform_shipment(
            channel_type="OFFLINE_PHONE",
            requires_platform_push=0,
            doc_no="SO-9",
            tracking_no="X",
        )
