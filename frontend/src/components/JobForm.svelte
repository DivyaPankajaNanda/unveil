<script lang="ts">
    import {onMount} from "svelte"
    import * as CONSTANTS from "../constants"

    let job_title : String = ""
    let job_description : String = ""
    let company_name : String = ""
    let company_address : String = ""
    let company_logo : String = ""
    let min_experience : String = ""
    let job_location : String = ""
    let job_type : String = ""
    let job_skills : String = ""
    let job_tags : String = ""
    let job_status : String = ""
    
    let user_logged : any = null

    const postJob =async () => {
        if(user_logged == null)
            return

        const res = await fetch(`${CONSTANTS.API_V1}/application`, {
			method: 'POST',
			body: JSON.stringify({
                "title" : job_title,
                "description" : job_description,
                "company" : {
                    "name" : company_name,
                    "address" : company_address,
                    "logo" : company_logo
                },
                "min_experience" : min_experience,
                "job_location" : job_location,
                "type" : job_type,
                "skills" : job_skills,
                "tags" : job_tags,
                "status" : job_status
            })
		})
		
		let result = JSON.stringify(await res.json())
    }

    onMount(async () => {
        user_logged = localStorage.getItem("user") != null ? localStorage.getItem("user") : null
    });

</script>
<div class="card w-75 job-form">
    <div class="mb-3">
        <label for="exampleFormControlInput1" class="form-label">Title</label>
        <input type="email" class="form-control" bind:value={job_title}>
      </div>
      <div class="mb-3">
        <label for="exampleFormControlTextarea1" class="form-label">Description</label>
        <textarea class="form-control" bind:value={job_description} rows="2"></textarea>
      </div>
      <div class="mb-3">
        <label for="exampleFormControlInput1" class="form-label">Company Name</label>
        <input type="email" class="form-control" bind:value={company_name}>
      </div>
      <div class="mb-3">
        <label for="exampleFormControlInput1" class="form-label">Company Address</label>
        <input type="email" class="form-control" bind:value={company_address}>
      </div>
      <div class="mb-3">
        <label for="exampleFormControlInput1" class="form-label">Company Logo</label>
        <input type="email" class="form-control" bind:value={company_logo}>
      </div>
      <div class="mb-3">
        <label for="exampleFormControlInput1" class="form-label">Min Experience</label>
        <input type="email" class="form-control" bind:value={min_experience}>
      </div>
      <div class="mb-3">
        <label for="exampleFormControlInput1" class="form-label">Job Location</label>
        <input type="email" class="form-control" bind:value={job_location}>
      </div>
      <div class="mb-3">
        <label for="exampleFormControlInput1" class="form-label">Job Type</label>
        <input type="email" class="form-control" bind:value={job_type}>
      </div>
      <div class="mb-3">
        <label for="exampleFormControlInput1" class="form-label">Skills</label>
        <input type="email" class="form-control" bind:value={job_skills}>
      </div>
      <div class="mb-3">
        <label for="exampleFormControlInput1" class="form-label"> Tags</label>
        <input type="email" class="form-control" bind:value={job_tags}>
      </div>
      
</div>