# main.py
"""
仅用于安全测试/教学演示：
- ALLOW_INSECURE_DEMO=1 时，启用不安全的硬编码密码反例
- 默认使用环境变量 APP_PASSWORD（安全做法）
"""

import os
import hmac
import getpass


def _load_expected_password() -> str:
    # 漏洞演示开关：仅测试环境允许
    if os.getenv("ALLOW_INSECURE_DEMO") == "1":
        # 不要放真实密码；仅用于反例演示
        return "<HARDCODED_PASSWORD_DEMO>"

    pwd = os.getenv("APP_PASSWORD")
    if not pwd:
        raise RuntimeError("Missing APP_PASSWORD in environment.")
    return pwd


def login() -> bool:
    username = input("Username: ").strip()
    if not username:
        print("Invalid username.")
        return False

    # 输入不回显，避免肩窥与日志泄露
    provided_password = getpass.getpass("Password: ")
    expected_password = _load_expected_password()

    # 使用恒定时间比较，降低时序侧信道风险
    ok = hmac.compare_digest(provided_password, expected_password)

    # 日志不打印密码，不暴露敏感细节
    if ok:
        print(f"User {username} logged in.")
        return True

    print("Authentication failed.")
    return False


if __name__ == "__main__":
    try:
        login()
    except Exception as e:
        # 生产可替换为结构化日志；避免输出敏感上下文
        print(f"Login error: {e}")