"""Tests aimed at BRANCH coverage of blood_donation_screening.py (Lab 6).

Every decision in the module is exercised for both its True and False
outcome, including the boundary values (age 17, weight 50, hb 12.5 / 18.0,
rpm 3000).
"""
import pytest
from blood_donation_screening import (
    process_donor_cohort,
    verify_storage_centrifuge,
)

GOOD = {"age": 25, "weight_kg": 65, "hb": 14.0}
VOLUME = 450


def make_cohort(donors, registered=True, cohort_type="standard",
                fast_track=False):
    """Build a cohort dictionary for the tests."""
    return {
        "clinic_registered": registered,
        "type": cohort_type,
        "fast_track": fast_track,
        "donors": donors,
    }


def donor(age=25, weight=65, hb=14.0):
    """Build a donor dictionary for the tests."""
    return {"age": age, "weight_kg": weight, "hb": hb}


# ---- input validation -------------------------------------------------
def test_single_accepted_donor():
    result = process_donor_cohort([make_cohort([GOOD])], VOLUME)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


@pytest.mark.parametrize("cohorts, volume", [
    ("not a list", 450),
    (None, 450),
    ([make_cohort([GOOD])], 0),
    ([make_cohort([GOOD])], -10),
])
def test_invalid_input_raises(cohorts, volume):
    with pytest.raises(ValueError):
        process_donor_cohort(cohorts, volume)


# ---- cohort level branches -------------------------------------------
def test_unregistered_cohort_is_skipped():
    result = process_donor_cohort([make_cohort([GOOD], registered=False)],
                                  VOLUME)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_cohort_missing_registration_key_is_skipped():
    result = process_donor_cohort([{"donors": [GOOD]}], VOLUME)
    assert result["status"] == "ZERO_YIELD"


def test_cohort_defaults_type_and_donors():
    result = process_donor_cohort([{"clinic_registered": True}], VOLUME)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_empty_cohort_list_is_zero_yield():
    assert process_donor_cohort([], VOLUME) == {
        "collected_ml": 0, "status": "ZERO_YIELD"}


def test_fast_track_adds_bonus_volume():
    result = process_donor_cohort([make_cohort([GOOD], fast_track=True)],
                                  VOLUME)
    assert result == {"collected_ml": 500, "status": "ACCEPTED"}


def test_fast_track_bonus_applies_even_with_no_donors():
    result = process_donor_cohort([make_cohort([], fast_track=True)], VOLUME)
    assert result == {"collected_ml": 50, "status": "ACCEPTED"}


def test_multiple_cohorts_accumulate():
    cohorts = [make_cohort([GOOD]), make_cohort([GOOD, GOOD])]
    result = process_donor_cohort(cohorts, VOLUME)
    assert result["collected_ml"] == 1350


# ---- donor eligibility: age / weight ---------------------------------
def test_underage_donor_is_deferred():
    result = process_donor_cohort([make_cohort([donor(age=16), GOOD])],
                                  VOLUME)
    assert result["collected_ml"] == 450


def test_underweight_donor_is_deferred():
    result = process_donor_cohort([make_cohort([donor(weight=49), GOOD])],
                                  VOLUME)
    assert result["collected_ml"] == 450


def test_minimum_age_and_weight_are_accepted():
    result = process_donor_cohort([make_cohort([donor(age=17, weight=50)])],
                                  VOLUME)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_donor_missing_fields_is_deferred():
    result = process_donor_cohort([make_cohort([{}, GOOD])], VOLUME)
    assert result["collected_ml"] == 450


# ---- donor eligibility: hemoglobin -----------------------------------
def test_low_hemoglobin_standard_cohort_continues():
    result = process_donor_cohort([make_cohort([donor(hb=11.0), GOOD])],
                                  VOLUME)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_low_hemoglobin_high_altitude_resets_total_and_stops_cohort():
    cohort = make_cohort([GOOD, donor(hb=11.0), GOOD],
                         cohort_type="high_altitude")
    result = process_donor_cohort([cohort], VOLUME)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_high_altitude_reset_still_allows_fast_track_bonus():
    cohort = make_cohort([GOOD, donor(hb=11.0)], cohort_type="high_altitude",
                         fast_track=True)
    result = process_donor_cohort([cohort], VOLUME)
    assert result == {"collected_ml": 50, "status": "ACCEPTED"}


def test_high_altitude_cohort_with_good_donors_is_accepted():
    cohort = make_cohort([GOOD], cohort_type="high_altitude")
    result = process_donor_cohort([cohort], VOLUME)
    assert result["collected_ml"] == 450


def test_high_hemoglobin_donor_is_deferred():
    result = process_donor_cohort([make_cohort([donor(hb=19.0), GOOD])],
                                  VOLUME)
    assert result["collected_ml"] == 450


@pytest.mark.parametrize("hb", [12.5, 18.0])
def test_hemoglobin_boundaries_are_accepted(hb):
    result = process_donor_cohort([make_cohort([donor(hb=hb)])], VOLUME)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


# ---- final status ----------------------------------------------------
def test_four_deferrals_is_not_high_deferral():
    donors = [donor(age=16)] * 4 + [GOOD]
    result = process_donor_cohort([make_cohort(donors)], VOLUME)
    assert result["status"] == "ACCEPTED"


def test_five_deferrals_is_high_deferral():
    donors = [donor(age=16)] * 5 + [GOOD]
    result = process_donor_cohort([make_cohort(donors)], VOLUME)
    assert result == {"collected_ml": 450, "status": "HIGH_DEFERRAL"}


def test_high_deferral_takes_priority_over_zero_yield():
    donors = [donor(age=16)] * 5
    result = process_donor_cohort([make_cohort(donors)], VOLUME)
    assert result == {"collected_ml": 0, "status": "HIGH_DEFERRAL"}


def test_all_donors_deferred_is_zero_yield():
    result = process_donor_cohort([make_cohort([donor(age=16)])], VOLUME)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


# ---- centrifuge ------------------------------------------------------
@pytest.mark.parametrize("runs", [[], None])
def test_centrifuge_no_data(runs):
    assert verify_storage_centrifuge(runs) == "NO_DATA"


def test_centrifuge_stable():
    assert verify_storage_centrifuge([[3500, 3600, 3400]]) == "STABLE"


def test_centrifuge_exactly_3000_is_not_a_drop():
    assert verify_storage_centrifuge([[3000, 3000]]) == "STABLE"


def test_centrifuge_single_low_reading_is_stable():
    assert verify_storage_centrifuge([[3500, 2999, 3500]]) == "STABLE"


def test_centrifuge_streak_resets_after_recovery():
    assert verify_storage_centrifuge([[2900, 3200, 2900, 3200]]) == "STABLE"


def test_centrifuge_abort_on_two_consecutive_low_readings():
    assert verify_storage_centrifuge([[3500, 2900, 2800]]) == "ABORT_SPIN"


def test_centrifuge_abort_found_in_later_run():
    runs = [[3500, 3600], [3400, 2500, 2400]]
    assert verify_storage_centrifuge(runs) == "ABORT_SPIN"


def test_centrifuge_streak_does_not_carry_across_runs():
    runs = [[3500, 2900], [2900, 3500]]
    assert verify_storage_centrifuge(runs) == "STABLE"


def test_centrifuge_empty_run_is_stable():
    assert verify_storage_centrifuge([[]]) == "STABLE"
