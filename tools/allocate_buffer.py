import sys
import ctypes
import time

def allocate_buffer(size_in_mb):
    size_in_bytes = size_in_mb * 1024 * 1024
    buffer = (ctypes.c_byte * size_in_bytes)()
    return buffer

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <buffer_size_in_mb>")
        sys.exit(1)

    try:
        buffer_size_mb = int(sys.argv[1])
    except ValueError:
        print("Invalid buffer size. Please provide an integer value.")
        sys.exit(1)

    allocated_buffer = allocate_buffer(buffer_size_mb)

    # Print the address of the allocated buffer
    print(ctypes.addressof(allocated_buffer))

    while True:
        pass
        time.sleep(10)