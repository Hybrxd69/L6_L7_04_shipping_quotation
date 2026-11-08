from hypothesis import given, strategies as st
from processor import (
    calculate_dimensional_weight,
    format_tracking_label,
    parse_package_manifest,
)


@given(st.text() | st.none())
def test_calculate_dimensional_weight_no_crash(value):
    try:
        result = calculate_dimensional_weight(value)
    except (AttributeError, IndexError, TypeError, ValueError, OverflowError):
        return
    assert isinstance(result, float)


@given(st.text() | st.none())
def test_format_tracking_label_safe(value):
    try:
        result = format_tracking_label(value)
    except (AttributeError, IndexError, TypeError, ValueError, OverflowError):
        return
    assert isinstance(result, str)
    assert len(result) >= 8
    assert result[1] == "-"


@given(st.text() | st.none())
def test_parse_package_manifest_safe(value):
    try:
        result = parse_package_manifest(value)
    except (AttributeError, TypeError, ValueError, KeyError, OverflowError):
        return
    assert isinstance(result, float)