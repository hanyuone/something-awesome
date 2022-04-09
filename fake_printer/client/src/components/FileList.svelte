<script lang="ts">
  import type UploadedFile from "../types/UploadedFile";
  export let files: UploadedFile[];

  $: filesNum = files.length;
  $: pagesNum = files.map(file => file.pages).reduce((a, b) => a + b, 0);
</script>

<section>
  <div class="m-4">
    <p class="text-xl text-center pb-2">Sniffed files</p>
    {#if files.length === 0}
      <p class="text-center">No files sniffed!</p>
    {:else}
      <!-- Initial stats -->
      <div class="grid grid-cols-2 align-center">
        <div>Files printed: {filesNum}</div>
        <div>Pages printed: {pagesNum}</div>
      </div>
      
      <!-- Specific files -->
      <ul class="bg-white divide-y-2 shadow rounded">
        {#each files as { name, pages, time }}
        <li class="p-2 flow-root">
          <span class="float-left"><b>{name}</b></span>
          <span class="float-right">{pages} {pages === 1 ? "page" : "pages"}, printed at {time.toDateString()}</span>
        </li>
        {/each}
      </ul>
    {/if}
  </div>
</section>

<style></style>
