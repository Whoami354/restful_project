<script>
    import {Router, Route} from "svelte-routing";

    import Dashboard from "./pages/Dashboard.svelte";
    import Home from "./pages/Home.svelte";
    import Converter from "./pages/Converter.svelte";
    import PostPage from "./pages/PostPage.svelte";
    import PlaylistPage from "./pages/PlaylistPage.svelte";
    import PostList from "./components/PostList.svelte";
    import ListForm from "./components/ListForm.svelte";
    import List from "./components/List.svelte";
    import Sidebar from "./components/Sidebar.svelte";
    import PlaylistForm from "./pages/PlaylistForm.svelte";
</script>

<Router>
    <Sidebar/>
    <main>
        <Route path="/" component={Home}></Route>
        <Route path="/dashboard" component={Dashboard}></Route>
        <Route path="/posts" component={PostPage}/>
        <Route path="/converter" component={Converter}></Route>
        <Route path="/playlists" component={PlaylistPage}></Route>
        <Route path="/playlists/:id" let:params>
            <PlaylistForm id={params.id} isCreate={false}/>
        </Route>
        <Route path="/playlists/new">
            <PlaylistForm isCreate={true}/>
        </Route>

    </main>
</Router>

<style>
    .sidebar {
        grid-area: sidebar;
    }

    main {
        grid-area: main;
    }
</style>