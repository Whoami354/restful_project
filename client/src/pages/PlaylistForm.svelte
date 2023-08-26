<script>
    import {getList, getListItems, getLists, postList, updateList} from '../api';
    import {onMount} from "svelte";
    import {Link} from "svelte-routing";
    import PageHeader from "../components/PageHeader.svelte";
    import PageContent from "../components/PageContent.svelte";

    export let id = "";
    export let isCreate = false;
    export let name = "";
    export let vendor = "";
    export let time_range = ""
    export let limit = ""
    export let offset = ""
    export let type = ""
    export let _id = ""

    async function handleSubmit() {
        let list = {
            name,
            vendor,
            params: {
                time_range,
                limit,
                offset,
            },
            type,
        }

        if (!isCreate) {
            updateList(id, list)
        } else {
            postList(list)
        }

        spotifyData = await getListItems(id)


    }

    let data;
    let spotifyData;

    if (!isCreate) {
        onMount(async () => {
            try {
                data = await getList(id)
                if (data) {
                    name = data.name
                    vendor = data.vendor
                    time_range = data.params.time_range
                    limit = data.params.limit
                    offset = data.params.offset
                    type = data.type
                }
                spotifyData = await getListItems(id)
                console.log(spotifyData)

            } catch (error) {
                console.error(error)
            }
            console.log(data)
        })
    }


</script>


<PageHeader>
    <h1 slot="title">Dashboard</h1>
</PageHeader>
<form class="flex gap-2 " on:submit|preventDefault={handleSubmit}>
    <div class="flex flex-col w-100">
        <label class="font-bold text-left">Name</label>
        <input type="text" bind:value={name}
               class="bg-slate-600 hover:bg-slate-500 text-white-500 border border-gray-400 rounded-lg  px-4 py-2"/>
    </div>
    <div class="flex flex-col gap-1">
        <label class="font-bold text-left">Vendor</label>
        <select type="text" bind:value={vendor}
                class="bg-slate-600 border hover:bg-slate-500 text-white-500 rounded-lg px-4 py-2">
            <option value="spotify">Spotify</option>
        </select>
    </div>
    <div class="flex flex-col gap-1">
        <label class="font-bold text-left">Time_Range</label>
        <select type="text" bind:value={time_range}
                class="bg-slate-600 border hover:bg-slate-500 text-white-500 rounded-lg px-4 py-2">
            <option value="short_term" label="Letzte 4 Wochen"/>
            <option value="medium_term" label="Letzte 6 Monate"/>
            <option value="long_term" label="All-Time"/>
        </select>
    </div>
    <div class="flex flex-col gap-1">
        <label class="font-bold text-left">Limit</label>
        <input type="number" bind:value={limit}
               min="0"
               max="50"
               class="bg-slate-600 border hover:bg-slate-500 text-white-500 rounded-lg px-4 py-2"/>
    </div>
    <div class="flex flex-col gap-1">
        <label class="font-bold text-left">Offset</label>
        <input type="text" bind:value={offset}
               class="bg-slate-600 border hover:bg-slate-500 text-white-500 rounded-lg  px-4 py-2"/>
    </div>
    <div class="flex flex-col gap-1">
        <label class="font-bold text-left">Type</label>
        <select type="text" bind:value={type}
                class="bg-slate-600 border hover:bg-slate-500 text-white-500 rounded-lg  px-4 py-2">
            <option value="tracks" label="Lieder"/>
            <option value="artists" label="Interpreten"/>
        </select>
    </div>
    <button class="ml-auto bg-primary-600 hover:bg-primary-500 text-black rounded-full py-2 px-4">
        Liste { isCreate ? "hinzufügen" : "aktualisieren"}
    </button>
</form>
<PageContent>

    <header class="flex justify-between items-center">
        <h2 class="font-bold uppercase text-left text-xl mb-3">Items</h2>
    </header>
    {#if spotifyData}
        {#each spotifyData.items as item}
            <div class="flex items-center mb-2 p-2">
                <img class="mr-5" src="{item.album.images[2].url}" width="{item.album.images[2].width}"
                     height="{item.album.images[2].height}">
                <p class="w-1/5 text-left">
                    { item.artists.map(a => {
                        return a.name
                    })}
                </p>
                <p class="w-2/5 text-left">
                    {item.name}
                </p>
                <audio controls>
                    <source src={item.preview_url} type="audio/mp3">
                </audio>

            </div>
        {/each}
    {/if}
</PageContent>

