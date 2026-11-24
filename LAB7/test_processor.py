from hypothesis import given, strategies as st
from processor import validate_blood_type, calculate_pulse_pressure, parse_donor_registry

@given(st.text() | st.none())
def test_validate_blood_type_no_crash(s):
    # To-Do: Using try and except complete this function.
    try:
        validate_blood_type(s)
    except Exception as e:
        assert False, f"validate_blood_type crashed with: {e}"

@given(st.text() | st.none())
def test_calculate_pulse_pressure_safe(s):
    # To-Do: Using try and except complete this function.
    try:
        calculate_pulse_pressure(s)
    except Exception as e:
        assert False, f"calculate_pulse_pressure crashed with: {e}"

@given(st.text() | st.none())
def test_parse_donor_registry_safe(s):
    # To-Do: Using try and except complete this function.
    try:
        parse_donor_registry(s)
    except Exception as e:
        assert False, f"parse_donor_registry crashed with: {e}"
