
import pytest
from shipping_quote import process_shipments, monitor_container_pressures


def test_input_validation_branches():
    with pytest.raises(ValueError):
        process_shipments("invalid", 20.0)
    with pytest.raises(ValueError):
        process_shipments([], -1.0)


def test_manifest_and_transport_branches():
    shipments = [
        {"manifest_approved": False, "mode": "ground"},
        {"manifest_approved": True, "mode": "air",
         "packages": [{"weight_kg": 2}]},
        {"manifest_approved": True, "mode": "sea",
         "packages": [{"weight_kg": 2}]},
    ]
    result = process_shipments(shipments, 10.0)
    assert result["total_quote"] == 34.0
    assert result["status"] == "CLEARED"


def test_package_weight_branches():
    shipments = [{
        "manifest_approved": True,
        "mode": "ground",
        "packages": [
            {"weight_kg": 0},
            {"weight_kg": -2},
            {"weight_kg": 10},
            {"weight_kg": 40},
        ],
    }]
    result = process_shipments(shipments, 5.0)
    assert result["total_quote"] == 285.0
    assert result["status"] == "FLAGGED_REVIEW"


def test_hazmat_and_fragile_branches():
    shipments = [
        {"manifest_approved": True, "is_fragile": False,
         "packages": [{"weight_kg": 2, "is_hazmat": True}]},
        {"manifest_approved": True, "is_fragile": True,
         "packages": [{"weight_kg": 2, "is_hazmat": True}]},
    ]
    result = process_shipments(shipments, 10.0)
    assert result["total_quote"] == 60.0
    assert result["status"] == "CLEARED"


def test_express_and_regular_shipments():
    shipments = [
        {"manifest_approved": True, "mode": "ground",
         "express_priority": False, "packages": [{"weight_kg": 2}]},
        {"manifest_approved": True, "mode": "air",
         "express_priority": True, "packages": [{"weight_kg": 2}]},
    ]
    result = process_shipments(shipments, 10.0)
    assert result["total_quote"] == 60.5
    assert result["status"] == "CLEARED"


def test_rejected_parcel_threshold():
    shipments = [{
        "manifest_approved": True,
        "mode": "ground",
        "packages": [{"weight_kg": 0} for _ in range(4)],
    }]
    result = process_shipments(shipments, 10.0)
    assert result["status"] == "FLAGGED_REVIEW"


def test_no_cargo_and_cleared_status():
    assert process_shipments([], 10.0) == {
        "total_quote": 0.0, "status": "NO_CARGO"
    }
    result = process_shipments([{
        "manifest_approved": True,
        "mode": "ground",
        "packages": [{"weight_kg": 2}],
    }], 10.0)
    assert result["status"] == "CLEARED"


def test_pressure_monitoring_branches():
    assert monitor_container_pressures([]) == "NO_DATA"
    assert monitor_container_pressures([[15.0, 15.0, 16.0]]) == "STABLE"
    assert monitor_container_pressures([[13.0, 14.0, 13.0]]) == "STABLE"
    assert monitor_container_pressures([[13.0, 12.0]]) == "LEAK_DETECTED"
    assert monitor_container_pressures([[15.0, 12.0, 12.0]]) == "LEAK_DETECTED"
