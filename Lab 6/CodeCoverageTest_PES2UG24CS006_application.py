%%writefile CodeCoverageTest_PES2UG24CS006_application.py
import pytest
from shipping_quote import process_shipments, monitor_container_pressures


def test_invalid_shipments_input():
    with pytest.raises(ValueError):
        process_shipments("invalid", 20.0)


def test_negative_handling_fee():
    with pytest.raises(ValueError):
        process_shipments([], -1.0)


def test_ground_air_and_express_quotes():
    shipments = [
        {
            "manifest_approved": True,
            "mode": "ground",
            "is_fragile": False,
            "express_priority": False,
            "packages": [
                {"weight_kg": 10, "is_hazmat": False},
                {"weight_kg": 40, "is_hazmat": False},
            ],
        },
        {
            "manifest_approved": True,
            "mode": "air",
            "is_fragile": False,
            "express_priority": True,
            "packages": [
                {"weight_kg": 5, "is_hazmat": False}
            ],
        },
    ]

    result = process_shipments(shipments, 20.0)
    assert result == {
        "total_quote": 400.0,
        "status": "CLEARED",
    }


def test_unapproved_and_unsupported_shipments():
    shipments = [
        {"manifest_approved": False},
        {"manifest_approved": True, "mode": "sea"},
    ]

    result = process_shipments(shipments, 20.0)
    assert result["status"] == "NO_CARGO"
    assert result["total_quote"] == 0.0


def test_hazardous_and_fragile_packages():
    shipments = [
        {
            "manifest_approved": True,
            "mode": "ground",
            "is_fragile": False,
            "packages": [
                {"weight_kg": 2, "is_hazmat": True}
            ],
        },
        {
            "manifest_approved": True,
            "mode": "air",
            "is_fragile": True,
            "packages": [
                {"weight_kg": 2, "is_hazmat": True}
            ],
        },
    ]

    result = process_shipments(shipments, 10.0)
    assert result["total_quote"] == 60.0
    assert result["status"] == "CLEARED"


def test_invalid_package_weights():
    shipments = [
        {
            "manifest_approved": True,
            "mode": "ground",
            "packages": [
                {"weight_kg": 0},
                {"weight_kg": -1},
                {"weight_kg": 0},
                {"weight_kg": -5},
            ],
        }
    ]

    result = process_shipments(shipments, 10.0)
    assert result["status"] == "FLAGGED_REVIEW"
    assert result["total_quote"] == 10.0


def test_empty_shipments_return_no_cargo():
    result = process_shipments([], 20.0)
    assert result == {
        "total_quote": 0.0,
        "status": "NO_CARGO",
    }


def test_empty_pressure_logs():
    assert monitor_container_pressures([]) == "NO_DATA"


def test_consecutive_low_pressures_detect_leak():
    assert monitor_container_pressures([[13.0, 12.0]]) == "LEAK_DETECTED"


def test_pressure_recovery_resets_streak():
    assert monitor_container_pressures([[13.0, 14.0, 13.0]]) == "STABLE"


def test_stable_container_pressure():
    assert monitor_container_pressures([[15.0, 15.0, 16.0]]) == "STABLE"
