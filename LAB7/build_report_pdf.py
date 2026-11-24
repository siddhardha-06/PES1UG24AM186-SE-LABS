import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, Preformatted
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#666666"))
        
        # Running Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(40, 756, "Lab 7: Fuzzing for Input Validation Bugs — PES1UG24AM186")
            self.setStrokeColor(colors.HexColor("#dcdfe6"))
            self.setLineWidth(0.5)
            self.line(40, 750, 572, 750)
            
        # Running Footer
        text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(572, 24, text)
        self.drawString(40, 24, "Blood Donation Screening System — P Manas Siddhardha")
        self.setStrokeColor(colors.HexColor("#dcdfe6"))
        self.setLineWidth(0.5)
        self.line(40, 34, 572, 34)
        self.restoreState()

def build_pdf(filename="PES1UG24AM186_LAB7_REPORT.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0f2c59")
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#333333")
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0f2c59"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#1e3d59"),
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#222222"),
        spaceAfter=5
    )
    
    code_pre_style = ParagraphStyle(
        'Code_Pre',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.8,
        leading=8.0,
        textColor=colors.HexColor("#1a1a1a")
    )
    
    code_pre_test_style = ParagraphStyle(
        'Code_Pre_Test',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#1a1a1a")
    )
    
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#222222")
    )
    
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.white
    )
    
    story = []
    
    # ================= PAGE 1: Overview, Summary & Dependencies =================
    story.append(Paragraph("Lab 7: Fuzzing for Input Validation Bugs", title_style))
    story.append(Paragraph("Blood Donation Screening System (<code>processor.py</code>)", subtitle_style))
    story.append(Spacer(1, 8))
    
    # Metadata Table
    meta_data = [
        [Paragraph("<b>Name</b>", table_cell), Paragraph("P Manas Siddhardha", table_cell)],
        [Paragraph("<b>SRN</b>", table_cell), Paragraph("PES1UG24AM186", table_cell)],
        [Paragraph("<b>Repository</b>", table_cell), Paragraph("SETAPESU26/L6_L7_05_blood_donation_screening", table_cell)],
        [Paragraph("<b>Tools</b>", table_cell), Paragraph("Python 3.11, Hypothesis 6.170.17, Pytest 9.2.0", table_cell)],
        [Paragraph("<b>Domain</b>", table_cell), Paragraph("Blood Donation Screening (ABO/Rh validation, pulse pressure vitals, donor registry)", table_cell)]
    ]
    meta_table = Table(meta_data, colWidths=[80, 452])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8f9fa")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#dcdfe6")),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))
    
    # 1. Objective and Approach
    story.append(Paragraph("1. Objective and Approach", h1_style))
    story.append(Paragraph(
        "The objective of this lab is to explore dynamic fuzz testing as a security and quality assurance technique "
        "by identifying and fixing hidden input validation bugs in an assigned blood donation screening module "
        "(<code>processor.py</code>) using the <b>Hypothesis</b> property-based testing framework.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Methodology:</b> Rather than authoring manual hand-crafted test vectors that only verify anticipated inputs, "
        "property-based fuzz testing specifies general invariants (e.g., functions must process arbitrary inputs without crashing or raising unhandled exceptions). "
        "Hypothesis generates hundreds of randomized, edge-case, and malformed inputs (empty strings, <code>NoneType</code>, boundary conditions, malformed tokens, "
        "non-numeric strings, and zero denominators). Once failures are uncovered, Hypothesis automatically shrinks the inputs to identify minimal reproducible test cases. "
        "Defensive programming and rigorous input sanitation are then applied in <code>processor.py</code> to harden the application against all invalid inputs.",
        body_style
    ))
    story.append(Spacer(1, 8))
    
    # 2. Results Summary
    story.append(Paragraph("2. Results Summary", h1_style))
    summary_data = [
        [Paragraph("Test Function", table_header), Paragraph("Fuzzing Strategy", table_header), Paragraph("Buggy Code Result", table_header), Paragraph("Hardened Code Result", table_header)],
        [
            Paragraph("<code>test_validate_blood_type_no_crash</code>", table_cell),
            Paragraph("<code>st.text() | st.none()</code>", table_cell),
            Paragraph("<font color='#d93025'><b>FAILED</b> (3 sub-exceptions: AttributeError, IndexError, KeyError)</font>", table_cell),
            Paragraph("<font color='#188038'><b>PASSED</b> (100+ fuzzed runs, 0 crashes)</font>", table_cell)
        ],
        [
            Paragraph("<code>test_calculate_pulse_pressure_safe</code>", table_cell),
            Paragraph("<code>st.text() | st.none()</code>", table_cell),
            Paragraph("<font color='#d93025'><b>FAILED</b> (3 sub-exceptions: AttributeError, ValueError, ZeroDivisionError)</font>", table_cell),
            Paragraph("<font color='#188038'><b>PASSED</b> (100+ fuzzed runs, 0 crashes)</font>", table_cell)
        ],
        [
            Paragraph("<code>test_parse_donor_registry_safe</code>", table_cell),
            Paragraph("<code>st.text() | st.none()</code>", table_cell),
            Paragraph("<font color='#d93025'><b>FAILED</b> (3 sub-exceptions: AttributeError, IndexError, ValueError)</font>", table_cell),
            Paragraph("<font color='#188038'><b>PASSED</b> (100+ fuzzed runs, 0 crashes)</font>", table_cell)
        ]
    ]
    summary_table = Table(summary_data, colWidths=[160, 110, 132, 130])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0f2c59")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#dcdfe6")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 10))
    
    # Step 1
    story.append(Paragraph("3. Lab Execution Steps and Screenshots", h1_style))
    story.append(Paragraph("<b>Step 1: Installing Dependencies</b>", h2_style))
    story.append(Paragraph(
        "Installed the required property testing dependencies using <code>pip install hypothesis pytest</code>. "
        "Hypothesis provides generative strategies and shrinking mechanisms, while Pytest serves as the test discovery and execution engine.",
        body_style
    ))
    
    story.append(PageBreak())
    
    # ================= PAGE 2: Step 2 & Step 3 =================
    story.append(Paragraph("<b>Step 2: Running Buggy Application (<code>python processor.py</code>)</b>", h2_style))
    story.append(Paragraph(
        "The starter application was executed using typical nominal inputs (<code>O+</code>, <code>120/80</code>, and <code>D101|65.5|14.2</code>). "
        "Under happy-path execution, the script produces expected formatted outputs. However, the implementation completely lacks defensive guards "
        "and crashes immediately upon receiving unexpected, empty, or malformed tokens.",
        body_style
    ))
    story.append(Spacer(1, 4))
    
    if os.path.exists("screenshots/step2_buggy_processor_run.png"):
        img_s2 = Image("screenshots/step2_buggy_processor_run.png", width=510, height=174)
        story.append(img_s2)
        story.append(Spacer(1, 14))
        
    story.append(Paragraph("<b>Step 3: Completing <code>test_processor.py</code> using Hypothesis</b>", h2_style))
    story.append(Paragraph(
        "Using Hypothesis's <code>@given(st.text() | st.none())</code> decorator and a defensive <code>try-except</code> test harness, "
        "property-based fuzz tests were implemented for all three functions. Rather than asserting specific return values, the test asserts "
        "the core robustness property: <i>the application must not crash or raise unhandled exceptions on any generated input</i>. "
        "If any exception propagates, the test fails with <code>assert False, f'... crashed with: {e}'</code>.",
        body_style
    ))
    story.append(Spacer(1, 8))
    
    test_snippet = (
        "@given(st.text() | st.none())\n"
        "def test_validate_blood_type_no_crash(s):\n"
        "    try:\n"
        "        validate_blood_type(s)\n"
        "    except Exception as e:\n"
        "        assert False, f\"validate_blood_type crashed with: {e}\""
    )
    story.append(Preformatted(test_snippet, code_pre_test_style))
    
    story.append(PageBreak())
    
    # ================= PAGE 3: Step 4 Pytest Failures =================
    story.append(Paragraph("<b>Step 4: Running Fuzz Tests on Buggy Code (<code>pytest test_processor.py</code>)</b>", h2_style))
    story.append(Paragraph(
        "Executing <code>python -m pytest test_processor.py</code> immediately triggered failures across all 3 functions. "
        "Hypothesis dynamically generated edge-case inputs and systematically shrank them to minimal failing examples: "
        "<code>s=None</code> (AttributeError), <code>s=''</code> (IndexError), <code>s='0'</code> (KeyError), <code>s='/'</code> (ValueError), and <code>s='|'</code> (ValueError). "
        "The complete Pytest failure log is captured below:",
        body_style
    ))
    story.append(Spacer(1, 4))
    
    if os.path.exists("screenshots/step4_pytest_failures.png"):
        img_s4 = Image("screenshots/step4_pytest_failures.png", width=510, height=511)
        story.append(img_s4)
        
    story.append(PageBreak())
    
    # ================= PAGE 4: Step 5 & Step 6 =================
    story.append(Paragraph("<b>Step 5: Hardening the Application (<code>processor.py</code>)</b>", h2_style))
    story.append(Paragraph(
        "The module was hardened through comprehensive defensive programming: checking for <code>None</code> and type validity, "
        "enforcing string boundary lengths, validating ABO/Rh antigen membership (<code>A, B, AB, O</code> and <code>+, -</code>), "
        "safely parsing systolic/diastolic components with zero/negative division guards, validating positive numeric ranges for weight and hemoglobin, "
        "and rejecting non-finite/NaN/infinite inputs. Running the fixed script demonstrates graceful error handling instead of unhandled crashes.",
        body_style
    ))
    story.append(Spacer(1, 4))
    
    if os.path.exists("screenshots/step5_fixed_processor_output.png"):
        img_s5 = Image("screenshots/step5_fixed_processor_output.png", width=510, height=235)
        story.append(img_s5)
        story.append(Spacer(1, 10))
        
    story.append(Paragraph("<b>Step 6: Re-Running Fuzz Tests on Hardened Application</b>", h2_style))
    story.append(Paragraph(
        "Re-running <code>python -m pytest test_processor.py -v</code> verifies that all property tests pass successfully (100% pass rate). "
        "Hypothesis generated 100+ randomized fuzz iterations per function (300+ total runs) with zero crashes or unhandled exceptions.",
        body_style
    ))
    story.append(Spacer(1, 4))
    
    if os.path.exists("screenshots/step6_pytest_passing.png"):
        img_s6 = Image("screenshots/step6_pytest_passing.png", width=510, height=195)
        story.append(img_s6)
        
    story.append(PageBreak())
    
    # ================= PAGE 5: Issues, Fixes & Comparison =================
    story.append(Paragraph("4. Discovered Vulnerabilities and Defensive Fixes", h1_style))
    story.append(Paragraph("The following table documents all bugs and security vulnerabilities discovered through fuzzing, along with the defensive remediation approach implemented:", body_style))
    story.append(Spacer(1, 2))
    
    bug_data = [
        [Paragraph("#", table_header), Paragraph("Function", table_header), Paragraph("Trigger Input", table_header), Paragraph("Exception Type", table_header), Paragraph("Vulnerability Description", table_header), Paragraph("Fix Approach", table_header)],
        [
            Paragraph("1", table_cell),
            Paragraph("<code>validate_blood_type</code>", table_cell),
            Paragraph("<code>s = None</code>", table_cell),
            Paragraph("<code>AttributeError</code>", table_cell),
            Paragraph("Calling <code>.strip()</code> on <code>NoneType</code> crashes program.", table_cell),
            Paragraph("Type guard: verify <code>isinstance(blood_code, str) and not None</code>.", table_cell)
        ],
        [
            Paragraph("2", table_cell),
            Paragraph("<code>validate_blood_type</code>", table_cell),
            Paragraph("<code>s = ''</code>", table_cell),
            Paragraph("<code>IndexError</code>", table_cell),
            Paragraph("Index <code>[-1]</code> on empty/whitespace string crashes.", table_cell),
            Paragraph("Boundary check: ensure <code>len(cleaned) >= 2</code>.", table_cell)
        ],
        [
            Paragraph("3", table_cell),
            Paragraph("<code>validate_blood_type</code>", table_cell),
            Paragraph("<code>s = '0'</code>, <code>'XYZ'</code>", table_cell),
            Paragraph("<code>KeyError</code>", table_cell),
            Paragraph("Direct dictionary lookup <code>rh_map[rh_char]</code> crashes.", table_cell),
            Paragraph("Validate Rh in <code>{'+', '-'}</code> and antigen in <code>{'A','B','AB','O'}</code>.", table_cell)
        ],
        [
            Paragraph("4", table_cell),
            Paragraph("<code>calculate_pulse_pressure</code>", table_cell),
            Paragraph("<code>s = None</code>", table_cell),
            Paragraph("<code>AttributeError</code>", table_cell),
            Paragraph("Calling <code>.split('/')</code> on <code>None</code> raises unhandled error.", table_cell),
            Paragraph("Strict type guard ensuring input is a string.", table_cell)
        ],
        [
            Paragraph("5", table_cell),
            Paragraph("<code>calculate_pulse_pressure</code>", table_cell),
            Paragraph("<code>s = ''</code>, <code>'120'</code>", table_cell),
            Paragraph("<code>ValueError</code>", table_cell),
            Paragraph("Unpacking <code>split('/')</code> fails when <code>/</code> is absent.", table_cell),
            Paragraph("Check <code>len(parts) == 2</code> before unpacking.", table_cell)
        ],
        [
            Paragraph("6", table_cell),
            Paragraph("<code>calculate_pulse_pressure</code>", table_cell),
            Paragraph("<code>s = '/'</code>, <code>'a/b'</code>", table_cell),
            Paragraph("<code>ValueError</code>", table_cell),
            Paragraph("Calling <code>int()</code> on empty or non-digit strings crashes.", table_cell),
            Paragraph("Catch <code>(ValueError, TypeError)</code> safely.", table_cell)
        ],
        [
            Paragraph("7", table_cell),
            Paragraph("<code>calculate_pulse_pressure</code>", table_cell),
            Paragraph("<code>s = '120/0'</code>", table_cell),
            Paragraph("<code>ZeroDivisionError</code>", table_cell),
            Paragraph("Zero diastolic pressure causes fatal division by zero.", table_cell),
            Paragraph("Enforce physiological boundary: <code>diastolic > 0 and systolic > 0</code>.", table_cell)
        ],
        [
            Paragraph("8", table_cell),
            Paragraph("<code>parse_donor_registry</code>", table_cell),
            Paragraph("<code>s = None</code>", table_cell),
            Paragraph("<code>AttributeError</code>", table_cell),
            Paragraph("Calling <code>.split('|')</code> on <code>None</code> crashes process.", table_cell),
            Paragraph("Type guard ensuring input is a string.", table_cell)
        ],
        [
            Paragraph("9", table_cell),
            Paragraph("<code>parse_donor_registry</code>", table_cell),
            Paragraph("<code>s = ''</code>, <code>'D1'</code>", table_cell),
            Paragraph("<code>IndexError</code>", table_cell),
            Paragraph("Accessing fields crashes when fewer than 3 tokens exist.", table_cell),
            Paragraph("Verify exactly 3 pipe-separated fields (<code>len == 3</code>).", table_cell)
        ],
        [
            Paragraph("10", table_cell),
            Paragraph("<code>parse_donor_registry</code>", table_cell),
            Paragraph("<code>s = '|'</code>, <code>'D1|x|y'</code>", table_cell),
            Paragraph("<code>ValueError</code>", table_cell),
            Paragraph("Calling <code>float()</code> on malformed strings causes crash.", table_cell),
            Paragraph("Catch conversion exceptions; reject non-numeric inputs.", table_cell)
        ],
        [
            Paragraph("11", table_cell),
            Paragraph("<code>parse_donor_registry</code>", table_cell),
            Paragraph("<code>' |60|13'</code>", table_cell),
            Paragraph("Logic Error", table_cell),
            Paragraph("Blank Donor ID was permitted into registry.", table_cell),
            Paragraph("Require non-empty stripped <code>donor_id</code> string.", table_cell)
        ],
        [
            Paragraph("12", table_cell),
            Paragraph("<code>parse_donor_registry</code>", table_cell),
            Paragraph("<code>'D1|-50|-10'</code>, <code>nan</code>", table_cell),
            Paragraph("Domain / Logic", table_cell),
            Paragraph("Negative weights/hemoglobin or NaN/inf values accepted.", table_cell),
            Paragraph("Enforce positive, finite numbers via <code>math.isfinite() > 0</code>.", table_cell)
        ]
    ]
    bug_table = Table(bug_data, colWidths=[18, 110, 80, 85, 125, 114])
    bug_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0f2c59")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#dcdfe6")),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
    ]))
    story.append(bug_table)
    story.append(Spacer(1, 8))
    
    # 5. Behaviour Before and After
    story.append(Paragraph("5. Behaviour Before and After", h1_style))
    beh_data = [
        [Paragraph("Scenario / Input", table_header), Paragraph("Buggy Code Behaviour (Before)", table_header), Paragraph("Hardened Code Behaviour (After)", table_header)],
        [
            Paragraph("Normal valid blood type: <code>'O+'</code>", table_cell),
            Paragraph("Returns <code>'O Positive'</code>", table_cell),
            Paragraph("Returns <code>'O Positive'</code> (Preserved functionality)", table_cell)
        ],
        [
            Paragraph("Empty blood type: <code>''</code> or <code>None</code>", table_cell),
            Paragraph("<font color='#d93025'>Crashes with <code>IndexError</code> / <code>AttributeError</code></font>", table_cell),
            Paragraph("<font color='#188038'>Returns descriptive error string safely</font>", table_cell)
        ],
        [
            Paragraph("Invalid blood group / Rh: <code>'XYZ'</code>", table_cell),
            Paragraph("<font color='#d93025'>Crashes with <code>KeyError: 'Z'</code></font>", table_cell),
            Paragraph("<font color='#188038'>Validates ABO antigen and Rh sign</font>", table_cell)
        ],
        [
            Paragraph("Normal BP: <code>'120/80'</code>", table_cell),
            Paragraph("Returns <code>'Diff: 40, Ratio: 1.5'</code>", table_cell),
            Paragraph("Returns <code>'Diff: 40, Ratio: 1.5'</code> (Preserved)", table_cell)
        ],
        [
            Paragraph("Division by zero BP: <code>'120/0'</code>", table_cell),
            Paragraph("<font color='#d93025'>Crashes with fatal <code>ZeroDivisionError</code></font>", table_cell),
            Paragraph("<font color='#188038'>Validates diastolic pressure > 0</font>", table_cell)
        ],
        [
            Paragraph("Malformed donor string: <code>'|bad|'</code>", table_cell),
            Paragraph("<font color='#d93025'>Crashes with <code>ValueError</code> on float parsing</font>", table_cell),
            Paragraph("<font color='#188038'>Catches parsing error; validates ID and ranges</font>", table_cell)
        ]
    ]
    beh_table = Table(beh_data, colWidths=[150, 185, 197])
    beh_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0f2c59")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#dcdfe6")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
    ]))
    story.append(beh_table)
    
    story.append(PageBreak())
    
    # ================= PAGE 6: Reflection & test_processor.py =================
    story.append(Paragraph("6. Reflection and Analysis", h1_style))
    story.append(Paragraph("<b>Why is property-based fuzzing superior to traditional unit testing?</b>", h2_style))
    story.append(Paragraph(
        "Traditional unit tests only validate scenarios the developer actively anticipates. Developers carry cognitive bias toward valid "
        "or structured inputs, frequently overlooking boundary conditions, weird Unicode glyphs, empty tokens, negative numbers, or type incompatibilities. "
        "Property-based fuzzing with Hypothesis treats the system as a black box and actively searches the entire input domain to break assumptions. "
        "Fuzzing discovers defects that developers never imagined could occur.",
        body_style
    ))
    
    story.append(Paragraph("<b>How does Hypothesis's input shrinking help in debugging?</b>", h2_style))
    story.append(Paragraph(
        "When a fuzzer discovers a crash with an enormous, chaotic random input (e.g., a 500-character random Unicode string), debugging is cumbersome. "
        "Hypothesis automatically performs 'shrinking': iteratively simplifying the failing input to the simplest possible counterexample "
        "(such as reducing the string to <code>''</code>, <code>'0'</code>, or <code>None</code>). This pinpoints the exact root cause in seconds.",
        body_style
    ))
    
    story.append(Paragraph("<b>Which issues were easiest and hardest to fix?</b>", h2_style))
    story.append(Paragraph(
        "The easiest fixes were type and existence checks (verifying <code>is not None</code> and string length). The hardest fixes were "
        "domain-specific boundary logic: ensuring physiological constraints (positive non-zero blood pressure, non-NaN/non-infinite floating point metrics, "
        "and proper ABO/Rh medical blood groupings) while ensuring the function never crashes regardless of malformed inputs.",
        body_style
    ))
    
    story.append(Paragraph("<b>How would you integrate fuzzing into continuous integration (CI)?</b>", h2_style))
    story.append(Paragraph(
        "In CI/CD pipelines, fuzz tests should run as an automated test stage on every pull request with a bounded number of examples (e.g. 100-200 iterations) "
        "for fast feedback, and as a prolonged nightly fuzzing job (10,000+ iterations) to continuously discover deep regression bugs before release.",
        body_style
    ))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("7. Source Code Listings", h1_style))
    story.append(Paragraph("<b>Updated <code>test_processor.py</code> (Hypothesis Fuzz Test Suite):</b>", h2_style))
    with open("test_processor.py", "r", encoding="utf-8") as f:
        test_code_text = f.read()
    story.append(Preformatted(test_code_text, code_pre_test_style))
    
    story.append(PageBreak())
    
    # ================= PAGE 7: Hardened processor.py =================
    story.append(Paragraph("<b>Hardened Application: <code>processor.py</code>:</b>", h2_style))
    with open("processor.py", "r", encoding="utf-8") as f:
        proc_code_text = f.read()
    story.append(Preformatted(proc_code_text, code_pre_style))
    
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    build_pdf()
