import os
import logging


def read_file(path):
    """Reads a file and returns its content."""
    try:
        with open(path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        logging.warning(f"File not found: {path}")
        return None
    except Exception as e:
        logging.error(f"Error reading file {path}: {str(e)}")
        return None


def get_device_model(device):
    """Returns the model of a device."""
    return read_file(f'/sys/block/{device}/device/model')


def get_device_size(device):
    """Returns the size of a device."""
    device_name = os.listdir(f'sys/bus/scsi/devices/{device}/block')[0]
    size = read_file(f'/sys/bus/scsi/devices/{device}/block/{device_name}/size')
    return int(size) * 512 if size else None


def get_host_disks():
    """Returns information about the host's disks."""
    disks = {}
    block_devices = os.listdir('/sys/bus/scsi/devices/')
    for device in block_devices:
        model = get_device_model(device)
        size = get_device_size(device)
        if model and size:
            disks[device] = {'model': model, 'size': size}

    return disks
