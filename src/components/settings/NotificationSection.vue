<template>
  <section class="settings-card shadow-card">
    <div class="card-header">
      <h3><i class="fa-solid fa-bell"></i> Notifications</h3>
    </div>

    <div class="toggle-list">
      <div class="toggle-item">
        <div class="toggle-info">
          <span>Renewal Reminders</span>
          <p>Get notified 3 days before a subscription is due.</p>
        </div>
        <input type="checkbox" checked />
      </div>

      <div class="toggle-item">
        <div class="toggle-info">
          <span>Monthly Reports</span>
          <p>Receive a summary of your spending every month.</p>
        </div>
        <input type="checkbox" />
      </div>
    </div>
  </section>
</template>

<style scoped>
.toggle-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
}
.toggle-item:not(:last-child) {
  border-bottom: 1px solid var(--app-border);
}
.toggle-info span {
  font-weight: 600;
  display: block;
}
.toggle-info p {
  font-size: 0.8rem;
  color: var(--app-text-muted);
}
</style>