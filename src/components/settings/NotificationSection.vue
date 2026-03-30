<script setup>

</script>

<template>
  <section class="settings-card">
    <div class="card-header">
      <h3><i class="fa-solid fa-bell"></i> Notifications</h3>
    </div>

    <div class="toggle-list">
      <div class="toggle-item">
        <div class="toggle-info">
          <span>Renewal Reminders</span>
          <p>Get notified 3 days before a subscription is due.</p>
        </div>
        <label class="switch">
          <input type="checkbox" checked>
          <span class="slider"></span>
        </label>
      </div>

      <div class="toggle-item">
        <div class="toggle-info">
          <span>Monthly Reports</span>
          <p>Receive a summary of your spending every month.</p>
        </div>
        <label class="switch">
          <input type="checkbox">
          <span class="slider"></span>
        </label>
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
    color: var(--app-text); 
}

.toggle-info p { 
    font-size: 0.8rem; 
    color: var(--app-text-muted); 
}

.switch { 
    position: relative; 
    display: inline-block; 
    width: 44px; 
    height: 24px; 
}

.switch input { 
    opacity: 0; 
    width: 0; 
    height: 0; 
}

.slider {
  position: absolute; 
  cursor: pointer; 
  inset: 0;
  background-color: var(--app-surface-soft); 
  border-radius: 24px; 
  transition: .3s;
}

.slider:before {
  position: absolute; 
  content: ""; 
  height: 18px; 
  width: 18px;
  left: 3px; 
  bottom: 3px; 
  background-color: white; 
  border-radius: 50%; 
  transition: .3s;
}

input:checked + .slider { 
    background-color: var(--app-accent); 
}

input:checked + .slider:before { 
    transform: translateX(20px); 
}
</style>