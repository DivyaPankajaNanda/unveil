<script lang="ts">
import * as CONSTANTS from "../constants"

let user_email : String
let user_name : String
let user_password : String

export let signup : Boolean
let button_text : String = signup?"Signup":"Signin"


export const onSubmmit = async () => {
    if(signup == true){
        const res = await fetch(`${CONSTANTS.API_V1}/auth/signup`, {
			method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
			body: JSON.stringify({
                "email" : user_email,
                "username" : user_email,
                "name" : user_name,
                "password" : user_password,
            })
		})
		
		let result = JSON.stringify(await res.json())
    }else{
        const res = await fetch(`${CONSTANTS.API_V1}/auth/signin`, {
			method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
			body: JSON.stringify({
                "username" : user_email,
                "password" : user_password,
            })
		})
		
		let result = JSON.stringify(await res.json())
    }

}
</script>

<form class="form card w-50 p-3" style="margin:auto;">
    {#if signup}
        <div>
            <label>Name</label>
            <input type="text" class="form-control" bind:value={user_name}>
        </div>
    {/if}
    <div>
      <label>Email</label>
      <input type="text" class="form-control" bind:value={user_email}>
    </div>
    <div>
      <label>Password</label>
      <input type="password" class="form-control" bind:value={user_password}>
    </div>
    <div>
      <button type="submit" on:click={()=>onSubmmit()} class="mt-3">{button_text}</button>
    </div>
  </form>