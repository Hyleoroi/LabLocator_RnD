import time
import matplotlib.pyplot as plt

# Define a decorator function to measure execution time
def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        if measure_time.execution_times.get(func.__name__) is not None:
            measure_time.execution_times[func.__name__] = execution_time + measure_time.execution_times[func.__name__]
        else:
            measure_time.execution_times[func.__name__] = execution_time
        return result
    return wrapper


measure_time.execution_times = {}  # Store the execution times in a dictionary

def calculate_running_time():
    # Calculate the total execution time for function1 and function2
    combined_time = measure_time.execution_times["get_all_pubmed_ids"] + measure_time.execution_times["get_articles_information"]
    measure_time.execution_times["Get data from the web"] = combined_time

    combined_time2 = measure_time.execution_times["get_useful_pubmed_info"] - measure_time.execution_times["Get data from the web"]
    measure_time.execution_times["Parse and edit data"] = combined_time2

    # Plot the running times on a graph
    function_names = list(measure_time.execution_times.keys())
    execution_times = list(measure_time.execution_times.values())

    function_names.remove("get_all_pubmed_ids")
    function_names.remove("get_articles_information")
    function_names.remove("get_useful_pubmed_info")
    function_names.remove("extract_relevant_information_xml")
    execution_times.remove(measure_time.execution_times["get_all_pubmed_ids"])
    execution_times.remove(measure_time.execution_times["get_articles_information"])
    execution_times.remove(measure_time.execution_times["get_useful_pubmed_info"])
    execution_times.remove(measure_time.execution_times["extract_relevant_information_xml"])


    desired_order = ["Get data from the web", "Parse and edit data", "cosine_similarity_algorithme"]

    # Sort function_names and execution_times based on the desired order
    function_names = [name for name in desired_order if name in measure_time.execution_times]
    execution_times = [measure_time.execution_times[name] for name in desired_order if
                       name in measure_time.execution_times]

    function_names[function_names.index("cosine_similarity_algorithme")] = "NLP similarity algorithme"

    timerdata = list(zip(function_names,execution_times))

    return timerdata