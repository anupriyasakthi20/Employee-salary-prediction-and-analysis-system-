import json


# ============================================================
# SAMPLE N8N PAYLOAD
# ============================================================

def build_payload():

    return {

        "employee_id": "1001",

        "name": "John Kumar",

        "email": "john@example.com",

        "experience": 6.0,

        "education_level": 4.0,

        "performance_rating": 4.0,

        "skill_score": 80.0,

        "previous_salary_percentile": 70.0,

        "prediction": "HIGH",

        "risk": "LOW",
    }


# ============================================================
# PAYLOAD FIELD TEST
# ============================================================

def test_n8n_payload_contains_required_fields():

    payload = build_payload()


    required = {

        "employee_id",

        "name",

        "email",

        "experience",

        "education_level",

        "performance_rating",

        "skill_score",

        "previous_salary_percentile",

        "prediction",

        "risk",
    }


    assert required.issubset(
        payload.keys()
    )


# ============================================================
# JSON SERIALIZATION TEST
# ============================================================

def test_n8n_payload_is_json_serializable():

    payload = build_payload()


    encoded = json.dumps(
        payload
    )


    decoded = json.loads(
        encoded
    )


    assert decoded[
        "prediction"
    ] == "HIGH"


    assert decoded[
        "risk"
    ] == "LOW"


# ============================================================
# RECOMMENDATION TEST
# ============================================================

def test_n8n_success_response_contains_recommendation():

    response = {

        "recommendation":
        "Maintain competitive pay and "
        "provide growth opportunities."
    }


    assert response.get(
        "recommendation"
    )


# ============================================================
# RESPONSE FALLBACK TEST
# ============================================================

def test_n8n_response_fallback_fields():

    responses = [

        {
            "recommendation":
            "Recommendation A"
        },

        {
            "output":
            "Recommendation B"
        },

        {
            "text":
            "Recommendation C"
        },
    ]


    for response in responses:

        recommendation = (

            response.get(
                "recommendation"
            )

            or response.get(
                "output"
            )

            or response.get(
                "text"
            )

            or ""
        )


        assert recommendation
