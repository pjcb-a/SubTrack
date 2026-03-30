<template>
  <section class="settings-card shadow-card">
    <div class="card-header">
      <h3><i class="fa-solid fa-shield-halved"></i> Account Security</h3>
    </div>
    
    <div class="section-content">
      <div class="input-group">
        <label>Email Address</label>
        <div class="input-with-icon">
          <input type="email" value="@example.com" readonly />
          <i class="fa-solid fa-lock"></i>
        </div>
        <p class="input-help">Email cannot be changed directly for security.</p>
      </div>

      <div class="action-row">
        <button class="secondary-btn">Change Password</button>
      </div>

      <div class="danger-zone">
        <h4>Danger Zone</h4>
        <p>Permanently delete your account and all subscription data.</p>
        <button class="delete-btn">Delete Account</button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.danger-zone {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid var(--app-border);
}
.danger-zone h4 {
  color: var(--app-danger);
  margin-bottom: 5px;
}
.danger-zone p {
  font-size: 0.85rem;
  color: var(--app-text-muted);
  margin-bottom: 15px;
}
.delete-btn {
  background: transparent;
  border: 1px solid var(--app-danger);
  color: var(--app-danger);
  padding: 10px 20px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.delete-btn:hover {
  background: var(--app-danger);
  color: white;
}
</style>