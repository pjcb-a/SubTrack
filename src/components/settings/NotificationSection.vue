<script setup>
import { computed } from 'vue';
import { useUserSettings } from '../../composables/useUserSettings';

const { settings, settingsSaving, updateSettings } = useUserSettings();

const renewalEnabled = computed(() => settings.value?.renewal_reminders_enabled ?? true);
const reportsEnabled = computed(() => settings.value?.monthly_reports_enabled ?? false);

const toggleSetting = async (field, event) => {
  await updateSettings({ [field]: event.target.checked });
};
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
          <p>Get notified before a subscription is due.</p>
        </div>
        <label class="switch">
          <input
            :checked="renewalEnabled"
            :disabled="settingsSaving"
            type="checkbox"
            @change="toggleSetting('renewal_reminders_enabled', $event)"
          >
          <span class="slider"></span>
        </label>
      </div>

      <div class="toggle-item">
        <div class="toggle-info">
          <span>Monthly Reports</span>
          <p>Store your preference for monthly summary reports.</p>
        </div>
        <label class="switch">
          <input
            :checked="reportsEnabled"
            :disabled="settingsSaving"
            type="checkbox"
            @change="toggleSetting('monthly_reports_enabled', $event)"
          >
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
