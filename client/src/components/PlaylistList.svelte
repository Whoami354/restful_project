<script>
    import {onMount} from "svelte";
    import {deleteList, getLists} from "../api.js"
    import {Link, navigate, links, Router} from "svelte-routing";

    const basePath = "playlists"
    let etag;
    let lists;
    onMount(async () => {
        try {
            const response = await getLists();
            // etag = response.headers.get("ETag");
            // console.log(etag)
            lists = response
        } catch (error) {
            console.error(error)
        }
    })

    const deleteItem = (list_Id) => {
        deleteList(list_Id).then(() => {
            lists = lists.filter(list => {
                return list._id !== list_Id
            })
        })
    }

</script>

<div class="flex-col divide-y">
    {etag}
    {#if lists}
        {#each lists as list}
            <div class="flex justify-between p-3">
                <div class=" text-left">
                    <p class="text-2xl">{list.name}</p>
                    <small>{list.vendor.toUpperCase()}</small>
                </div>
                <div>
                    <a href={`${basePath}/${list._id}`}>Edit</a>
                    <button on:click={() => deleteList(list._id)}>Delete</button>
                </div>
            </div>
        {/each}
    {/if}
</div>