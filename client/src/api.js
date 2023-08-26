const API = "http://localhost:8000";

export async function getPost(postId) {
    const response = await fetch(`${API}/posts/${postId}`);
    if (!response.ok) {
        throw new Error('Failed to fetch post');
    }
    const data = await response.json();
    return data;
}

export async function getPosts(lastmodified) {
    const headers = {};
    if (lastmodified) {
        headers['If-Modified-Since'] = lastmodified;
    }

    const response = await fetch(`${API}/posts`);
    if (response.status === 304) {
        return null;
    } else if (response.ok) {
        const lastmodified = response.headers.get('Last-Modified');
        const data = await response.json();
        return {data, lastmodified};
    } else {
        throw new Error('Failed to fetch posts');
    }
}

export async function publishPost(postId) {
    const response = await fetch(`${API}/posts/${postId}/publish`, {method: 'POST', credentials: "include"});
    if (!response.ok) {
        throw new Error("Failed to publish tweet");
    }
    const data = await response.json();
    console.log(data)
    return data;
}

export async function getMedia(media_id) {
    const response = await fetch(`${API}/media/${media_id}`);
    if (!response.ok) {
        throw new Error("Failed to get media");
    }
    const data = await response.json();
    return data;
}

export async function createPost(post) {
    const response = await fetch(`${API}/posts`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(post),
        credentials: "include"
    })
    if (!response.ok) {
        throw new Error("Failed to create Post")
    }
    const data = await response.json();
    return data;
}

export async function getLists() {
    const response = await fetch(`${API}/lists`, {method: "GET"})
    if (!response.ok) {
        throw new Error("Failed to fetch Playlists")
    }
    let data = await response.json();
    return data;
}

export async function getList(list_id) {
    const response = await fetch(`${API}/lists/${list_id}`, {method: "GET"})
    if (!response.ok) {
        throw new Error("Failed to fetch Playlist")
    }
    return await response.json();
}

export async function getListItems(list_id) {
    const response = await fetch(`${API}/lists/${list_id}/items`, {
        method: "GET",
        credentials: "include",
    })
    if (!response.ok) {
        throw new Error("Failed to fetch Playlist Items")

    }
    return await response.json();
}

export async function postList(list) {
    const response = await fetch(`${API}/lists`, {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(list)
    })
    if (!response.ok) {
        throw new Error("Failed to create Playlists")
    }
    return await response.json();
}

export async function updateList(id, data) {
    const response = await fetch(`${API}/lists/${id}`, {
        method: "PUT",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data),
    })
    if (!response.ok) {
        throw new Error("Failed to update Playlists")
    }
    return await response.json();
}


export async function deleteList(list_id) {
    const response = await fetch(`${API}/lists/${list_id}`, {
        method: "DELETE"
    })
}