# Include your process that need to be brought up when the server gets reboot
# processes_to_monitor =['spproxhealthmonitor2.py', 'health_check.py','xxxx.py']

# Include your process that need to be brought up when the server gets reboot. Provide string to submit your job
submit_str_map = {'spproxhealthmonitor2.py':'nohup /home/testkoch/spproxhealthmonitor/submit_job.sh 1>submit_job.out 2>submit_job.err &', 
                  'xxxx.py':'/home/testkoch/spproxhealthmonitor/submit_xxx.sh 1> submit_xxxx.out 2> submit_xxxx.err &'}
processes_to_monitor = list(submit_str_map.keys())

import subprocess
def jobs_to_monitor():
    cmd = ['ps -ef']
    jobs_to_resubmit = []
    process_list = []

    process = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE )
    [process_list.append(str(line)) for line in process.stdout]

    def exists_chk(proc):
        result = False;
        for x in process_list:
            if (proc in str(x)):
                result = True
        return result

    for proc in processes_to_monitor:
        if (not exists_chk(proc)):
            # print('Process dont exist. PLEASE RESUBMIT THAT PARTICLAR JOB')
            jobs_to_resubmit.append(proc)

    # print(jobs_to_resubmit)
    return jobs_to_resubmit

# print(jobs_to_resubmit)

def submit_jobs(jobs_to_resubmit):
    i = 0
    while i < len(jobs_to_resubmit):
        cmd = submit_str_map.get(jobs_to_resubmit[i])
        i = i + 1
        # submits your job here
        print(cmd)
        returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix
        print('returned value:', returned_value)

jobs_to_resubmit = jobs_to_monitor()
print(jobs_to_resubmit)
submit_jobs(jobs_to_resubmit)
