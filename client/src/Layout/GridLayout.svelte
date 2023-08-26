<script>
    export let columns = 3;
    export let gap = '1rem'; 
    $: gridTemplateColumns = `repeat(${columns}, 1fr)`;
  </script>
  
  <div class="grid mt-4" style="grid-template-columns: {gridTemplateColumns}; gap: {gap}">
    <slot></slot>
  </div>
  
  <style>
    .grid {
      display: grid;
    }
  </style>
  