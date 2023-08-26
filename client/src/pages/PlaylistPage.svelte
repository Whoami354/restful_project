<script>
    import Sidebar from './../components/Sidebar.svelte';
    import PlaylistList from "../components/PlaylistList.svelte";
    import {Link, navigate} from "svelte-routing";
    import PageHeader from "../components/PageHeader.svelte";
    import PageContent from "../components/PageContent.svelte";

</script>
<style>
    .hinzufügen-button {
        margin-top: 1.5rem;
    }

    h1 {
        margin-left: 0rem;
        margin-top: 1rem;
        font-size: 2rem;
    }

    .content-container {
        margin-left: 20rem;
        margin-right: 5rem;
    }
</style>

<PageHeader>
    <h1 slot="title">Playlists</h1>

    <Link slot="add"
          class="bg-primary-500 py-2 px-4 rounded-lg font-medium text-white-950 hover:bg-primary-200 hinzufügen-button"
          to={`playlists/new`}>Hinzufügen
    </Link>

</PageHeader>
<PageContent>
    <PlaylistList/>
</PageContent>
