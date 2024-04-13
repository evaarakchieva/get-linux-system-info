import json
import logging

from get_cgroups_info import get_cgroups_info
from get_cpu_info import get_cpu_info
from get_disks_info import get_host_disks
from get_mem_info import get_host_mem
from get_process_status import get_process_status


def generate_output():
    """Generates a dictionary with system information."""
    try:
        output = {
            'cpu_info': get_cpu_info(),
            'process_status': get_process_status(),
            'mem_info': get_host_mem(),
            'disks_info': get_host_disks()
        }
        return output
    except Exception as e:
        logging.error(f"Error generating output: {str(e)}")
        return {}


def print_output():
    """Prints the generated output in a pretty JSON format."""
    try:
        print(json.dumps(generate_output(), indent=4).replace('\\u0000', ''))
    except Exception as e:
        logging.error(f"Error printing output: {str(e)}")


if __name__ == '__main__':
    print_output()
