<template>
  <section class="settings-card shadow-card">
    <div class="card-header">
      <h3><i class="fa-solid fa-database"></i> Data Management</h3>
    </div>

    <div class="data-actions">
      <div class="data-box">
        <i class="fa-solid fa-file-export"></i>
        <span>Export Data</span>
        <button class="action-btn">Download CSV</button>
      </div>

      <div class="data-box">
        <i class="fa-solid fa-file-import"></i>
        <span>Import Data</span>
        <button class="action-btn">Upload CSV</button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.data-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.data-box {
  background: var(--app-surface-alt);
  padding: 20px;
  border-radius: 15px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}
.data-box i { font-size: 1.5rem; color: var(--app-accent); }
.action-btn {
  width: 100%;
  padding: 8px;
  background: var(--app-surface-soft);
  border: 1px solid var(--app-border);
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}
@media (max-width: 600px) {
  .data-actions { grid-template-columns: 1fr; }
}
</style>