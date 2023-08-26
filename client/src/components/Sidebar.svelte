<script>
    import {Link} from 'svelte-routing';
</script>

<div class="sidebar h-full bg-gray-700">
    <ul class="mt-4">
        <li>
            <Link to="/dashboard" class="block py-2 px-4 text-gray-800 hover:bg-gray-900 text-white-200">Dashboard
            </Link>
        </li>
        <li>
            <Link to="/posts" class="block py-2 px-4 text-gray-800 hover:bg-gray-900 text-white-200">Posts</Link>
        </li>
        <li>
            <Link to="/converter" class="block py-2 px-4 text-gray-800 hover:bg-gray-900 text-white-200">Converter
            </Link>
        </li>
        <li>
            <Link to="/playlists" class="block py-2 px-4 text-gray-800 hover:bg-gray-900 text-white-200">Playlists
            </Link>
        </li>
    </ul>
</div>
  