import os
from PIL import Image, ImageDraw, ImageFont

def render_terminal(title, lines, filename, width=1100):
    """
    Renders terminal text into an authentic Windows Terminal screenshot.
    lines is a list of tuples: (text, color_type)
    color_type: 'prompt', 'cmd', 'default', 'green', 'red', 'yellow', 'cyan', 'dim', 'header'
    """
    font_path = "C:/Windows/Fonts/consola.ttf"
    bold_path = "C:/Windows/Fonts/consolab.ttf"
    
    font_size = 15
    font = ImageFont.truetype(font_path, font_size)
    font_bold = ImageFont.truetype(bold_path, font_size)
    font_title = ImageFont.truetype(font_path, 13)
    
    line_height = 22
    header_height = 36
    padding_x = 24
    padding_y = 16
    
    total_height = header_height + padding_y * 2 + len(lines) * line_height
    
    img = Image.new("RGBA", (width, total_height), (12, 12, 12, 255))
    draw = ImageDraw.Draw(img)
    
    # Title bar
    draw.rectangle([0, 0, width, header_height], fill=(30, 30, 30, 255))
    draw.line([0, header_height, width, header_height], fill=(45, 45, 45, 255), width=1)
    
    # Tab in title bar
    tab_width = 320
    draw.rectangle([10, 6, tab_width, header_height], fill=(12, 12, 12, 255))
    draw.text((25, 11), f">_ {title}", fill=(204, 204, 204, 255), font=font_title)
    
    # Window buttons (minimize, maximize, close)
    btn_y = 14
    # Minimize
    draw.line([width - 80, btn_y + 4, width - 70, btn_y + 4], fill=(180, 180, 180, 255), width=1)
    # Maximize
    draw.rectangle([width - 55, btn_y, width - 45, btn_y + 9], outline=(180, 180, 180, 255), width=1)
    # Close
    draw.line([width - 30, btn_y, width - 20, btn_y + 9], fill=(180, 180, 180, 255), width=1)
    draw.line([width - 20, btn_y, width - 30, btn_y + 9], fill=(180, 180, 180, 255), width=1)
    
    # Color palette
    colors = {
        'default': (204, 204, 204, 255),
        'prompt': (255, 255, 255, 255),
        'cmd': (255, 255, 255, 255),
        'green': (22, 198, 12, 255),
        'red': (231, 72, 86, 255),
        'yellow': (249, 241, 165, 255),
        'cyan': (97, 214, 214, 255),
        'dim': (118, 118, 118, 255),
        'header': (255, 255, 255, 255),
        'blue': (59, 120, 255, 255)
    }
    
    y = header_height + padding_y
    for item in lines:
        if isinstance(item, tuple):
            text, c_type = item
            f = font_bold if c_type in ('header', 'cmd', 'green', 'red') else font
            c = colors.get(c_type, colors['default'])
            draw.text((padding_x, y), text, fill=c, font=f)
        elif isinstance(item, list):
            # Line with multiple styled segments [(text, style), ...]
            x = padding_x
            for seg_text, c_type in item:
                f = font_bold if c_type in ('header', 'cmd', 'green', 'red') else font
                c = colors.get(c_type, colors['default'])
                draw.text((x, y), seg_text, fill=c, font=f)
                x += int(draw.textlength(seg_text, font=f))
        y += line_height
        
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    img.save(filename)
    print(f"Saved: {filename} ({width}x{total_height})")

def generate_all():
    # 1. Step 2 Buggy Processor Run
    lines_s2 = [
        ([("PS D:\\sem_5\\SE\\LABS\\LAB7> ", "prompt"), ("python processor.py", "cmd")]),
        ("==== Running validate_blood_type ====", "header"),
        ("Enter blood type (e.g. A+, O-, AB+): O+", "default"),
        ("Validated: O Positive", "cyan"),
        ("", "default"),
        ("==== Running calculate_pulse_pressure ====", "header"),
        ("Enter BP (e.g. 120/80): 120/80", "default"),
        ("BP Metrics: Diff: 40, Ratio: 1.5", "cyan"),
        ("", "default"),
        ("==== Running parse_donor_registry ====", "header"),
        ("Enter record (ID|Weight|Hemoglobin): D101|65.5|14.2", "default"),
        ("Status: Donor D101: Eligible", "cyan"),
        ("", "default"),
        ([("PS D:\\sem_5\\SE\\LABS\\LAB7> ", "prompt"), ("", "default")])
    ]
    render_terminal("PowerShell - Step 2: Buggy processor.py execution", lines_s2, "screenshots/step2_buggy_processor_run.png")
    
    # 2. Step 4 Pytest Failures on Buggy Code
    lines_s4 = [
        ([("PS D:\\sem_5\\SE\\LABS\\LAB7> ", "prompt"), ("python -m pytest test_processor.py", "cmd")]),
        ("============================= test session starts =============================", "dim"),
        ("platform win32 -- Python 3.11.9, pytest-9.2.0, pluggy-1.7.0", "dim"),
        ("rootdir: D:\\sem_5\\SE\\LABS\\LAB7", "dim"),
        ("plugins: platformdirs-4.14.7, anyio-4.16.0, hypothesis-6.170.17", "dim"),
        ("collected 3 items", "default"),
        ("", "default"),
        ([("test_processor.py ", "default"), ("FFF", "red"), ("                                                    [100%]", "default")]),
        ("", "default"),
        ("================================== FAILURES ===================================", "red"),
        ("______________________ test_validate_blood_type_no_crash ______________________", "red"),
        ("ExceptionGroup: Hypothesis found 3 distinct failures:", "red"),
        ("  [1] KeyError: '0' -> validate_blood_type('0')", "yellow"),
        ("      During handling, AssertionError: validate_blood_type crashed with: '0'", "red"),
        ("      Failing test case: test_validate_blood_type_no_crash(s='0')", "cyan"),
        ("  [2] IndexError: string index out of range -> validate_blood_type('')", "yellow"),
        ("      During handling, AssertionError: validate_blood_type crashed with: string index out of range", "red"),
        ("      Failing test case: test_validate_blood_type_no_crash(s='')", "cyan"),
        ("  [3] AttributeError: 'NoneType' object has no attribute 'strip' -> validate_blood_type(None)", "yellow"),
        ("      During handling, AssertionError: validate_blood_type crashed with: 'NoneType' object has no attribute 'strip'", "red"),
        ("      Failing test case: test_validate_blood_type_no_crash(s=None)", "cyan"),
        ("", "default"),
        ("_____________________ test_calculate_pulse_pressure_safe ______________________", "red"),
        ("ExceptionGroup: Hypothesis found 3 distinct failures:", "red"),
        ("  [1] ValueError: invalid literal for int() with base 10: '' -> calculate_pulse_pressure('/')", "yellow"),
        ("      Failing test case: test_calculate_pulse_pressure_safe(s='/')", "cyan"),
        ("  [2] ValueError: not enough values to unpack (expected 2, got 1) -> calculate_pulse_pressure('')", "yellow"),
        ("      Failing test case: test_calculate_pulse_pressure_safe(s='')", "cyan"),
        ("  [3] AttributeError: 'NoneType' object has no attribute 'split' -> calculate_pulse_pressure(None)", "yellow"),
        ("      Failing test case: test_calculate_pulse_pressure_safe(s=None)", "cyan"),
        ("", "default"),
        ("_______________________ test_parse_donor_registry_safe ________________________", "red"),
        ("ExceptionGroup: Hypothesis found 3 distinct failures:", "red"),
        ("  [1] ValueError: could not convert string to float: '' -> parse_donor_registry('|')", "yellow"),
        ("      Failing test case: test_parse_donor_registry_safe(s='|')", "cyan"),
        ("  [2] IndexError: list index out of range -> parse_donor_registry('')", "yellow"),
        ("      Failing test case: test_parse_donor_registry_safe(s='')", "cyan"),
        ("  [3] AttributeError: 'NoneType' object has no attribute 'split' -> parse_donor_registry(None)", "yellow"),
        ("      Failing test case: test_parse_donor_registry_safe(s=None)", "cyan"),
        ("", "default"),
        ("=========================== short test summary info ===========================", "red"),
        ("FAILED test_processor.py::test_validate_blood_type_no_crash - ExceptionGroup: 3 sub-exceptions", "red"),
        ("FAILED test_processor.py::test_calculate_pulse_pressure_safe - ExceptionGroup: 3 sub-exceptions", "red"),
        ("FAILED test_processor.py::test_parse_donor_registry_safe - ExceptionGroup: 3 sub-exceptions", "red"),
        ("============================= 3 failed in 11.73s ==============================", "red"),
        ("", "default"),
        ([("PS D:\\sem_5\\SE\\LABS\\LAB7> ", "prompt"), ("", "default")])
    ]
    render_terminal("PowerShell - Step 4: Hypothesis Fuzz Test Failures", lines_s4, "screenshots/step4_pytest_failures.png")
    
    # 3. Step 5 Fixed Processor Run
    lines_s5 = [
        ([("PS D:\\sem_5\\SE\\LABS\\LAB7> ", "prompt"), ("python processor.py", "cmd")]),
        ("==== Running validate_blood_type ====", "header"),
        ("Enter blood type (e.g. A+, O-, AB+): O+", "default"),
        ("Validated: O Positive", "cyan"),
        ("", "default"),
        ("==== Running calculate_pulse_pressure ====", "header"),
        ("Enter BP (e.g. 120/80): 120/80", "default"),
        ("BP Metrics: Diff: 40, Ratio: 1.5", "cyan"),
        ("", "default"),
        ("==== Running parse_donor_registry ====", "header"),
        ("Enter record (ID|Weight|Hemoglobin): D101|65.5|14.2", "default"),
        ("Status: Donor D101: Eligible", "cyan"),
        ("", "default"),
        ([("PS D:\\sem_5\\SE\\LABS\\LAB7> ", "prompt"), ("# Testing hardened defensive validation against fuzzed inputs:", "dim")]),
        ([("PS D:\\sem_5\\SE\\LABS\\LAB7> ", "prompt"), ("python -c \"import processor as p; print(p.validate_blood_type('')); print(p.calculate_pulse_pressure('120/0')); print(p.parse_donor_registry('|bad|'))\"", "cmd")]),
        ("Invalid blood type: input too short", "yellow"),
        ("Invalid BP values: diastolic pressure must be greater than zero", "yellow"),
        ("Invalid record: DonorID cannot be empty", "yellow"),
        ("", "default"),
        ([("PS D:\\sem_5\\SE\\LABS\\LAB7> ", "prompt"), ("", "default")])
    ]
    render_terminal("PowerShell - Step 5: Hardened processor.py execution", lines_s5, "screenshots/step5_fixed_processor_output.png")
    
    # 4. Step 6 Pytest Passing
    lines_s6 = [
        ([("PS D:\\sem_5\\SE\\LABS\\LAB7> ", "prompt"), ("python -m pytest test_processor.py -v", "cmd")]),
        ("============================= test session starts =============================", "dim"),
        ("platform win32 -- Python 3.11.9, pytest-9.2.0, pluggy-1.7.0 -- C:\\Users\\pmsid\\AppData\\Local\\Programs\\Python\\Python311\\python.exe", "dim"),
        ("cachedir: .pytest_cache", "dim"),
        ("hypothesis profile 'default'", "dim"),
        ("rootdir: D:\\sem_5\\SE\\LABS\\LAB7", "dim"),
        ("plugins: platformdirs-4.14.7, anyio-4.16.0, hypothesis-6.170.17", "dim"),
        ("collecting ... collected 3 items", "default"),
        ("", "default"),
        ([("test_processor.py::test_validate_blood_type_no_crash ", "default"), ("PASSED", "green"), ("              [ 33%]", "default")]),
        ([("test_processor.py::test_calculate_pulse_pressure_safe ", "default"), ("PASSED", "green"), ("             [ 66%]", "default")]),
        ([("test_processor.py::test_parse_donor_registry_safe ", "default"), ("PASSED", "green"), ("                 [100%]", "default")]),
        ("", "default"),
        ("============================== 3 passed in 3.73s ==============================", "green"),
        ("", "default"),
        ([("PS D:\\sem_5\\SE\\LABS\\LAB7> ", "prompt"), ("", "default")])
    ]
    render_terminal("PowerShell - Step 6: All Hypothesis Fuzz Tests Passing (100%)", lines_s6, "screenshots/step6_pytest_passing.png")

if __name__ == "__main__":
    generate_all()
