<script setup>

</script>

<template>
  <section class="settings-card">
    <div class="card-header">
      <h3><i class="fa-solid fa-database"></i> Data Management</h3>
    </div>

    <div class="data-grid">
      <div class="data-panel">
        <i class="fa-solid fa-file-export"></i>
        <div class="panel-text">
          <span>Export Data</span>
          <p>Download your subscriptions as a CSV file.</p>
        </div>
        <button class="settings-btn-secondary">Export</button>
      </div>

      <div class="data-panel">
        <i class="fa-solid fa-file-import"></i>
        <div class="panel-text">
          <span>Import Data</span>
          <p>Upload a CSV to bulk-add subscriptions.</p>
        </div>
        <button class="settings-btn-secondary">Import</button>
      </div>
    </div>

    <div class="history-clear">
      <div class="clear-text">
        <span>Clean Up History</span>
        <p>This will permanently remove all items from your deleted history.</p>
      </div>
      <button class="clear-btn" >
            <i class="fa-solid fa-trash"></i> Clear History
        </button>
    </div>
  </section>
</template>

<style scoped>
.data-grid { 
  display: grid; 
  grid-template-columns: 1fr 1fr; 
  gap: 15px; 
  margin-bottom: 25px; }

.data-panel {
  background: var(--app-surface-alt); 
  padding: 20px; 
  border-radius: 16px;
  display: flex; 
  flex-direction: column; 
  align-items: center; 
  text-align: center; 
  gap: 12px;
}

.data-panel i { 
  font-size: 1.4rem; 
  color: var(--app-accent); 
}

.panel-text span { 
  font-weight: 700; 
  color: var(--app-text); 
  font-size: 0.9rem; 
}

.panel-text p { 
  font-size: 0.75rem; 
  color: var(--app-text-muted); 
  margin-top: 4px; 
}

.history-clear {
  display: flex; 
  justify-content: space-between; 
  align-items: center;
  background: var(--app-surface-alt); 
  padding: 20px; 
  border-radius: 16px;
}

.clear-text span { 
  font-weight: 700; 
  color: var(--app-text); 
}

.clear-text p { 
  font-size: 0.8rem; 
  color: var(--app-text-muted); 
}

@media (max-width: 700px) {
  .data-grid { 
    grid-template-columns: 1fr; 
  }

  .history-clear { 
    flex-direction: column; 
    text-align: center; 
    gap: 15px; 
  }
}
</style>