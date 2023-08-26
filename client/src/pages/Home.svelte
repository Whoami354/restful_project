<script>
  function handleLogin() {
    window.location.href = "http://localhost:8000/login";
  }
</script>

<main>
  <body>
    <div class="h1-next-to-button">
      <h1 class="font-bold">Willkommen bei Socialtunes</h1>
    <button on:click={handleLogin} class="bg-primary-500 py-2 px-4 rounded-lg font-medium text-white-950 hover:bg-primary-200">Login</button>
    </div>
    <section class="hero">
      <div class="wrapper">
        <p class="description">Verbinde deine Deezer- und Spotify-Konten mit Twitter und entdecke eine neue Art, Musik zu teilen und zu entdecken.</p>
        <p class="description">Mit Socialtunes kannst du ganz einfach Playlists von Deezer und Spotify konvertieren und sie mit deinen Freunden auf Twitter teilen.</p>
      </div>
    </section>
    
    <footer>
      <p class="footer">© 2023 Socialtunes</p>
    </footer>
  </body>
</main>

<style>
  .h1-next-to-button{
    display: flex;
    align-items: center;
  }
  button{
    margin-left: auto;
    margin-right: 4rem;
    margin-top: 5rem;
  }
  .description{
    font-size: 1.5rem;
    font-weight: 400;
    color: #303030;
  }
  footer{
    margin-top: 10rem;
    text-align: center;
  }
  h1{
    margin-left: 4rem;
    margin-top: 5rem;
    font-size: 3rem;
  }
  section{
    margin-top: 10rem; 
    padding-block: 10rem;
    align-items: right;
  }
  .wrapper{
    max-width: 1200px;
    margin: 0 auto;
    padding-inline: 1rem;
  }
  .hero{
    position: relative;
    isolation: isolate;
  }
  .hero::after{
    content:'';
    background-image: linear-gradient(
      45deg,
      #12c2e9,
      #50e6cd,
      #00FF95
    );
    position: absolute;
    z-index: -1;
    inset: 0; 
    transform: skewY(-5deg);
    
  }
</style>
