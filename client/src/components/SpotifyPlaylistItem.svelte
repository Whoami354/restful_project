<script>
  export let image_url;
  export let name;
  export let url;
  export let id;

  let showSuccess = false;

  function handleClick() {
    //location.href = url;
    window.open(url, "_blank").focus();
  }

  function handlePost() {

  }

  async function handleConvert() {
    let response = await fetch("http://localhost:8000/convert/spotify/" + id, {method: "GET", credentials: "include"});
    if (response.ok) {
      showSuccess = true;
      setTimeout(() => {
      showSuccess = false;
    }, 3000);
    }
  }
</script>

<div class="flex flex-col gap-2 bg-slate-700 rounded-2xl overflow-hidden w-64">
  <img src={image_url} class=""/>
  <div class="p-2 flex flex-col gap-2 justify-evenly h-full">
    <h1 class="text-left text-xl font-medium hover:underline hover:text-primary-600 cursor-pointer w-fit" on:click={handleClick}>{name}</h1>
    <button class="rounded-full text-black font-medium bg-primary-600 hover:bg-gray-500 py-2 px-4 cursor-not-allowed my-2 mx-1">Post generieren</button>
    <button class="rounded-full text-white-500 font-medium bg-secondary-500 hover:bg-secondary-600 py-2 px-4 cursor-pointer mb-2 mx-1" on:click={handleConvert}>Zu Deezer konvertieren</button>
  </div>
</div>
{#if showSuccess}
    <div class="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-50">
        <div class="bg-slate-700 p-6 rounded-md shadow-md flex items-center flex-col gap-4">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-12 h-12 text-green-500">
            <path fill-rule="evenodd" d="M8.603 3.799A4.49 4.49 0 0112 2.25c1.357 0 2.573.6 3.397 1.549a4.49 4.49 0 013.498 1.307 4.491 4.491 0 011.307 3.497A4.49 4.49 0 0121.75 12a4.49 4.49 0 01-1.549 3.397 4.491 4.491 0 01-1.307 3.497 4.491 4.491 0 01-3.497 1.307A4.49 4.49 0 0112 21.75a4.49 4.49 0 01-3.397-1.549 4.49 4.49 0 01-3.498-1.306 4.491 4.491 0 01-1.307-3.498A4.49 4.49 0 012.25 12c0-1.357.6-2.573 1.549-3.397a4.49 4.49 0 011.307-3.497 4.49 4.49 0 013.497-1.307zm7.007 6.387a.75.75 0 10-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 00-1.06 1.06l2.25 2.25a.75.75 0 001.14-.094l3.75-5.25z" clip-rule="evenodd" />
          </svg>       
          <p class="text-center text-lg">Playlist wurde erfolgreich konvertiert!</p>
        </div>
    </div>
  {/if}