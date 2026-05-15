<script setup>
import { computed, ref, watch } from 'vue';
import { useAuth } from '../../composables/useAuth';
import { useUserSettings } from '../../composables/useUserSettings';

const { currentUser } = useAuth();
const { updateProfile, settingsSaving } = useUserSettings();
const username = ref('');
const localError = ref('');
const localMessage = ref('');

watch(
  currentUser,
  (user) => {
    username.value = user?.username ?? '';
  },
  { immediate: true },
);

const userInitials = computed(() => {
  const source = (currentUser.value?.username || 'Guest User').trim();
  return source
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase() || '')
    .join('');
});

const saveProfile = async () => {
  localError.value = '';
  localMessage.value = '';

  if (!username.value.trim()) {
    localError.value = 'Username is required.';
    return;
  }

  try {
    await updateProfile(username.value.trim());
    localMessage.value = 'Profile updated.';
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
        <div class="initials-circle"> {{ userInitials }} </div>
      </div>

      <div class="form-group">
        <label>Username</label>
        <input v-model="username" type="text" class="settings-input" />
        <p v-if="localError" class="feedback error">{{ localError }}</p>
        <p v-else-if="localMessage" class="feedback success">{{ localMessage }}</p>
        <button class="update-btn" :disabled="settingsSaving" @click="saveProfile">
          {{ settingsSaving ? 'Saving...' : 'Save Changes' }}
        </button>
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

.update-btn:disabled {
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
@media (max-width: 600px) {
  .profile-content { flex-direction: column; text-align: center; }
  .update-btn { align-self: stretch; }
}
</style>
