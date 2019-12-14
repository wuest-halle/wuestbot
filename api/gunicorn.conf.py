from multiprocessing import cpu_count
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

bind = "0.0.0.0:5000"
workers = cpu_count() * 2 + 1
max_requests = 50
chdir = "src"

def child_exit(server, worker):
    GunicornInternalPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)
