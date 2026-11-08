"""
Tests for CLI sparkline renderer and self-check.
"""

from bio_sync.cli import render_sparkline


def test_render_sparkline():
    line_min = render_sparkline(-1.0, width=10)
    assert line_min == "O---------"

    line_max = render_sparkline(1.0, width=10)
    assert line_max == "---------O"

    line_mid = render_sparkline(0.0, width=11)
    assert "O" in line_mid
    assert len(line_mid) == 11
