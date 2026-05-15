<script setup>
import { computed, ref, watch } from 'vue';
import { useUserSettings } from '../../composables/useUserSettings';

const { settings, capStatus, settingsSaving, updateSettings } = useUserSettings();
const mode = ref('none');
const capAmount = ref('');
const overagePercent = ref('');
const localError = ref('');
const statusMessage = ref('');

watch(
  settings,
  (nextSettings) => {
    mode.value = nextSettings?.spending_cap_mode ?? 'none';
    capAmount.value = nextSettings?.spending_cap_amount ?? '';
    overagePercent.value = nextSettings?.soft_cap_overage_percent ?? '';
  },
  { immediate: true },
);

const isSoft = computed(() => mode.value === 'soft');
const isDisabled = computed(() => mode.value === 'none');

const savePreferences = async () => {
  localError.value = '';
  statusMessage.value = '';

  try {
    await updateSettings({
      spending_cap_mode: mode.value,
      spending_cap_amount: isDisabled.value ? null : capAmount.value,
      soft_cap_overage_percent: isSoft.value ? overagePercent.value : null,
    });
    statusMessage.value = 'Constraint settings updated.';
  } catch (error) {
    localError.value = error.message;
  }
};
</script>

<template>
  <section class="settings-card">
    <div class="card-header">
      <h3><i class="fa-solid fa-credit-card"></i> Subscription Constraint</h3>
    </div>

    <div class="constraint-grid">
      <label class="field-group">
        <span>Constraint Mode</span>
        <select v-model="mode" class="settings-input">
          <option value="none">Off</option>
          <option value="soft">Soft Cap</option>
          <option value="hard">Hard Cap</option>
        </select>
      </label>

      <label class="field-group">
        <span>Monthly Cap Amount</span>
        <input v-model="capAmount" class="settings-input" :disabled="isDisabled" type="number" min="0" step="0.01" placeholder="10000">
      </label>

      <label class="field-group">
        <span>Soft Cap Overage %</span>
        <input v-model="overagePercent" class="settings-input" :disabled="!isSoft" type="number" min="0" step="0.01" placeholder="10">
      </label>
    </div>

    <div class="preference-footer">
      <button class="settings-btn-secondary" :disabled="settingsSaving" @click="savePreferences">
        {{ settingsSaving ? 'Saving...' : 'Save Constraint Settings' }}
      </button>
      <span v-if="statusMessage" class="status-ok">{{ statusMessage }}</span>
    </div>

    <p v-if="localError" class="error-text">{{ localError }}</p>

    <div v-if="capStatus?.enabled" class="cap-status">
      <p><strong>Current Monthly Total:</strong> ₱{{ Number(capStatus.current_monthly_total || 0).toFixed(2) }}</p>
      <p><strong>Cap:</strong> ₱{{ Number(capStatus.cap_amount || 0).toFixed(2) }}</p>
      <p v-if="capStatus.mode === 'soft'"><strong>Soft Limit:</strong> ₱{{ Number(capStatus.soft_cap_limit || 0).toFixed(2) }}</p>
      <p v-if="capStatus.warning_message" class="warning-text">{{ capStatus.warning_message }}</p>
    </div>
  </section>
</template>

<style scoped>
.constraint-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 15px;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-weight: 600;
  color: var(--app-text);
}

.settings-input {
  background: var(--app-surface-alt);
  border: 1px solid var(--app-border);
  padding: 12px;
  border-radius: 12px;
  color: var(--app-text);
}

.preference-footer {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 18px;
}

.settings-btn-secondary {
  background-color: var(--app-surface-alt);
  border: 2px solid var(--app-border);
  color: var(--app-text);
  padding: 10px 20px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
}

.status-ok {
  color: var(--app-accent-strong);
  font-weight: 600;
}

.error-text {
  color: var(--app-danger);
  margin: 12px 0 0;
}

.cap-status {
  margin-top: 18px;
  padding: 16px;
  border-radius: 14px;
  background: var(--app-surface-alt);
  border: 1px solid var(--app-border);
}

.cap-status p {
  margin: 0 0 6px;
}

.warning-text {
  color: #ab6a00;
  font-weight: 600;
}

@media (max-width: 900px) {
  .constraint-grid {
    grid-template-columns: 1fr;
  }

  .preference-footer {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
