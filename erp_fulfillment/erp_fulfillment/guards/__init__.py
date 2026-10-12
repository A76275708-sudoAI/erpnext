"""Hard guards G1/G2 (+ G3 stubs). Pure-Python core; Frappe raise when available."""

from erp_fulfillment.guards.platform_push import (
    ERR_OFFLINE_PUSH,
    assert_platform_push_allowed,
    is_offline_channel,
)
from erp_fulfillment.guards.delivery_note_cancel import (
    ERR_DN_CANCEL,
    assert_delivery_note_cancel_allowed,
)

__all__ = [
    "ERR_OFFLINE_PUSH",
    "ERR_DN_CANCEL",
    "is_offline_channel",
    "assert_platform_push_allowed",
    "assert_delivery_note_cancel_allowed",
]
