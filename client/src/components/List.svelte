<script>
    let items = [
      {
        id: 1,
        title: 'Song 1',
        author: 'Author 1',
        description: 'Description',
        imageUrl: 'https://cms-assets.tutsplus.com/cdn-cgi/image/width=850/uploads/users/114/posts/34296/final_image/Final-image.jpg',
      },
      {
        id: 2,
        title: 'Song 2',
        author: 'Author 2',
        description: 'Description',
        imageUrl: 'https://cms-assets.tutsplus.com/cdn-cgi/image/width=850/uploads/users/114/posts/34296/final_image/Final-image.jpg',
      },
      {
        id: 3,
        title: 'Song 2',
        author: 'Author 2',
        description: 'Description',
        imageUrl: 'https://cms-assets.tutsplus.com/cdn-cgi/image/width=850/uploads/users/114/posts/34296/final_image/Final-image.jpg',
      },
      {
        id: 4,
        title: 'Song 2',
        author: 'Author 2',
        description: 'Description',
        imageUrl: 'https://cms-assets.tutsplus.com/cdn-cgi/image/width=850/uploads/users/114/posts/34296/final_image/Final-image.jpg',
      },
      {
        id: 5,
        title: 'Song 2',
        author: 'Author 2',
        description: 'Description',
        imageUrl: 'https://cms-assets.tutsplus.com/cdn-cgi/image/width=850/uploads/users/114/posts/34296/final_image/Final-image.jpg',
      },
    ];
  </script>
  
  <style>
    .container{
      margin-top: 2rem;
      margin-left: 20rem;
      margin-right: 4rem;
    }

    .list-item {
      display: flex;  
      transition: background-color 0.2s ease;
      list-style-type: none;
      padding: 0;
      margin-bottom: 1rem;
    }
    
    .list-item:hover{
      background-color: #395057;
    }

    .list-item:hover .item-title{
      color: #000000;
    }

    .list-item:hover .item-author{
      color: #000000;
    }

    .list-item:hover .item-description{
      color: #000000;
    }
  
    .list-image { 
      width: 10%;
      height: 10%;
      object-fit: cover;
    }
    .item-title{
      font-size: 1.5rem;
      font-weight: 600;
    }
  </style>
  
  <div class="container">
    {#each items as item (item.id)}
      <div class="list-item">
        <img class="w-16 h-16 mr-6 rounded list-image" src={item.imageUrl} alt={item.title} />
        <div>
          <h3 class="item-title">{item.title}</h3>
          <p class="item-author">{item.author}</p>
          <p class="item-description">{item.description}</p>
        </div>
      </div>
    {/each}
  </div>
  