from app.security.rate_limit import check_limit
from app.security.risk import calculate_risk


def test_rate_limit_rules():
    assert check_limit("email") == {
        "cooldown_seconds": 60,
        "daily_limit": 20,
    }
    assert check_limit("sms") == {
        "cooldown_seconds": 60,
        "daily_limit": 10,
    }
    assert check_limit("unknown") is None


def test_risk_levels():
    assert calculate_risk()["level"] == "low"
    assert calculate_risk(new_ip=True, password_failed=True) == {
        "score": 30,
        "level": "medium",
    }
    assert calculate_risk(
        new_device=True,
        password_failed=True,
        captcha_abnormal=True,
    ) == {"score": 60, "level": "high"}
