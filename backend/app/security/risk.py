def calculate_risk(
    new_device=False,
    new_ip=False,
    password_failed=False,
    captcha_abnormal=False
):
    score=0
    if new_device:
        score+=10
    if new_ip:
        score+=10
    if password_failed:
        score+=20
    if captcha_abnormal:
        score+=30

    if score < 30:
        level="low"
    elif score < 60:
        level="medium"
    else:
        level="high"

    return {
        "score":score,
        "level":level
    }
