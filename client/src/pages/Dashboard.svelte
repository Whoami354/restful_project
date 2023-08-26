<script>

    import PageHeader from "../components/PageHeader.svelte";
    import PageContent from "../components/PageContent.svelte";

    import {onMount} from "svelte";
    import Sidebar from "./../components/Sidebar.svelte";
    import SpotifyPlaylistItem from "../components/SpotifyPlaylistItem.svelte";


    function handleDeezerLogin() {
        window.location.href = "http://localhost:8000/login/deezer";
    }


    function handleTwitterLogin() {
        window.location.href = "http://localhost:8000/login/twitter";
    }


    let playlists = [];

    onMount(async () => {
        let response = await fetch("http://localhost:8000/spotify/playlists", {method: "GET", credentials: "include"});
        if (!response.ok) {
            throw new Error("Failed to fetch user playlists");
        }
        playlists = await response.json()
        console.log(playlists)
    })
</script>

<PageHeader>
    <h1 slot="title">Dashboard</h1>
    <svelte:fragment slot="add">
        <button on:click={handleDeezerLogin}
                class="bg-primary-500 py-2 px-4 rounded-lg font-medium text-white-950 hover:bg-primary-200">Deezer Login
        </button>
        <button on:click={handleTwitterLogin}
                class="bg-primary-500 py-2 px-4 rounded-lg font-medium text-white-950 hover:bg-primary-200">Twitter
            Login
        </button>
    </svelte:fragment>

</PageHeader>
<PageContent>
    <div class="mt-8">
        <h2 class="text-3xl font-bold text-left mb-6">Deine Spotify Playlists</h2>
        <div class="flex flex-row flex-wrap gap-6">
            {#each playlists as playlist}
                <SpotifyPlaylistItem image_url={playlist.image_url} name={playlist.name} url={playlist.url}
                                     id={playlist.id}/>
            {/each}
        </div>
    </div>
</PageContent>
<style>
    h1 {
        margin-left: 0rem;
        margin-top: 1rem;
        font-size: 2rem;
    }
</style>
