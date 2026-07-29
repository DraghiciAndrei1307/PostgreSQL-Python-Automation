import threading
import time
import psutil

class ResourceMonitor(threading.Thread):

    def __init__(self, process_pid: int = None, interval: float = 0.2):

        # We call the parent constructor.

        # We use the daemon=True for
        # cases when the main process crashes.
        # We want to also stop the monitor thread
        # if that happens.
        super().__init__(daemon=True)

        # create a Process object which is used
        # to monitor the current Python process
        self.process = psutil.Process(pid=process_pid)

        # sampling interval
        self.interval = interval

        # control boolean to stop
        # the thread loop when test is over
        self.running = False

        # used for read/write of the samples
        # lists from different threads
        self._lock = threading.Lock()

        # where we are going to save the samples
        self.ram_samples = []
        self.cpu_samples = []


    # Because this class inherited the Thread,
    # we have to override the run() method.

    # When we use the .start() method, this will
    # automatically call the run() method on a
    # separate thread.
    def run(self):
        """
        This is the heart of our monitor.
        """

        self.running = True

        # This will return 0.0 (internal init of psutil)
        self.process.cpu_percent()

        try:
            while self.running:
                rss_mb = self.process.memory_info().rss / 1024 / 1024  # this is measured in MB
                cpu_usage_value = self.process.cpu_percent(interval=None)

                with self._lock:
                    self.ram_samples.append(rss_mb)
                    self.cpu_samples.append(cpu_usage_value)


                time.sleep(self.interval)

        except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess
        ) as e:
            print(f"Error: {e}")
            self.stop()


    def stop(self):
        """We stop the monitor thread loop"""
        self.running = False


    def get_metrics(self) -> dict:
        """We get the metrics from the monitor thread"""

        with self._lock:
            ram_copy = list(self.ram_samples)
            cpu_copy = list(self.cpu_samples)

        metrics_dict = {}

        if cpu_copy:
            metrics_dict["cpu"] = {
                "cpu_samples": cpu_copy,
                "cpu_percent": round(sum(cpu_copy) / len(cpu_copy), 2),
                "peak_cpu": round(max(cpu_copy), 2),
            }

        if ram_copy:
            metrics_dict["ram"] = {
                "ram_samples": ram_copy,
                "ram_mean": round(sum(ram_copy) / len(ram_copy), 2),
                "peak_ram": round(max(ram_copy), 2),
            }

        return metrics_dict

    # By defining the following methods, we can use
    # this class with the 'with' syntax

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        self.join()  # waits for the thread to stop