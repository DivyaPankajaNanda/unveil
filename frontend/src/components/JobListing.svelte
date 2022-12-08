<script lang="ts">
    import Job from "./Job.svelte"

    export let jobs : any = []

</script>

{#each jobs as job}
    <Job {job}></Job>
{/each}