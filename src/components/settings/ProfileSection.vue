<script setup>
import { computed, ref, watch } from 'vue';
import { useAuth } from '../../composables/useAuth';
import { useUserSettings } from '../../composables/useUserSettings';

const { currentUser } = useAuth();
const { settingsSaving, updateProfile } = useUserSettings();
const username = ref('');
const statusMessage = ref('');
const localError = ref('');

watch(
  currentUser,
  (user) => {
    username.value = user?.username || '';
  },
  { immediate: true },
);

const userInitials = computed(() => (
  username.value
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase() || '')
    .join('') || 'ST'
));

const saveProfile = async () => {
  localError.value = '';
  statusMessage.value = '';

  try {
    await updateProfile(username.value);
    statusMessage.value = 'Profile updated.';
  } catch (error) {
    localError.value = error.message;
  }
};
</script>

<template>
  <section class="settings-card">
    <div class="card-header">
      <h3><i class="fa-solid fa-circle-user"></i> Profile Details</h3>
    </div>

    <div class="profile-content">
      <div class="avatar-display">
        <div class="initials-circle">{{ userInitials }}</div>
      </div>

      <div class="form-group">
        <label>Username</label>
        <input v-model="username" type="text" class="settings-input" />
        <div class="profile-actions">
          <button class="update-btn" :disabled="settingsSaving" @click="saveProfile">
            {{ settingsSaving ? 'Saving...' : 'Save Changes' }}
          </button>
          <span v-if="statusMessage" class="status-ok">{{ statusMessage }}</span>
        </div>
        <p v-if="localError" class="error-text">{{ localError }}</p>
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
  background: linear-gradient(135deg, var(--app-accent-strong), var(--app-accent));
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

.profile-actions {
  display: flex;
  align-items: center;
  gap: 12px;
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

.update-btn:disabled {
  opacity: 0.7;
  cursor: wait;
}

.status-ok {
  color: var(--app-accent-strong);
  font-weight: 600;
}

.error-text {
  color: var(--app-danger);
  margin: 0;
}

@media (max-width: 600px) {
  .profile-content { flex-direction: column; text-align: center; }
  .profile-actions { flex-direction: column; }
  .update-btn { align-self: stretch; }
}
</style>
