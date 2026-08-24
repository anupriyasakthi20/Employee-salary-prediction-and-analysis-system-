import re


EMAIL_PATTERN = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"


def valid_employee_id(value):
    value = str(value).strip()

    return bool(value) and value.isdigit()


def valid_name(value):
    value = str(value).strip()

    return bool(value) and bool(
        re.fullmatch(r"[A-Za-z ]+", value)
    )


def valid_email(value):
    value = str(value).strip()

    return (
        bool(value)
        and re.match(EMAIL_PATTERN, value) is not None
    )


def valid_range(value, minimum, maximum):

    try:
        number = float(str(value).strip())

    except ValueError:
        return False

    return minimum <= number <= maximum


# ============================================================
# EMPLOYEE ID TESTING
# ============================================================

def test_employee_id_valid():

    assert valid_employee_id("1001")


def test_employee_id_rejects_letters():

    assert not valid_employee_id("EMP1001")


def test_employee_id_rejects_empty():

    assert not valid_employee_id("")


# ============================================================
# NAME TESTING
# ============================================================

def test_name_valid():

    assert valid_name("John Kumar")


def test_name_rejects_numbers():

    assert not valid_name("John123")


def test_name_rejects_empty():

    assert not valid_name("")


# ============================================================
# EMAIL TESTING
# ============================================================

def test_email_valid():

    assert valid_email("john@example.com")


def test_email_rejects_invalid():

    assert not valid_email("john@example")


def test_email_rejects_empty():

    assert not valid_email("")


# ============================================================
# EXPERIENCE TESTING
# Range: 0 - 40
# ============================================================

def test_experience_range():

    assert valid_range("6", 0, 40)

    assert valid_range("0", 0, 40)

    assert valid_range("40", 0, 40)


def test_experience_out_of_range():

    assert not valid_range("41", 0, 40)

    assert not valid_range("-1", 0, 40)


# ============================================================
# EDUCATION LEVEL TESTING
# Range: 1 - 5
# ============================================================

def test_education_range():

    assert valid_range("1", 1, 5)

    assert valid_range("5", 1, 5)


def test_education_out_of_range():

    assert not valid_range("0", 1, 5)

    assert not valid_range("6", 1, 5)


# ============================================================
# PERFORMANCE TESTING
# Range: 1 - 5
# ============================================================

def test_performance_range():

    assert valid_range("1", 1, 5)

    assert valid_range("5", 1, 5)


def test_performance_out_of_range():

    assert not valid_range("0", 1, 5)

    assert not valid_range("6", 1, 5)


# ============================================================
# SKILL SCORE TESTING
# Range: 0 - 100
# ============================================================

def test_skill_score_range():

    assert valid_range("80", 0, 100)

    assert valid_range("0", 0, 100)

    assert valid_range("100", 0, 100)


def test_skill_score_out_of_range():

    assert not valid_range("101", 0, 100)

    assert not valid_range("-1", 0, 100)


# ============================================================
# PREVIOUS SALARY PERCENTILE TESTING
# Range: 0 - 100
# ============================================================

def test_previous_salary_percentile_range():

    assert valid_range("70", 0, 100)

    assert valid_range("100", 0, 100)


def test_previous_salary_percentile_out_of_range():

    assert not valid_range("-1", 0, 100)

    assert not valid_range("101", 0, 100)
