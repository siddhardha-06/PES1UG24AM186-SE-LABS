import math

def validate_blood_type(blood_code):
    """
    Standardizes blood group and Rh factor (e.g. 'O+', 'AB-').
    Hardened against invalid types, empty strings, and malformed inputs.
    """
    if blood_code is None or not isinstance(blood_code, str):
        return "Invalid input: blood type must be a non-empty string"
    cleaned = blood_code.strip().upper()
    if len(cleaned) < 2:
        return "Invalid blood type: input too short"
    antigen = cleaned[:-1]
    rh_char = cleaned[-1]
    valid_antigens = {"A", "B", "AB", "O"}
    rh_map = {"+": "Positive", "-": "Negative"}
    if antigen not in valid_antigens or rh_char not in rh_map:
        return f"Invalid blood type: '{blood_code.strip()}' is not a recognized ABO/Rh format"
    return f"{antigen} {rh_map[rh_char]}"

def calculate_pulse_pressure(bp_string):
    """
    Calculates pulse pressure (systolic - diastolic) and arterial ratio.
    Hardened against malformed formats, non-numeric values, and division by zero.
    """
    if bp_string is None or not isinstance(bp_string, str):
        return "Invalid input: BP must be a string in 'systolic/diastolic' format"
    parts = bp_string.strip().split('/')
    if len(parts) != 2:
        return "Invalid BP format: expected 'systolic/diastolic' (e.g. 120/80)"
    try:
        systolic = int(parts[0].strip())
        diastolic = int(parts[1].strip())
    except (ValueError, TypeError):
        return "Invalid BP values: systolic and diastolic must be integers"
    if diastolic <= 0:
        return "Invalid BP values: diastolic pressure must be greater than zero"
    if systolic <= 0:
        return "Invalid BP values: systolic pressure must be greater than zero"
    pulse_diff = systolic - diastolic
    ratio = round(systolic / diastolic, 2)
    return f"Diff: {pulse_diff}, Ratio: {ratio}"

def parse_donor_registry(donor_entry):
    """
    Parses pipe-delimited record: 'DonorID|WeightKg|Hemoglobin'.
    Hardened against invalid fields, wrong token counts, and malformed numeric values.
    """
    if donor_entry is None or not isinstance(donor_entry, str):
        return "Invalid input: donor entry must be a pipe-delimited string"
    fields = donor_entry.strip().split('|')
    if len(fields) != 3:
        return "Invalid record: expected 3 pipe-separated fields (DonorID|WeightKg|Hemoglobin)"
    donor_id = fields[0].strip()
    if not donor_id:
        return "Invalid record: DonorID cannot be empty"
    try:
        weight = float(fields[1].strip())
        hemoglobin = float(fields[2].strip())
    except (ValueError, TypeError):
        return "Invalid record: weight and hemoglobin must be valid numbers"
    if math.isnan(weight) or math.isinf(weight) or math.isnan(hemoglobin) or math.isinf(hemoglobin):
        return "Invalid record: weight and hemoglobin must be finite numbers"
    if weight <= 0 or hemoglobin <= 0:
        return "Invalid record: weight and hemoglobin must be positive numbers"
    eligible = weight >= 50.0 and hemoglobin >= 12.5
    return f"Donor {donor_id}: {'Eligible' if eligible else 'Deferred'}"

def main():
    print("==== Running validate_blood_type ====")
    b_input = input("Enter blood type (e.g. A+, O-, AB+): ")
    print("Validated:", validate_blood_type(b_input))

    print("\n==== Running calculate_pulse_pressure ====")
    bp_input = input("Enter BP (e.g. 120/80): ")
    print("BP Metrics:", calculate_pulse_pressure(bp_input))

    print("\n==== Running parse_donor_registry ====")
    d_input = input("Enter record (ID|Weight|Hemoglobin): ")
    print("Status:", parse_donor_registry(d_input))

if __name__ == "__main__":
    main()
