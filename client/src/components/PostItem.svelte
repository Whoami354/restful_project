<script>
  import { onMount } from "svelte";
  import { publishPost, getMedia } from "../api";
  import Modal from "./Modal.svelte";
  import PostForm from "./PostForm.svelte";

  export let post;

  let imageString;
  let twitterId = "";
  let createdAtFormatted = "";
  let showIds = false;
  let showModal = false;

  //console.log(post._links)

  onMount(async () => {
    //const media = await getMedia(post.media_id);
    const response = await fetch(post._links.media.href, {method: post._links.media.method})
    let media = await response.json()
    imageString = media.base64;
    createdAtFormatted = formatCreatedAt(post.created_at);
  });

  async function publish() {
    let response = await publishPost(post.post_id);
    post.twitter_id = response;
    twitterId = response;
  }

  function formatCreatedAt(createdAt) {
    const date = new Date(createdAt);
    return date.toLocaleString();
  }

  function toggleIds() {
    showIds = !showIds;
  }

  function handleEdit() {
    showModal = true;
  }

  function handleDelete() {
    const deleteLink = post._links.delete;

    if (deleteLink) {
      fetch(deleteLink.href, {method: deleteLink.method})
      .then(response => {
        if (response.ok) {
          location.reload();
        }
      })
      .catch(error => {
        console.log("Failed to delete Post with ID " + post.post_id + ", Error: " + error);
      });
    }
  }
</script>

<Modal {showModal} on:click={() => showModal = false} title="Post bearbeiten">
  <PostForm 
    spotify_id={post.spotify_id} 
    list_id={post.list_id}
    template_id={post.template_id}
    media_id={post.media_id}
    caption={post.caption}
    post_type={post.post_type}
    link={post._links.update}
  />
</Modal>
<div class="bg-gray-800 rounded-lg flex flex-col py-4 px-8 gap-4 hover:bg-gray-700 my-5 mx-2">
  <!-- <h1 class="text-center text-2xl text-white">{post.post_id}</h1> -->
  {#if imageString}
    <img src={"data:image/png;base64," + imageString} alt="Media of the Post" class="rounded-lg my-5" />
  {:else}
    <p class="text-center text-lg font-bold text-red-500">Media not found!</p>
  {/if}
  {#if showIds}
    <div class="grid grid-cols-2 gap-2">
      <div class="flex flex-col gap-1">
        <h2 class="font-medium text-lg text-white">Caption</h2>
        <p class="text-white">{post.caption}</p>
      </div>
      <div class="flex flex-col gap-1">
        <h2 class="font-medium text-lg text-white">Media ID</h2>
        <p class="text-white">{post.media_id}</p>
      </div>
      <div class="flex flex-col gap-1">
        <h2 class="font-medium text-lg text-white">List ID</h2>
        <p class="text-white">{post.list_id}</p>
      </div>
      <div class="flex flex-col gap-1">
        <h2 class="font-medium text-lg text-white">Template ID</h2>
        <p class="text-white">{post.template_id}</p>
      </div>
    </div>
  {/if}
  <div class="flex flex-col gap-1">
    <button
      on:click={toggleIds}
      class="rounded-full text-black font-medium bg-primary-600 hover:bg-primary-500 py-2 px-4 cursor-pointer"
    >
      {#if showIds}Hide IDs{:else}Show More{/if}
    </button>
  </div>
  <div class="flex flex-col gap-1">
    <h2 class="font-medium text-lg text-white">Created at</h2>
    <p class="text-white">{createdAtFormatted}</p>
  </div>
  {#if post.twitter_id}
    <div class="flex flex-col gap-1">
      <p class="text-green-600">The {post.post_type} has already been published</p>
      <h2 class="font-medium text-lg text-white">Twitter ID</h2>
      <p class="text-white">{post.twitter_id}</p>
    </div>
  {:else}
    <button
      on:click={publish}
      class="rounded-full text-black font-medium bg-primary-600 hover:bg-primary-500 py-2 px-4 cursor-pointer"
    >
      Publish {post.post_type}
    </button>
  {/if}
  <button on:click={handleEdit} class="rounded-full text-black font-medium bg-yellow-500 hover:bg-yellow-600 py-2 px-4 cursor-pointer">Edit Post</button>
  <button on:click={handleDelete} class="rounded-full text-white-500 font-medium bg-red-600 hover:bg-red-500 py-2 px-4 cursor-pointer">Delete Post</button>
</div>
