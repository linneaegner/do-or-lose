from constants import (
    CONTENT_MIN_WIDTH,
    CONTENT_WIDTH,
    CONTENT_WIDTH_WIDE,
    layout_metrics,
)


def test_layout_metrics_phone():
    metrics = layout_metrics(375)
    assert metrics["narrow"] is True
    assert metrics["wide"] is False
    assert metrics["content_width"] <= 375 - metrics["pad_x"] * 2
    assert metrics["content_width"] >= CONTENT_MIN_WIDTH


def test_layout_metrics_default():
    metrics = layout_metrics(480)
    assert metrics["narrow"] is False
    assert metrics["wide"] is False
    assert metrics["content_width"] == CONTENT_WIDTH


def test_layout_metrics_wide():
    metrics = layout_metrics(768)
    assert metrics["wide"] is True
    assert metrics["content_width"] == CONTENT_WIDTH_WIDE
