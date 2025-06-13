import getpass
import platform
from enum import Enum

import distro
import cpuinfo

def get_system_info() -> dict[str,any]:
    return {
        "platform": platform.system(),              # e.g., 'Linux'
        "machine": platform.machine(),              # e.g., 'armv7l'
        "processor": platform.processor(),          # sometimes empty
        "cpu_brand": cpuinfo.get_cpu_info().get("brand_raw", ""),
        "architecture": platform.architecture()[0], # e.g., '32bit' or '64bit'
        "distro": distro.name(pretty=True),
        "username": getpass.getuser()
    }

class EnumPlatform(Enum):
    UNKNOWN = 0
    DESKTOP = 1
    RASPBERRY_PI = 2

def classify_host() -> EnumPlatform:
    info = get_system_info()
    cpu = info["cpu_brand"].lower()
    mach = info["machine"]

    if "raspberry" in cpu or "bcm" in cpu or "arm" in mach and "linux" in info["platform"].lower():
        return EnumPlatform.RASPBERRY_PI
    elif "intel" in cpu or "amd" in cpu:
        return EnumPlatform.DESKTOP
    else:
        return EnumPlatform.UNKNOWN