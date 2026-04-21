<script setup>

</script>

<template>
  <section class="settings-card">
    <div class="card-header">
      <h3><i class="fa-solid fa-circle-user"></i> Profile Details</h3>
    </div>
    
    <div class="profile-content">
      <div class="avatar-display">
        <div class="initials-circle"> {{ userInitials }} </div>
      </div>

      <div class="form-group">
        <label>Username</label>
        <input type="text" class="settings-input" value=" " />
        <button class="update-btn">Save Changes</button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.profile-content {
  display: flex;
  gap: 30px;
  align-items: center;
}

.initials-circle {
  width: 80px;
  height: 80px;
  background: var(--app-sidebar-bg);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  font-weight: 700;
  box-shadow: var(--app-shadow-soft);
}

.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.settings-input {
  background: var(--app-surface-alt);
  border: 1px solid var(--app-border);
  padding: 12px;
  border-radius: 12px;
  color: var(--app-text);
}

.update-btn {
  background: var(--app-accent);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  align-self: flex-start;
}

.update-btn:hover {
  background: var(--app-accent-strong);
}
@media (max-width: 600px) {
  .profile-content { flex-direction: column; text-align: center; }
  .update-btn { align-self: stretch; }
}
</style>