import multiprocessing

def worker(obj, method_name):
    try:
        method = getattr(obj, method_name)
        return method_name, method()
    except Exception as e:
        return method_name, f"Error: {str(e)}"

def run_methods_in_parallel(obj, *method_names, num_processes=None):
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()

    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.starmap(worker, [(obj, method_name) for method_name in method_names])

    return dict(results)