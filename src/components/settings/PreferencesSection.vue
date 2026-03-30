<template>
  <section class="settings-card">
    <div class="card-header">
      <h3><i class="fa-solid fa-earth-asia"></i> Regional & Appearance</h3>
    </div>

    <div class="pref-grid">
      <div class="field">
        <label>Primary Currency</label>
        <select class="settings-select">
          <option value="PHP">Philippine Peso (₱)</option>
          <option value="USD">US Dollar ($)</option>
        </select>
      </div>

      <div class="field">
        <label>Timezone</label>
        <select class="settings-select">
          <option>Asia/Manila (GMT+8)</option>
        </select>
      </div>
    </div>
  </section>
</template>

<style scoped>
.pref-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.field label {
  display: block;
  font-size: 0.85rem;
  margin-bottom: 8px;
  color: var(--app-text-muted);
}
.settings-select {
  width: 100%;
  padding: 12px;
  border-radius: 12px;
  background: var(--app-surface-alt);
  border: 1px solid var(--app-border);
  color: var(--app-text);
  cursor: pointer;
}
@media (max-width: 600px) {
  .pref-grid { grid-template-columns: 1fr; }
}
</style>