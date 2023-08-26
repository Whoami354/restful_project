<script>
    import PostItem from "./PostItem.svelte";
    import {getPosts} from "../api";
    import {onMount} from "svelte";

    const localStorageKey = "cachedPosts"
    let cachedPosts = []

    let posts;
    onMount(async () => {
        const lastmodified = localStorage.getItem("lastmodified");
        const response = await getPosts(lastmodified);
        if(response){
            cachedPosts = response.data;
            localStorage.setItem(localStorageKey, JSON.stringify(cachedPosts));
            localStorage.setItem("lastmodified", response.lastmodified);
        } else {
            cachedPosts = JSON.parse(localStorage.getItem(localStorageKey));
        }
        posts = cachedPosts;
    });
</script>


{#if posts}
    {#each posts as post}
        <PostItem {post}/>
    {/each}
{:else}
    <p>Loading...</p>
{/if}