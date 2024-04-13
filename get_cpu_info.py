from typing import Dict

def get_cpu_info() -> Dict[str, str]:
    """Returns information about the host's CPU."""
    result = {}
    key_map = {
        'model name': 'Model',
        'cpu MHz': 'Mhz',
        'cache size': 'Cache'
    }

    try:
        with open('/proc/cpuinfo', 'r') as file:
            for line in file:
                if not line.strip():
                    continue

                k, v = map(str.strip, line.strip().split(':', 1))
                if k in key_map:
                    result[key_map[k]] = v
    except FileNotFoundError:
        print("File /proc/cpuinfo not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {str(e)}")

    return result