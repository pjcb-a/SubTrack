<script setup>
import { useRouter } from 'vue-router';
import ProfileSection from './ProfileSection.vue';
import AccountSection from './AccountSection.vue';
import PreferencesSection from './PreferencesSection.vue';
import NotificationSection from './NotificationSection.vue';
import DataSection from './DataSection.vue';

const router = useRouter();

const goBack = () => {
    router.push('/dashboard');
}
</script>

<template>
    <div class="settings-page">
        <button class="back-btn" @click="goBack">
            <i class="fa-solid fa-arrow-left"></i> Back to Dashboard
        </button>
        <h1> <i class="fa-solid fa-gear"></i> Settings</h1>
    </div>

    <div class="settings-content">
        <ProfileSection />
        <AccountSection />
        <PreferencesSection />
        <NotificationSection />
        <DataSection />
    </div>

</template>

<style scoped>
.settings-page {
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
    animation: fadeIn 0.3s ease;
}

.settings-header {
    margin-bottom: 30px;
}

.settings-header h1 {
    margin-top: 20px;
    color: var(--app-heading);
    display: flex;
    align-items: center;
    gap: 15px;
}

.settings-stack {
    display: flex;
    flex-direction: column;
    gap: 25px;
    padding-bottom: 50px;
}

.back-btn {
    background: var(--app-surface-soft);
    border: 1px solid var(--app-border);
    color: var(--app-text);
    padding: 8px 16px;
    border-radius: 10px;
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

@media (max-width: 959px) {
  .settings-page {
    padding: 15px;
  }
  .settings-stack {
    gap: 15px;
  }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>