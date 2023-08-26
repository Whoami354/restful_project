<script>
  import { createEventDispatcher } from 'svelte';
  import { createPost } from '../api';
  import { compute_slots } from 'svelte/internal';

  export let spotify_id = "";
  export let list_id = "";
  export let template_id = "";
  export let media_id = "";
  export let caption = "";
  export let post_type = "tweet";
  export let link = null;

  const dispatch = createEventDispatcher();

  console.log(link)

  async function handleSubmit() {
    console.log("CREATE POST")
    console.log(link)
    let post = {
      list_id,
      template_id,
      caption,
      post_type
    }

    if (media_id !== "") {
      post.media_id = media_id;
    }
    if (spotify_id !== "") {
      post.spotify_id = spotify_id;
    }

    /*let post = {
    "caption": "This tweet was generated using the Socialtunes API",
    "post_type": "tweet",
    "list_id": "beispiel-list-id",
    "template_id": "beispiel-template-id",
    "media_id": "649e00e9086835a8ce3eadb1"
  }*/

    console.log(post)

    let response;

    if (link !== null) {
      console.log(link)
      console.log(link.method)
      console.log(link.href)
      response = await fetch(link.href, {method: "PATCH", headers: {'Content-Type': 'application/json'}, body: JSON.stringify(post), credentials: 'include'})
      if (!response.ok) {
        throw new Error("Failed to " + link.method + " Post!");
      }
    } else {
      response = await createPost(post)
    }

    if (response) {
      dispatch("submit")
      location.reload()
    }
  }
</script>

<form class="flex flex-col gap-2 w-80" on:submit|preventDefault={handleSubmit}>
  <div class="flex flex-col gap-1">
    <label class="font-bold text-left">Spotify ID</label>
    <input type="text" bind:value={spotify_id} class="bg-slate-600 hover:bg-slate-500 text-white-500 border border-gray-400 rounded-lg  px-4 py-2"/>
  </div>
  <div class="flex flex-col gap-1">
    <label class="font-bold text-left">List ID *</label>
    <input type="text" bind:value={list_id} class="bg-slate-600 border hover:bg-slate-500 text-white-500 rounded-lg px-4 py-2"/>
  </div>
  <div class="flex flex-col gap-1">
    <label class="font-bold text-left">Template ID *</label>
    <input type="text" bind:value={template_id} class="bg-slate-600 border hover:bg-slate-500 text-white-500 rounded-lg px-4 py-2"/>
  </div>
  <div class="flex flex-col gap-1">
    <label class="font-bold text-left">Media ID</label>
    <input type="text" bind:value={media_id} class="bg-slate-600 border hover:bg-slate-500 text-white-500 rounded-lg px-4 py-2"/>
  </div>
  <div class="flex flex-col gap-1">
    <label class="font-bold text-left">Caption</label>
    <input type="text" bind:value={caption} class="bg-slate-600 border hover:bg-slate-500 text-white-500 rounded-lg  px-4 py-2"/>
  </div>
  <div class="flex flex-col gap-1">
    <label class="font-bold text-left">Post Type</label>
    <select bind:value={post_type} class="bg-slate-600 border hover:bg-slate-500 text-white-500 rounded-lg  px-4 py-2">
      <option value="post">Post</option>
      <option value="tweet">Tweet</option>
      <option value="directmessages">Direct Messages</option>
    </select>
  </div>
  <div class="my-2">
    <button class="bg-primary-600 hover:bg-primary-500 text-black rounded-full py-2 px-4 w-full">Post hinzufügen</button>
  </div>
</form>