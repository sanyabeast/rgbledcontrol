import multiprocessing
import time


def cpu_load():
    while True:
        pass


def load_cpu(percentage):
    num_cpus = multiprocessing.cpu_count()
    num_processes = int(num_cpus * (percentage / 100))

    processes = []
    for _ in range(num_processes):
        process = multiprocessing.Process(target=cpu_load)
        process.start()
        processes.append(process)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python cpu_load.py <percentage>")
        sys.exit(1)

    percentage = float(sys.argv[1])
    if percentage < 0 or percentage > 100:
        print("Percentage should be between 0 and 100.")
        sys.exit(1)

    load_cpu(percentage)