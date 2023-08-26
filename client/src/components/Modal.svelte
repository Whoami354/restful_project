<script>
  export let showModal;
  export let title = "";
</script>

{#if showModal}
  <div class="fixed inset-0 flex items-center justify-center">
    <div class="fixed inset-0 bg-black opacity-50" on:click></div>
    <div class="modal-container relative bg-slate-700 px-6 py-4 rounded-2xl max-w-full overflow-y-auto overflow-x-hidden">
      <div class="flex items-center justify-between mb-4 gap-2">
        <h2 class="text-2xl">{title}</h2>
        <div class="close-button text-3xl p-2 -my-2 -mx-3 cursor-pointer rounded-full hover:bg-gray-300 hover:bg-opacity-50" on:click>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>          
        </div>
      </div>
      <div class="modal-content">
        <slot></slot>
      </div>
    </div>
  </div>
{/if}

<style>
  .modal-container::-webkit-scrollbar {
    width: 10px;
  }

  .modal-container {
    scrollbar-width: thin;
    scrollbar-color: #EDF2F7;
    max-height: 80vh;
    overflow-y: auto;
  }

  .modal-container::-webkit-scrollbar-track {
    background-color: #EDF2F7;
    border-radius: 9999px;
  }

  .modal-container::-webkit-scrollbar-thumb {
    background-color: #999a9a;
    border-radius: 9999px;
  }

  .modal-container::-webkit-scrollbar-thumb:hover {
    background: #A0AEC0;
  }
</style>