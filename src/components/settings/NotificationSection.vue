<script setup>
import { ref, watch } from 'vue';
import { useUserSettings } from '../../composables/useUserSettings';

const { settings, updateSettings, settingsSaving } = useUserSettings();
const renewalRemindersEnabled = ref(true);
const monthlyReportsEnabled = ref(false);
const localError = ref('');
const localMessage = ref('');

watch(
  settings,
  (nextSettings) => {
    renewalRemindersEnabled.value = nextSettings?.renewal_reminders_enabled ?? true;
    monthlyReportsEnabled.value = nextSettings?.monthly_reports_enabled ?? false;
  },
  { immediate: true },
);

const saveNotifications = async () => {
  localError.value = '';
  localMessage.value = '';

  try {
    await updateSettings({
      renewal_reminders_enabled: renewalRemindersEnabled.value,
      monthly_reports_enabled: monthlyReportsEnabled.value,
    });
    localMessage.value = 'Notification settings updated.';
  } catch (error) {
    localError.value = error.message;
  }
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
          <p>Get notified 3 days before a subscription is due.</p>
        </div>
        <label class="switch">
          <input v-model="renewalRemindersEnabled" type="checkbox">
          <span class="slider"></span>
        </label>
      </div>

      <div class="toggle-item">
        <div class="toggle-info">
          <span>Monthly Reports</span>
          <p>Receive a summary of your spending every month.</p>
        </div>
        <label class="switch">
          <input v-model="monthlyReportsEnabled" type="checkbox">
          <span class="slider"></span>
        </label>
      </div>
    </div>

    <p v-if="localError" class="feedback error">{{ localError }}</p>
    <p v-else-if="localMessage" class="feedback success">{{ localMessage }}</p>

    <button class="save-btn" :disabled="settingsSaving" @click="saveNotifications">
      {{ settingsSaving ? 'Saving...' : 'Save Notification Settings' }}
    </button>
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

.save-btn {
  margin-top: 18px;
  background: var(--app-accent);
  border: none;
  color: white;
  padding: 10px 18px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
}

.save-btn:disabled {
  opacity: 0.7;
  cursor: wait;
}

.feedback {
  font-size: 0.82rem;
}

.feedback.error {
  color: var(--app-danger);
}

.feedback.success {
  color: var(--app-accent);
}
</style>
