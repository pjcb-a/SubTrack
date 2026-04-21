<script setup>

</script>

<template>
  <section class="settings-card">
    <div class="card-header">
      <h3><i class="fa-solid fa-credit-card"></i> Subscription Constraint</h3>
    </div>

    <div class="data-grid">
      <div class="data-panel">
        <i class="fa-solid fa-file-invoice"></i>
        <div class="panel-text">
          <span>Soft Cap</span>
          <p>Freedom to exceed your subscription spending limits.</p>
        </div>
        <button class="settings-btn-secondary">Soft Cap</button>
      </div>

      <div class="data-panel">
        <i class="fa-solid fa-file-invoice-dollar"></i>
        <div class="panel-text">
          <span>Hard Cap</span>
          <p>Set a strict limit on your subscription spending.</p>
        </div>
        <button class="settings-btn-secondary">Hard Cap</button>
      </div>
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

.settings-btn-secondary {
  background-color: var(--app-surface-alt);
  border: 2px solid var(--app-border);
  color: var(--app-text); 
  padding: 10px 20px; 
  border-radius: 12px;
  font-weight: 600; 
  cursor: pointer; 
  transition: 0.2s;
}

.settings-btn-secondary:hover {
  background-color: var(--app-accent-strong);
  color: #f5f5f5;
  border-color: transparent;
  transform: translateY(-1px);
}

@media (max-width: 700px) {
  .data-grid { 
    grid-template-columns: 1fr; 
  }
}
</style>