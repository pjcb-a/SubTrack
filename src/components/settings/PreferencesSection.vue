<script setup>
import { computed, ref, watch } from 'vue';
import { useUserSettings } from '../../composables/useUserSettings';

const { settings, capStatus, updateSettings, settingsSaving } = useUserSettings();
const spendingCapMode = ref('none');
const spendingCapAmount = ref('');
const softCapOveragePercent = ref('');
const localError = ref('');
const localMessage = ref('');

watch(
  settings,
  (nextSettings) => {
    spendingCapMode.value = nextSettings?.spending_cap_mode ?? 'none';
    spendingCapAmount.value = nextSettings?.spending_cap_amount ?? '';
    softCapOveragePercent.value = nextSettings?.soft_cap_overage_percent ?? '';
  },
  { immediate: true },
);

const capSummary = computed(() => {
  if (!capStatus.value?.enabled) {
    return 'Cap protection is currently turned off.';
  }

  if (capStatus.value.mode === 'soft') {
    return `Current monthly total: ₱${capStatus.value.current_monthly_total.toFixed(2)}. Soft limit: ₱${capStatus.value.soft_cap_limit.toFixed(2)}.`;
  }

  return `Current monthly total: ₱${capStatus.value.current_monthly_total.toFixed(2)}. Hard cap: ₱${capStatus.value.cap_amount.toFixed(2)}.`;
});

const savePreferences = async () => {
  localError.value = '';
  localMessage.value = '';

  try {
    await updateSettings({
      spending_cap_mode: spendingCapMode.value,
      spending_cap_amount: spendingCapAmount.value === '' ? 0 : Number(spendingCapAmount.value),
      soft_cap_overage_percent: spendingCapMode.value === 'soft'
        ? Number(softCapOveragePercent.value || 0)
        : 0,
    });
    localMessage.value = 'Spending cap settings updated.';
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

    <div class="preferences-form">
      <div class="input-group">
        <label>Cap Mode</label>
        <select v-model="spendingCapMode" class="settings-input">
          <option value="none">Off</option>
          <option value="soft">Soft Cap</option>
          <option value="hard">Hard Cap</option>
        </select>
      </div>

      <div class="input-group">
        <label>Monthly Cap Amount</label>
        <input v-model="spendingCapAmount" class="settings-input" type="number" min="0" step="0.01" />
      </div>

      <div v-if="spendingCapMode === 'soft'" class="input-group">
        <label>Soft Cap Overage Percent</label>
        <input v-model="softCapOveragePercent" class="settings-input" type="number" min="0" step="0.01" />
      </div>

      <p class="cap-summary">{{ capSummary }}</p>
      <p v-if="capStatus?.warning_message" class="feedback warning">{{ capStatus.warning_message }}</p>
      <p v-if="localError" class="feedback error">{{ localError }}</p>
      <p v-else-if="localMessage" class="feedback success">{{ localMessage }}</p>

      <button class="settings-btn-secondary" :disabled="settingsSaving" @click="savePreferences">
        {{ settingsSaving ? 'Saving...' : 'Save Cap Settings' }}
      </button>
    </div>
  </section>
</template>

<style scoped>
.preferences-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.input-group label {
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

.settings-btn-secondary {
  background-color: var(--app-surface-alt);
  border: 2px solid var(--app-border);
  color: var(--app-text); 
  padding: 10px 20px; 
  border-radius: 12px;
  font-weight: 600; 
  cursor: pointer; 
  transition: 0.2s;
}

.settings-btn-secondary:hover {
  background-color: var(--app-accent-strong);
  color: #f5f5f5;
  border-color: transparent;
  transform: translateY(-1px);
}

.settings-btn-secondary:disabled {
  opacity: 0.7;
  cursor: wait;
}

.cap-summary {
  font-size: 0.82rem;
  color: var(--app-text-muted);
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

.feedback.warning {
  color: var(--app-accent-strong);
}
</style>
