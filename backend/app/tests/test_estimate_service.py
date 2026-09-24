import pytest
from fastapi import HTTPException

from app.services import estimate_service

ROOM = {"id": 1, "length": 6.0, "width": 4.5, "data_quality": "clean"}
TILE = {"id": 1, "tile_l": 0.6, "tile_w": 0.6}


def _patch_lookups(monkeypatch, inserted):
    monkeypatch.setattr(estimate_service.rooms, "get_room", lambda rid: ROOM)
    monkeypatch.setattr(estimate_service.tiles, "get_tile", lambda tid: TILE)

    def fake_insert(room_id, tile_id, waste_pct, payload, note=""):
        inserted.append(
            {"room_id": room_id, "tile_id": tile_id, "waste_pct": waste_pct, "payload": payload}
        )
        return 1

    monkeypatch.setattr(estimate_service.history, "insert_run", fake_insert)


def test_invalid_gap_returns_422_and_never_inserts(monkeypatch):
    inserted = []
    _patch_lookups(monkeypatch, inserted)
    with pytest.raises(HTTPException) as exc_info:
        estimate_service.run_estimate(1, 1, 8.0, True, "n", gap_mm=600.0)
    assert exc_info.value.status_code == 422
    assert inserted == []


def test_gap_is_echoed_and_pinned_in_payload(monkeypatch):
    inserted = []
    _patch_lookups(monkeypatch, inserted)
    resp = estimate_service.run_estimate(1, 1, 8.0, True, "n", gap_mm=5.0)
    assert resp["gap_mm"] == 5.0
    assert resp["raw_count"] == 77
    assert resp["order_count"] == 84
    assert len(inserted) == 1
    payload = inserted[0]["payload"]
    assert payload["gap_mm"] == 5.0
    assert payload["raw_count"] == 77
    assert payload["order_count"] == 84


def test_none_gap_falls_back_to_settings_default(monkeypatch):
    inserted = []
    _patch_lookups(monkeypatch, inserted)
    monkeypatch.setattr(estimate_service.settings_repo, "get_gap_mm", lambda: 5.0)
    resp = estimate_service.run_estimate(1, 1, 8.0, False, "")
    assert resp["gap_mm"] == 5.0
    assert resp["raw_count"] == 77
    assert inserted == []
