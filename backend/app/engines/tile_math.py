"""Floor tile order count: area method + optional grid layout preview."""

import math

from app.engines.helpers import ceil_units


def tile_count(
    room_l: float,
    room_w: float,
    tile_l: float,
    tile_w: float,
    waste_pct: float,
    gap_m: float = 0.0,
) -> dict:
    """
    raw_count: ceil(room_area / effective_tile_piece_area)
    order_count: ceil(raw * (1 + waste_pct/100))

    Effective tile edge = tile edge - grout gap (gap_m, meters).
    """
    area = float(room_l) * float(room_w)
    if area < 0 or not math.isfinite(area):
        raise ValueError("invalid dimensions")
    if not math.isfinite(float(gap_m)) or float(gap_m) < 0:
        raise ValueError("gap width must not be negative")
    eff_l = float(tile_l) - float(gap_m)
    eff_w = float(tile_w) - float(gap_m)
    piece = eff_l * eff_w
    if eff_l <= 0 or eff_w <= 0 or piece <= 0:
        raise ValueError("gap width must be smaller than tile edge")
    raw = ceil_units(area / piece)
    with_waste = ceil_units(raw * (1 + float(waste_pct) / 100.0))
    layout = layout_preview(room_l, room_w, eff_l, eff_w)
    return {
        "area_m2": round(area, 3),
        "piece_m2": round(piece, 4),
        "raw_count": raw,
        "waste_pct": float(waste_pct),
        "order_count": with_waste,
        "layout": layout,
    }


def layout_preview(room_l: float, room_w: float, tile_l: float, tile_w: float) -> dict:
    """Grid count if tiles are laid on a full rectangular lattice (may exceed area method)."""
    cols = ceil_units(float(room_l) / float(tile_l))
    rows = ceil_units(float(room_w) / float(tile_w))
    grid_count = cols * rows
    return {
        "cols": cols,
        "rows": rows,
        "grid_count": grid_count,
    }
