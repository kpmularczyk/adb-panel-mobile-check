import requests
from config import SUPABASE_URL, SUPABASE_KEY


def get_device_details():
    url = f"{SUPABASE_URL}/rest/v1/device_details_dashboard"

    headers = {
        "apikey": SUPABASE_KEY,
    }

    params = {
        "select": "device_id,device_name,device_usage_status,adb_status,daily_check_ok,phone_number",
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=15,
    )

    response.raise_for_status()
    return response.json()


def get_problem_devices():
    devices = get_device_details()
    result = {}

    for device in devices:
        if (
            device["device_usage_status"] != "active" or
            (device["adb_status"] == "device"
            and device["daily_check_ok"] is True)
        ):
            continue

        device_id = device["device_id"]

        if device_id not in result:
            result[device_id] = {
                "name": device["device_name"],
                "adb_status": device["adb_status"],
                "daily_check_ok": device["daily_check_ok"],
                "phone_numbers": set(),
            }

        if device["phone_number"]:
            result[device_id]["phone_numbers"].add(
                device["phone_number"]
            )

    return result


problem_devices = get_problem_devices()

import requests
from config import SUPABASE_URL, SUPABASE_KEY


def get_device_details():
    url = f"{SUPABASE_URL}/rest/v1/device_details_dashboard"

    headers = {
        "apikey": SUPABASE_KEY,
    }

    params = {
        "select": "device_id,device_name,device_usage_status,adb_status,daily_check_ok,phone_number",
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=15,
    )

    response.raise_for_status()
    return response.json()


def get_problem_devices():
    devices = get_device_details()
    result = {}

    for device in devices:
        if (
            device["device_usage_status"] != "active" or
            (device["adb_status"] == "device"
            and device["daily_check_ok"] is True)
        ):
            continue

        device_id = device["device_id"]

        if device_id not in result:
            result[device_id] = {
                "name": device["device_name"],
                "adb_status": device["adb_status"],
                "daily_check_ok": device["daily_check_ok"],
                "phone_numbers": set(),
            }

        if device["phone_number"]:
            result[device_id]["phone_numbers"].add(
                device["phone_number"]
            )

    return result


problem_devices = get_problem_devices()

message = ""
if not problem_devices:
    message = "All devices are OK!"
else:
    message = f"{len(problem_devices)} devices with problems:\n"
    for device in problem_devices.values():
        message += f"- {device['name']}, ADB: {device['adb_status']}, DC: {device['daily_check_ok']}, "
        message += (
            "Tel.: "
            + ", ".join(sorted(device["phone_numbers"]))
            if device["phone_numbers"]
            else "Tel.: none"
        )

import notification
notification.schedule(
    message=message,
    delay=1,
    title="ADB panel check",
    sound_name="default"
    )