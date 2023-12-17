import os
from tempfile import NamedTemporaryFile

from lib.typedefs import BytesOrString


def measure_on_disk_size(data: BytesOrString):
    """
    Computes the size on disk for a given data (bytes or string)
    :param data: The data for which the disk size usage is required
    :return: The disk usage of the data.
    """
    tmp_file = NamedTemporaryFile(delete=False)
    tmp_file.close()

    if isinstance(data, str):
        with open(tmp_file.name, 'w', encoding='utf-8') as file:
            file.write(data)
    elif isinstance(data, bytes):
        with open(tmp_file.name, 'wb') as file:
            file.write(data)
    else:
        raise NotImplementedError(f"Measure on disk size cannot treat the following data type: {type(data)}")

    with open(tmp_file.name, 'rb') as file:
        disk_usage = len(file.read())

    if disk_usage == 0:
        raise Exception("Empty file")

    os.remove(tmp_file.name)

    return disk_usage
