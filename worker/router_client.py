from netmiko import ConnectHandler
import ntc_templates
import os
import json


def get_interfaces(ip, username, password):
    os.environ["NET_TEXTFSM"] = os.path.join(
        os.path.dirname(ntc_templates.__file__), "templates"
    )

    device = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": username,
        "password": password,
        "read_timeout_override": 90,  # ขยายเวลารอเป็น 90 วินาที
        "global_delay_factor": 3,  # เพิ่มหน่วงเวลาส่งคำสั่งเป็น 3 เท่า
        "fast_cli": False,  # ปิด fast mode เพื่อความเสถียร
    }

    with ConnectHandler(**device) as conn:
        try:
            conn.enable()
        except Exception:
            pass

        result = conn.send_command(
            "show ip int br",
            use_textfsm=True,
            expect_string=r"[\>#]",
            read_timeout=90,
        )

    print(json.dumps(result, indent=2))
    return result
