<script lang="ts">
    import {onMount} from "svelte"
    import * as CONSTANTS from "../constants"
    
    export let job : any
    let user_logged : any = null
    let applied_job_ids : any = []

    const apply =async (job_id : String, applicant_id : String) => {
        const res = await fetch(`${CONSTANTS.API_V1}/application`, {
			method: 'POST',
			body: JSON.stringify({
                "job_id": job_id,
                "applicant_id": applicant_id
            })
		})
		
		let result = JSON.stringify(await res.json())
        fetchUserApplications(user_logged)
    }

    const fetchUserApplications =async (user_logged : any) => {
        if(user_logged != null){
            const res = await fetch(`${CONSTANTS.API_V1}/application/user`)
            let applications = await res.json()   
            applied_job_ids = applications.map((application : any)=>application["job_id"])
        }
    }

    onMount(async () => {
        user_logged = localStorage.getItem("user") != null ? localStorage.getItem("user") : null
        await fetchUserApplications(user_logged)
    });

</script>
<div class="card job mb-3 p-2" style="width:100%,margin:auto;">
    <div class="d-flex justify-content-end">
        <!-- <div class="job-status">{job.status}</div> -->
        <!-- {#if user_logged != null && applied_job_ids.indexOf(job["_id"])==-1} -->
            <button on:click={()=>apply(job["_id"],user_logged["_id"])}>Apply</button>
        <!-- {/if} -->
    </div>
    <div class="d-flex gap-3">
        <div class="logo-container">
            <!-- <img src="{job.company.logo}" alt="logo"> -->
            <div class="logo">{job.company.name.substring(0,1)}</div>
        </div>
        <div class="d-flex flex-column gap-1">
            <h6>{job.title}</h6>
            <div>{job.company.name},{job.company.address}</div>
            <div>{job.min_experience}</div>
            <div>{job.job_location},{job.type}</div>
        </div>
    </div>
    <hr>
    <div></div>
    <div class="d-flex gap-2">
        <b>Skills: </b>
        {#each job.skills as skill}
            <div class="skill">{skill}</div>
        {/each}
    </div>
    <div class="d-flex gap-2">
        <b>Tags: </b>
        {#each job.tags as tag}
            <div class="tags">{tag}</div>
        {/each}
    </div>
    <div>
        <b>Description : </b>
        {job.description}
    </div>
</div>

<style>
    .logo-container{
        width:6rem;
    }
    .logo{
        width:4rem;
        height:4rem;
        border:0.5rem solid #3B3486;
        border-radius:50%;
        display:flex;
        justify-content: center;
        align-items: center;
    }
</style>