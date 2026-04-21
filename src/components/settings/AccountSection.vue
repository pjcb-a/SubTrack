<script setup>

</script>

<template>
  <section class="settings-card">
    <div class="card-header">
      <h3><i class="fa-solid fa-shield-halved"></i> Account Security</h3>
    </div>
    
    <div class="section-content">
      <div class="input-group">
        <label>Email Address</label>
        <div class="input-with-icon">
          <input type="email" class="settings-input" value="johnpaul@example.com" readonly />
          <i class="fa-solid fa-lock"></i>
        </div>
        <p class="input-help">Email cannot be changed directly for security.</p>
      </div>

      <div class="action-row">
        <button class="settings-btn-secondary">Change Password</button>
      </div>

      <div class="danger-zone">
        <div class="danger-info">
          <h4>Danger Zone</h4>
          <p>Permanently delete your account and all subscription data. This action is irreversible.</p>
        </div>
        <button class="settings-btn-danger">Delete Account</button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.section-content { 
    display: flex; 
    flex-direction: column; 
    gap: 20px; 
}

.input-group {
  display: flex; 
  flex-direction: column; 
  gap: 4px;
}

.input-group label, .input-group p {
  margin-left: 5px;
}

.input-with-icon { 
    position: relative; 
}

.input-with-icon i {
  position: absolute; 
  right: 15px; 
  top: 50%;
  transform: translateY(-50%); 
  color: var(--app-text-muted); 
  font-size: 0.9rem;
}

.settings-input {
  background: var(--app-surface-alt);
  border: 1px solid var(--app-border);
  padding: 12px;
  border-radius: 12px;
  color: var(--app-text);
}

.input-help { 
    font-size: 0.75rem; 
    color: var(--app-text-muted); 
    margin-top: 5px; 
}

.settings-btn-secondary {
  background: var(--app-surface-soft); 
  border: 1px solid var(--app-border);
  color: var(--app-text); 
  padding: 10px 20px; 
  border-radius: 12px;
  font-weight: 600; 
  cursor: pointer; 
  transition: 0.2s;
}

.danger-zone {
  margin-top: 20px; 
  padding-top: 20px; 
  border-top: 1px solid var(--app-border);
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  gap: 20px;
}

.danger-info h4 { 
    color: var(--app-danger); 
    margin-bottom: 4px; 
}

.danger-info p { 
    font-size: 0.85rem; 
    color: var(--app-text-muted); 
    max-width: 400px; 
}

.settings-btn-danger {
  background: transparent; 
  border: 1px solid var(--app-danger);
  color: var(--app-danger); 
  padding: 10px 20px; 
  border-radius: 12px;
  font-weight: 600; 
  cursor: pointer; 
  transition: 0.2s;
}

.settings-btn-danger:hover { 
    background: var(--app-danger); 
    color: white; 
}

@media (max-width: 600px) {
  .danger-zone { 
    flex-direction: column; 
    align-items: flex-start; 
}

  .settings-btn-danger { 
    width: 100%; 
}
}
</style>