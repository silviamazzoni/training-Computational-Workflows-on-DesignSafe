def t_jobs_getJobHistory(t,jobUuid):
    try: 
        JobHistory = t.jobs.getJobHistory(jobUuid=jobUuid)
        return JobHistory
    except Exception as e:
        print(e)
        return -1