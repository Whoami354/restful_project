<script>
    import Modal from '../components/Modal.svelte';
    import Sidebar from './../components/Sidebar.svelte';
    import PostList from './../components/PostList.svelte';
    import PostForm from '../components/PostForm.svelte';
    import PageHeader from "../components/PageHeader.svelte";
    import PageContent from "../components/PageContent.svelte";


    let showModal = false;

    function toggleModal() {
        showModal = !showModal;
    }


</script>
<style>
    h1 {
        margin-left: 0rem;
        margin-top: 1rem;
        font-size: 2rem;
    }

    .container-posts {
        margin-left: 20rem;
        margin-right: 5rem;
    }

    .post-button {
        margin-top: 1.5rem;
    }
</style>
<PageHeader>
    <h1 slot="title">Posts</h1>
    <button slot="add"
            class="bg-primary-500 py-2 px-4 rounded-lg font-medium text-white-950 hover:bg-primary-200 post-button"
            on:click={() => showModal = true}>Post hinzufügen
    </button>

</PageHeader>
<Modal {showModal} on:click={toggleModal} title="Post hinzufügen">
    <PostForm/>
</Modal>
<PageContent>

    <PostList/>
</PageContent>