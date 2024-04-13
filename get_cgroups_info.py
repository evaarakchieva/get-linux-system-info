import time
import logging


def read_file(path):
    """Reads a file and returns its content as a list of lines."""
    try:
        with open(path, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        logging.warning(f"File not found: {path}")
        return []
    except Exception as e:
        logging.error(f"Error reading file {path}: {str(e)}")
        return []


def get_cpu_limit_cores():
    """Returns the CPU limit cores."""
    for line in read_file('sys/fs/cgroup/cpu/cpu.cfs_quota_us'):
        if line.strip() and int(line) != -1:
            return float(line) / 1000000
    return None


def get_mem_limit_gb():
    """Returns the memory limit in GB."""
    gb = 1024 * 1024 * 1024
    big_num = 9233372036854775807
    for line in read_file('sys/fs/cgroup/memory/memory.limit_in_bytes'):
        if line.strip() and int(line) != big_num:
            return float(line) / gb
    return None


def get_mem_usage_gb():
    """Returns the memory usage in GB."""
    gb = 1024 * 1024 * 1024
    for line in read_file('sys/fs/cgroup/memory/memory.usage_in_bytes'):
        if line.strip():
            return float(line) / gb
    return None


def get_cpu_usage_cores():
    """Returns the CPU usage cores."""
    gb = 1024 * 1024 * 1024
    for line in read_file('sys/fs/cgroup/cpu/cpuacct.usage'):
        if line.strip():
            start_time = time.time()
            cpu_usage_cores_start = int(line)
            time.sleep(5)
            cpu_usage_cores_end = int(read_file('sys/fs/cgroup/cpu/cpuacct.usage')[0].strip())
            stop_time = time.time()
            usage = (cpu_usage_cores_end - cpu_usage_cores_start) / (stop_time - start_time) / gb
            return usage
    return None


def get_cgroups_info():
    """Returns information about the process's cgroups."""
    cgroups_info = {
        'cpu_limit_cores': get_cpu_limit_cores(),
        'mem_limit_gb': get_mem_limit_gb(),
        'mem_usage_gb': get_mem_usage_gb(),
        'cpu_usage_cores': get_cpu_usage_cores()
    }
    return cgroups_info
