<script>
    import Modal from './../components/Modal.svelte';
    import Sidebar from './../components/Sidebar.svelte';
    import PageHeader from "../components/PageHeader.svelte";
    import PageContent from "../components/PageContent.svelte";

    let platform = "spotify";
    let showModal = false;
    let playlistID = "5kBfxuOrLuyZXm3FFJaea6";

    function doModal() {
        showModal = true;
    }

    function handleConvertPlaylist() {
        fetch("http://localhost:8000/convert/" + platform + "/" + playlistID, {method: "GET", credentials: "include"});
    }

    function closeModel() {
        showModal = false;
    }
</script>

<style>
    h1 {
        margin-left: 0rem;
        margin-top: 1rem;
        font-size: 2rem;
    }

    .convert-button {
        margin-top: 1.5rem;
    }
</style>

<PageHeader>
    <h1 slot="title">Converter</h1>
    <button slot="add" on:click={doModal}
            class="bg-primary-500 py-2 px-4 rounded-lg font-medium text-white-950 hover:bg-primary-200 convert-button">
        Convert Playlist
    </button>
</PageHeader>

<PageContent>
</PageContent>
<Modal title="Convert Playlist" {showModal} on:click={closeModel}>
    <select name="provider" class="bg-slate-800" bind:value={platform}>
        <option value="spotify" class="bg-slate-700">Spotify</option>
        <option value="deezer" class="bg-slate-700">Deezer</option>
    </select>
    <input bind:value={playlistID} type="text" placeholder="PlaylistID" class="bg-slate-800"/>
    <button on:click={handleConvertPlaylist}
            class="bg-primary-500 py-2 px-4 rounded-lg font-medium text-white-950 hover:bg-primary-200">Convert
    </button>
</Modal>
