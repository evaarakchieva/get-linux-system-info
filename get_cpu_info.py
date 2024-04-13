import re
import logging


def read_cpuinfo_file():
    """Reads the /proc/cpuinfo file and returns its content as a list of lines."""
    try:
        with open('/proc/cpuinfo', 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        logging.warning("File not found: /proc/cpuinfo")
        return []
    except Exception as e:
        logging.error(f"Error reading file /proc/cpuinfo: {str(e)}")
        return []


def parse_cpuinfo_line(line):
    """Parses a line from the /proc/cpuinfo file and returns a key-value pair."""
    k, v = map(str.strip, line.strip().split(':', 1))
    return k, v


def get_cpu_info():
    """Returns information about the host's CPU."""
    result = {}
    cpu = {}
    cpu_list = []
    cpuinfo_lines = read_cpuinfo_file()
    for line in cpuinfo_lines:
        if not line.strip():
            continue

        k, v = parse_cpuinfo_line(line)

        if k == 'processor':
            if cpu:
                cpu_list.append(cpu)
            cpu = {}

        for a, b in (('model name', 'Model name'), ('cpu MHz', 'CPU MHz'), ('cache size', 'Cache size'), ('physical id', 'Physical ID'), ('core id', 'Core ID'), ('cpu cores', 'CPU cores')):
            if k == a:
                cpu[b] = v

        cpu_list.append(cpu)
        names = set([a.get('Model name') for a in cpu_list])
        if len(names) == 1:
            result['processorName'] = re.sub(r'\s+', ' ', names.pop())
        result['processorsCount'] = len(set([a.get('Physical ID') for a in cpu_list]))
        result['coresCount'] = len(set([a.get('Core ID') for a in cpu_list]))
        result['maxFreq'] = int(max(float(a.get('CPU MHz', 0)) for a in cpu_list))
        result['logicalCoresCount'] = len(cpu_list)

    return result
