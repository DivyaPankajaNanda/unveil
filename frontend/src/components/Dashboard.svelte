<script lang="ts">
    import JobListing from "./JobListing.svelte"
    import {onMount} from "svelte"
    import * as CONSTANTS from "../constants"

    let user_logged : any = null

    let jobs : any = []
    let open_jobs : any = []
    let applied_jobs : any = []
    let created_jobs : any = []
    let job_list_type : Number = 1

    const fetchAllJobs =async (user_logged : any) => {
        const res = await fetch(`${CONSTANTS.API_V1}/job`)
        jobs = await res.json()   
        open_jobs = jobs.filter((job : any)=>job["status"] == CONSTANTS.JOB_OPEN_STATUS || job["status"] == CONSTANTS.JOB_ONGOING_STATUS)  
        if(user_logged != null)
        created_jobs = jobs.filter((job : any)=>job.created_by == user_logged["_id"])  
    }

    const fetchUserApplications =async (user_logged : any) => {
        if(user_logged != null){
            const res = await fetch(`${CONSTANTS.API_V1}/application/user`)
            let applications = await res.json()   
            let applied_job_ids = applications.map((application : any)=>application["job_id"])
            applied_jobs = jobs.filter((job : any)=>applications.indexOf(job["_id"]) != -1) 
        }
    }

    onMount(async () => {
        user_logged = localStorage.getItem("user") != null ? localStorage.getItem("user") : null
        await fetchAllJobs(user_logged)
        await fetchUserApplications(user_logged)
    });

</script>
<div class="p-4">
    <div class="banner d-flex gap-3">
        <div class="form-check">
            <input class="form-check-input" type=radio bind:group={job_list_type} name="job_list_type" value={1}>
            <label class="form-check-label" for="job_list_type">Open</label>
        </div>
        {#if user_logged != null}
            <div class="form-check">
                <input class="form-check-input" type=radio bind:group={job_list_type} name="job_list_type" value={2}>
                <label class="form-check-label" for="job_list_type">Applied</label>
            </div>
            <div class="form-check">
                <input class="form-check-input" type=radio bind:group={job_list_type} name="job_list_type" value={3}>
                <label class="form-check-label" for="job_list_type">Created</label>
            </div>
        {/if}
    </div>
    <div class="job-list">
        {#if job_list_type == 1}
            <JobListing jobs={open_jobs}></JobListing>
        {:else if job_list_type == 2 && user_logged != null}
            <JobListing jobs={applied_jobs}></JobListing>
        {:else if job_list_type == 3 && user_logged != null }
            <JobListing jobs={created_jobs}></JobListing>
        {/if}
    </div>
</div>
{#if user_logged == null}
    <div class="text-center">
        Stay tuned for more amazing features.
    </div>
{/if}