import subprocess
import sys
import time
import json

def read_domains_from_file(file_name) -> list:
    with open(file_name,'r') as file:
        all_domains = [line.split(',')[1].replace('\n','') for line in file]
        domains = [*all_domains[0:10],*all_domains[-10:]]
    return domains

def write_results_to_files(ping_results, trace_results):
    with open("ping.json", "w") as ping_file:
        json.dump({"date":time.strftime("%Y%m%d"), "system":sys.platform, "pings":ping_results}, ping_file)
    with open("traceroute.json", "w") as trace_file:
        json.dump({"date":time.strftime("%Y%m%d"), "system":sys.platform, "traces":trace_results}, trace_file)

def execute_commands(domains) -> tuple:
    pings = [ subprocess.Popen(['ping','-n','10',domain],shell=True,stdout=subprocess.PIPE,universal_newlines=True) for domain in domains ]
    traces = [ subprocess.Popen(['tracert','-h','30',domain],shell=True,stdout=subprocess.PIPE, universal_newlines=True) for domain in domains ]
    ping_results, trace_results = get_command_results(domains, pings, traces)
    return ping_results, trace_results

def get_command_results(domains, ping_processes, trace_processes) -> tuple:
    ping_result = [ {"target":d,"output":p.communicate()[0].strip()} for p,d in  zip(ping_processes,domains)]
    trace_result = [ {"target":d,"output":t.communicate()[0].strip()} for t,d in  zip(trace_processes,domains)]
    return ping_result,trace_result

def main():
    start_time = time.time()
    file_name = sys.argv[1]

    domains = read_domains_from_file(file_name)
    ping_results,trace_results = execute_commands(domains)
    write_results_to_files(ping_results,trace_results)

    print(f"--- {time.time() - start_time} seconds ---")

if __name__ == "__main__":
    main()