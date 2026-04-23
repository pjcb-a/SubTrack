<script setup>
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '../../composables/useAuth';
import { useUserSettings } from '../../composables/useUserSettings';

const router = useRouter();
const { currentUser } = useAuth();
const { changePassword, deleteAccount, settingsSaving } = useUserSettings();
const currentPassword = ref('');
const newPassword = ref('');
const passwordError = ref('');
const passwordMessage = ref('');
const deleteError = ref('');

const emailAddress = computed(() => currentUser.value?.email ?? 'No email');

const submitPasswordChange = async () => {
  passwordError.value = '';
  passwordMessage.value = '';

  if (!currentPassword.value || !newPassword.value) {
    passwordError.value = 'Current password and new password are required.';
    return;
  }

  try {
    await changePassword({
      current_password: currentPassword.value,
      new_password: newPassword.value,
    });
    currentPassword.value = '';
    newPassword.value = '';
    passwordMessage.value = 'Password updated.';
  } catch (error) {
    passwordError.value = error.message;
  }
};

const handleDeleteAccount = async () => {
  deleteError.value = '';

  if (!window.confirm('Delete your account and all saved subscription data?')) {
    return;
  }

  try {
    await deleteAccount();
    router.push('/');
  } catch (error) {
    deleteError.value = error.message;
  }
};
</script>

<template>
  <section class="settings-card">
    <div class="card-header">
      <h3><i class="fa-solid fa-shield-halved"></i> Account Security</h3>
    </div>
    
    <div class="section-content">
      <div class="input-group">
        <label>Email Address</label>
        <div class="input-with-icon">
          <input type="email" class="settings-input" :value="emailAddress" readonly />
          <i class="fa-solid fa-lock"></i>
        </div>
        <p class="input-help">Email cannot be changed directly for security.</p>
      </div>

      <div class="input-group">
        <label>Current Password</label>
        <input v-model="currentPassword" type="password" class="settings-input" />
      </div>

      <div class="input-group">
        <label>New Password</label>
        <input v-model="newPassword" type="password" class="settings-input" />
        <p v-if="passwordError" class="feedback error">{{ passwordError }}</p>
        <p v-else-if="passwordMessage" class="feedback success">{{ passwordMessage }}</p>
      </div>

      <div class="action-row">
        <button class="settings-btn-secondary" :disabled="settingsSaving" @click="submitPasswordChange">
          {{ settingsSaving ? 'Saving...' : 'Change Password' }}
        </button>
      </div>

      <div class="danger-zone">
        <div class="danger-info">
          <h4>Danger Zone</h4>
          <p>Permanently delete your account and all subscription data. This action is irreversible.</p>
          <p v-if="deleteError" class="feedback error">{{ deleteError }}</p>
        </div>
        <button class="settings-btn-danger" :disabled="settingsSaving" @click="handleDeleteAccount">
          Delete Account
        </button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.section-content { 
    display: flex; 
    flex-direction: column; 
    gap: 20px; 
}

.input-group {
  display: flex; 
  flex-direction: column; 
  gap: 4px;
}

.input-group label, .input-group p {
  margin-left: 5px;
}

.input-with-icon { 
    position: relative; 
}

.input-with-icon i {
  position: absolute; 
  right: 15px; 
  top: 50%;
  transform: translateY(-50%); 
  color: var(--app-text-muted); 
  font-size: 0.9rem;
}

.settings-input {
  background: var(--app-surface-alt);
  border: 1px solid var(--app-border);
  padding: 12px;
  border-radius: 12px;
  color: var(--app-text);
}

.input-help { 
    font-size: 0.75rem; 
    color: var(--app-text-muted); 
    margin-top: 5px; 
}

.settings-btn-secondary {
  background: var(--app-surface-soft); 
  border: 1px solid var(--app-border);
  color: var(--app-text); 
  padding: 10px 20px; 
  border-radius: 12px;
  font-weight: 600; 
  cursor: pointer; 
  transition: 0.2s;
}

.settings-btn-secondary:disabled,
.settings-btn-danger:disabled {
  opacity: 0.7;
  cursor: wait;
}

.danger-zone {
  margin-top: 20px; 
  padding-top: 20px; 
  border-top: 1px solid var(--app-border);
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  gap: 20px;
}

.danger-info h4 { 
    color: var(--app-danger); 
    margin-bottom: 4px; 
}

.danger-info p { 
    font-size: 0.85rem; 
    color: var(--app-text-muted); 
    max-width: 400px; 
}

.settings-btn-danger {
  background: transparent; 
  border: 1px solid var(--app-danger);
  color: var(--app-danger); 
  padding: 10px 20px; 
  border-radius: 12px;
  font-weight: 600; 
  cursor: pointer; 
  transition: 0.2s;
}

.settings-btn-danger:hover { 
    background: var(--app-danger); 
    color: white; 
}

.feedback {
  font-size: 0.8rem;
}

.feedback.error {
  color: var(--app-danger);
}

.feedback.success {
  color: var(--app-accent);
}

@media (max-width: 600px) {
  .danger-zone { 
    flex-direction: column; 
    align-items: flex-start; 
}

  .settings-btn-danger { 
    width: 100%; 
}
}
</style>
