<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import ProfileSection from './ProfileSection.vue';
import AccountSection from './AccountSection.vue';
import PreferencesSection from './PreferencesSection.vue';
import NotificationSection from './NotificationSection.vue';
import DataSection from './DataSection.vue';
import { useUserSettings } from '../../composables/useUserSettings';

const router = useRouter();
const goBack = () => router.push('/dashboard');
const { fetchSettings, settingsLoading, settingsError } = useUserSettings();

onMounted(() => {
  fetchSettings().catch(() => {});
});
</script>

<template>
    <div class="settings-page">
        <header class="settings-header">
            <button class="back-btn" @click="goBack">
                <i class="fa-solid fa-arrow-left"></i> Back to Dashboard
            </button>
            <h1><i class="fa-solid fa-gear"></i> Settings</h1>
        </header>

        <p v-if="settingsError" class="settings-error">{{ settingsError }}</p>

        <div v-if="settingsLoading" class="settings-card settings-state">Loading settings...</div>

        <div v-else class="settings-stack">
            <ProfileSection />
            <AccountSection />
            <PreferencesSection />
            <NotificationSection />
            <DataSection />
        </div>
    </div>
</template>

<style>
/* GLOBAL SETTINGS STYLES (Accessible by Children) */
.settings-card {
  background: var(--app-surface);
  border: 1px solid var(--app-border);
  border-radius: 20px;
  padding: 24px;
  box-shadow: var(--app-shadow-soft);
  transition: transform 0.2s ease;
  font-family: 'Montserrat', sans-serif;
}

.settings-card h3 {
  color: var(--app-heading);
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.1rem;
}

.settings-card h3 i {
  color: var(--app-accent);
  width: 20px;
}
</style>

<style scoped>
.settings-page {
  font-family: 'Montserrat', sans-serif;
  max-width: 850px;
  margin: 0 auto;
  animation: fadeIn 0.3s ease;
}

.settings-header {
  margin-bottom: 25px;
}

.settings-header h1 {
  margin-top: 15px;
  color: var(--app-heading);
  font-size: 1.8rem;
  display: flex;
  align-items: center;
  gap: 12px;
}

.settings-stack {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding-bottom: 60px;
}

.settings-state {
  color: var(--app-text-muted);
  text-align: center;
}

.settings-error {
  color: var(--app-danger);
  margin-bottom: 18px;
}

.back-btn {
  background: var(--app-surface-soft);
  border: 1px solid var(--app-border);
  color: var(--app-text);
  padding: 8px 16px;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  transition: all 0.2s ease;
}

.back-btn:hover {
  background: var(--app-accent);
  color: white;
}

@media (max-width: 768px) {
  .settings-page { padding: 0 10px; }
  .settings-header h1 { font-size: 1.5rem; }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
