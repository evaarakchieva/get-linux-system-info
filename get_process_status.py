import os
import logging


def read_status_file():
    """Reads the /proc/self/status file and returns its content as a list of lines."""
    try:
        with open('/proc/self/status', 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        logging.warning("File not found: /proc/self/status")
        return []
    except Exception as e:
        logging.error(f"Error reading file /proc/self/status: {str(e)}")
        return []


def parse_status_line(line):
    """Parses a line from the /proc/self/status file and returns a key-value pair."""
    k, v = map(str.strip, line.strip().split(':', 1))
    return k, v


def get_process_status():
    """Returns information about the process's status."""
    status = {}
    status_lines = read_status_file()
    for line in status_lines:
        if not line.strip():
            continue

        k, v = parse_status_line(line)

        for left, right in (('VmRSS', 'RSS'), ('RssAnon', 'Anon'), ('RssFile', 'Buffers'), ('Threads', 'Threads'),
                            ('Cpus_allowed', 'Cpus allowed'), ('Cpus_allowed_list', 'Cpus allowed list'),
                            ('FDSize', 'Descriptors size')):
            if k == left:
                status[right] = v

        try:
            status['Execute path'] = os.readlink('/proc/self/exe')
            status['Descriptors open'] = len(os.listdir('/proc/self/fd'))
        except Exception as e:
            logging.error(f"Error reading file /proc/self/exe or /proc/self/fd: {str(e)}")

    return status
