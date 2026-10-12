"""B5 — Mock label print queue state machine (no printer hardware)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

PrintState = Literal["queued", "printing", "printed", "failed"]


@dataclass
class LabelJob:
    doc_no: str
    template_version: str = "v1"
    printer_id: str = "MOCK-PRINTER-1"
    reprint_count: int = 0
    state: PrintState = "queued"
    pdf_bytes: bytes = field(default=b"%PDF-MOCK")


def enqueue_label(doc_no: str, template_version: str = "v1") -> LabelJob:
    return LabelJob(doc_no=doc_no, template_version=template_version)


def mark_printed(job: LabelJob, *, is_reprint: bool = False) -> LabelJob:
    if is_reprint:
        job.reprint_count += 1
    job.state = "printed"
    return job


def assert_reprint_bumped(job: LabelJob, previous_count: int) -> None:
    """G3c stub: explicit reprint must bump reprint_count."""
    if job.reprint_count <= previous_count:
        raise PermissionError(
            "ERP_V1_REPRINT_COUNT_REQUIRED: reprint must increment reprint_count"
        )
