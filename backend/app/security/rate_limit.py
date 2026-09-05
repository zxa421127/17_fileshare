# 验证码防刷规则定义

RULES = {
    "email": {
        "cooldown_seconds": 60,
        "daily_limit": 20
    },
    "sms": {
        "cooldown_seconds": 60,
        "daily_limit": 10
    }
}

def check_limit(channel):
    return RULES.get(channel)
