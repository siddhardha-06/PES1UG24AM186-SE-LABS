"""Tests aimed at LINE coverage of blood_donation_screening.py (Lab 6)."""
import pytest
from blood_donation_screening import (
    process_donor_cohort,
    verify_storage_centrifuge,
)

GOOD = {"age": 25, "weight_kg": 65, "hb": 14.0}


def make_cohort(donors, registered=True, cohort_type="standard",
                fast_track=False):
    """Build a cohort dictionary for the tests."""
    return {
        "clinic_registered": registered,
        "type": cohort_type,
        "fast_track": fast_track,
        "donors": donors,
    }


def test_single_accepted_donor():
    result = process_donor_cohort([make_cohort([GOOD])], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_invalid_cohort_list_raises():
    with pytest.raises(ValueError):
        process_donor_cohort("not a list", 450)


def test_unregistered_cohort_is_skipped():
    result = process_donor_cohort([make_cohort([GOOD], registered=False)], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_underage_donor_is_deferred():
    young = {"age": 16, "weight_kg": 65, "hb": 14.0}
    result = process_donor_cohort([make_cohort([young, GOOD])], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_low_hemoglobin_high_altitude_resets_total():
    low = {"age": 30, "weight_kg": 70, "hb": 11.0}
    cohort = make_cohort([GOOD, low, GOOD], cohort_type="high_altitude")
    result = process_donor_cohort([cohort], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_high_deferral_status():
    young = {"age": 16, "weight_kg": 65, "hb": 14.0}
    result = process_donor_cohort([make_cohort([young] * 5 + [GOOD])], 450)
    assert result == {"collected_ml": 450, "status": "HIGH_DEFERRAL"}


def test_centrifuge_no_data():
    assert verify_storage_centrifuge([]) == "NO_DATA"


def test_centrifuge_abort_on_two_low_readings():
    assert verify_storage_centrifuge([[3500, 2900, 2800]]) == "ABORT_SPIN"


def test_centrifuge_stable():
    assert verify_storage_centrifuge([[3500, 3600, 3400]]) == "STABLE"
