#!/usr/bin/env python3
"""Offline smoke checks for G1/G2/G3 without Frappe or bench."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from erp_fulfillment.guards import (  # noqa: E402
    ERR_DN_CANCEL,
    ERR_OFFLINE_PUSH,
    assert_delivery_note_cancel_allowed,
    assert_platform_push_allowed,
    is_offline_channel,
)
from erp_fulfillment.guards.sales_order_validate import validate_sales_order  # noqa: E402
from erp_fulfillment.adapters.mock_channel.push_shipment import (  # noqa: E402
    push_platform_shipment,
)


def expect_perm(fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except PermissionError as e:
        return str(e)
    raise AssertionError(f"expected PermissionError from {fn.__name__}")


def main() -> int:
    assert is_offline_channel("OFFLINE_MOCK")
    assert not is_offline_channel("EC_MOCK")

    msg = expect_perm(assert_platform_push_allowed, "OFFLINE_MOCK", 0)
    assert ERR_OFFLINE_PUSH in msg, msg

    msg = expect_perm(assert_platform_push_allowed, "EC_MOCK", 0)
    assert ERR_OFFLINE_PUSH in msg, msg

    assert_platform_push_allowed("EC_MOCK", 1)  # must pass

    msg = expect_perm(assert_delivery_note_cancel_allowed, False)
    assert ERR_DN_CANCEL in msg, msg
    assert_delivery_note_cancel_allowed(allow_admin_override=True)

    expect_perm(
        validate_sales_order,
        {"channel_type": "OFFLINE_MOCK", "platform_order_no": "X", "requires_platform_push": 0},
    )
    expect_perm(
        validate_sales_order,
        {"channel_type": "EC_MOCK", "platform_order_no": "", "shop_id": "", "requires_platform_push": 1},
    )
    validate_sales_order(
        {
            "channel_type": "EC_MOCK",
            "platform_order_no": "PO-1",
            "shop_id": "S1",
            "requires_platform_push": 1,
        }
    )

    expect_perm(
        push_platform_shipment,
        channel_type="OFFLINE_MOCK",
        requires_platform_push=0,
        doc_no="SO-1",
        tracking_no="T1",
    )
    ok = push_platform_shipment(
        channel_type="EC_MOCK",
        requires_platform_push=1,
        doc_no="SO-2",
        tracking_no="T2",
    )
    assert ok["push_status"] == "MOCK_OK"

    print("check_guards_offline: ALL PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
