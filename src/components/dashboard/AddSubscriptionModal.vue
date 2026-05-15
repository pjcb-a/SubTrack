<script setup>
import { ref } from 'vue';
import { useSubscriptions } from '../../composables/useSubscriptions';
import {
  RECURRENCE_PRESET_OPTIONS,
  RECURRENCE_UNIT_OPTIONS,
  buildRecurrenceFromForm,
} from '../../utils/subscriptionRecurrence';

const emit = defineEmits(['close']);
const { addSubscription } = useSubscriptions();

const newSub = ref({
  name: '',
  amount: null,
  cycle: 'monthly',
  dueDate: '',
  notifyDays: 3,
  recurrencePreset: 'monthly',
  customInterval: 2,
  customUnit: 'day',
  recurrenceEndMode: 'forever',
  recurrenceEndDate: '',
});
const submitError = ref('');
const submitWarning = ref('');

const submitAdd = async () => {
  submitError.value = '';
  submitWarning.value = '';

  if (!newSub.value.name || !newSub.value.amount || !newSub.value.dueDate) {
    submitError.value = 'Please fill in the required fields.';
    return;
  }

  if (
    newSub.value.recurrenceEndMode === 'until'
    && !newSub.value.recurrenceEndDate
  ) {
    submitError.value = 'Please choose when the recurrence should end.';
    return;
  }

  const recurrence = buildRecurrenceFromForm({
    preset: newSub.value.recurrencePreset,
    customInterval: newSub.value.customInterval,
    customUnit: newSub.value.customUnit,
  });

  const payload = {
    ...newSub.value,
    cycle: newSub.value.recurrencePreset === 'yearly' ? 'yearly' : newSub.value.recurrencePreset,
    recurrenceUnit: recurrence.recurrenceUnit,
    recurrenceInterval: recurrence.recurrenceInterval,
    recurrenceEndDate: newSub.value.recurrenceEndMode === 'until'
      ? newSub.value.recurrenceEndDate
      : null,
  };

  try {
    const result = await addSubscription(payload);
    if (result.capWarning?.warning_message) {
      submitWarning.value = result.capWarning.warning_message;
      return;
    }
  } catch (error) {
    submitError.value = error.message;
    return;
  }

  emit('close');
};
</script>

<template>
  <div class="modal-overlay" @click.self="emit('close')">
    <div class="modal-card">
      <h3>Add New Subscription</h3>

      <div class="input-group">
        <label>Name</label>
        <input v-model="newSub.name" type="text" placeholder="Subscription Name" />
      </div>

      <div class="input-group">
        <label>Amount</label>
        <input v-model="newSub.amount" type="number" step="0.01" placeholder="1000" />
      </div>

      <div class="input-group">
        <label>Starts On</label>
        <input v-model="newSub.dueDate" type="date" />
      </div>

      <div class="input-group">
        <label>Recurrence</label>
        <select v-model="newSub.recurrencePreset">
          <option
            v-for="option in RECURRENCE_PRESET_OPTIONS"
            :key="option.value"
            :value="option.value"
          >
            {{ option.label }}
          </option>
        </select>
      </div>

      <div v-if="newSub.recurrencePreset === 'custom'" class="inline-grid">
        <div class="input-group">
          <label>Every</label>
          <input v-model="newSub.customInterval" type="number" min="1" step="1" />
        </div>

        <div class="input-group">
          <label>Unit</label>
          <select v-model="newSub.customUnit">
            <option
              v-for="option in RECURRENCE_UNIT_OPTIONS"
              :key="option.value"
              :value="option.value"
            >
              {{ option.label }}
            </option>
          </select>
        </div>
      </div>

      <div class="input-group">
        <label>Repeat Until</label>
        <select v-model="newSub.recurrenceEndMode">
          <option value="forever">Forever</option>
          <option value="until">Until a date</option>
        </select>
      </div>

      <div v-if="newSub.recurrenceEndMode === 'until'" class="input-group">
        <label>End Date</label>
        <input v-model="newSub.recurrenceEndDate" type="date" />
      </div>

      <p v-if="submitError" class="form-error">{{ submitError }}</p>
      <p v-if="submitWarning" class="form-warning">{{ submitWarning }}</p>

      <div class="modal-actions">
        <button class="cancel-btn" @click="emit('close')">Cancel</button>
        <button class="save-btn" @click="submitAdd">Save</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  font-family: 'Montserrat', sans-serif;
  position: fixed;
  inset: 0;
  background: rgba(5, 10, 8, 0.56);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-card {
  background: var(--app-surface);
  color: var(--app-text);
  padding: 30px;
  border-radius: 15px;
  width: min(440px, calc(100vw - 32px));
  display: flex;
  flex-direction: column;
  gap: 15px;
  box-shadow: var(--app-shadow);
  border: 1px solid var(--app-border);
}

.input-group {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.inline-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.input-group label {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--app-text);
}

.input-group input, .input-group select {
  padding: 10px;
  border: 1px solid var(--app-border);
  border-radius: 8px;
  margin-top: 5px;
  font-family: inherit;
  background: var(--app-surface-alt);
  color: var(--app-text);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 15px;
}

.form-error {
  color: #aa3333;
  font-size: 0.9rem;
}

.form-warning {
  color: #ab6a00;
  font-size: 0.9rem;
}

.save-btn {
  background: var(--app-accent-strong);
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 600;
}

.cancel-btn {
  background: var(--app-surface-soft);
  color: var(--app-text);
  padding: 10px 20px;
  border-radius: 8px;
  border: 1px solid var(--app-border);
  cursor: pointer;
  font-weight: 600;
}
</style>
