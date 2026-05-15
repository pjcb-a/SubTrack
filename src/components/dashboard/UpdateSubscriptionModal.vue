<script setup>
import { ref, watch } from 'vue';
import { useSubscriptions } from '../../composables/useSubscriptions';
import {
  RECURRENCE_PRESET_OPTIONS,
  RECURRENCE_UNIT_OPTIONS,
  buildRecurrenceForm,
  buildRecurrenceFromForm,
} from '../../utils/subscriptionRecurrence';

const emit = defineEmits(['close']);
const { subscriptions, updateSubscription } = useSubscriptions();

const selectedId = ref(null);
const editData = ref({
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

watch(selectedId, (newId) => {
  if (!newId) {
    return;
  }

  const subToEdit = subscriptions.value.find((subscription) => subscription.id === newId);
  if (!subToEdit) {
    return;
  }

  const recurrenceForm = buildRecurrenceForm(subToEdit);
  editData.value = {
    ...subToEdit,
    recurrencePreset: recurrenceForm.preset,
    customInterval: recurrenceForm.customInterval,
    customUnit: recurrenceForm.customUnit,
    recurrenceEndMode: subToEdit.recurrenceEndMode || 'forever',
    recurrenceEndDate: subToEdit.recurrenceEndDate || '',
  };
});

const submitUpdate = async () => {
  submitError.value = '';
  submitWarning.value = '';

  if (!selectedId.value) {
    submitError.value = 'Please select a subscription to update.';
    return;
  }

  if (!editData.value.name || !editData.value.amount || !editData.value.dueDate) {
    submitError.value = 'Please fill in all required fields.';
    return;
  }

  if (
    editData.value.recurrenceEndMode === 'until'
    && !editData.value.recurrenceEndDate
  ) {
    submitError.value = 'Please choose when the recurrence should end.';
    return;
  }

  const recurrence = buildRecurrenceFromForm({
    preset: editData.value.recurrencePreset,
    customInterval: editData.value.customInterval,
    customUnit: editData.value.customUnit,
  });

  try {
    const result = await updateSubscription(Number(selectedId.value), {
      ...editData.value,
      cycle: editData.value.recurrencePreset,
      recurrenceUnit: recurrence.recurrenceUnit,
      recurrenceInterval: recurrence.recurrenceInterval,
      recurrenceEndDate: editData.value.recurrenceEndMode === 'until'
        ? editData.value.recurrenceEndDate
        : null,
    });

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
      <h3>Update Subscription</h3>

      <div class="input-group highlight-group">
        <label>Select Subscription to Edit</label>
        <select v-model.number="selectedId" class="select-target">
          <option value="" disabled>-- Choose a subscription --</option>
          <option v-for="sub in subscriptions" :key="sub.id" :value="sub.id">
            {{ sub.name }} ₱{{ sub.amount }}
          </option>
        </select>
      </div>

      <div v-if="selectedId" class="form-fields">
        <div class="input-group">
          <label>Name</label>
          <input v-model="editData.name" type="text" />
        </div>

        <div class="input-group">
          <label>Amount</label>
          <input v-model="editData.amount" type="number" step="0.01" />
        </div>

        <div class="input-group">
          <label>Starts On</label>
          <input v-model="editData.dueDate" type="date" />
        </div>

        <div class="input-group">
          <label>Recurrence</label>
          <select v-model="editData.recurrencePreset">
            <option
              v-for="option in RECURRENCE_PRESET_OPTIONS"
              :key="option.value"
              :value="option.value"
            >
              {{ option.label }}
            </option>
          </select>
        </div>

        <div v-if="editData.recurrencePreset === 'custom'" class="inline-grid">
          <div class="input-group">
            <label>Every</label>
            <input v-model="editData.customInterval" type="number" min="1" step="1" />
          </div>

          <div class="input-group">
            <label>Unit</label>
            <select v-model="editData.customUnit">
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
          <select v-model="editData.recurrenceEndMode">
            <option value="forever">Forever</option>
            <option value="until">Until a date</option>
          </select>
        </div>

        <div v-if="editData.recurrenceEndMode === 'until'" class="input-group">
          <label>End Date</label>
          <input v-model="editData.recurrenceEndDate" type="date" />
        </div>
      </div>

      <div v-else class="empty-state">
        <p>Please select a subscription above to view its details.</p>
      </div>

      <p v-if="submitError" class="form-error">{{ submitError }}</p>
      <p v-if="submitWarning" class="form-warning">{{ submitWarning }}</p>

      <div class="modal-actions">
        <button class="cancel-btn" @click="emit('close')">Cancel</button>
        <button class="save-btn" :disabled="!selectedId" @click="submitUpdate">Update</button>
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

.highlight-group {
  background-color: var(--app-surface-alt);
  padding: 15px;
  border-radius: 10px;
  border: 1px solid var(--app-border);
  margin-bottom: 10px;
}

.select-target {
  font-weight: 600;
  color: var(--app-heading);
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

.form-fields {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.empty-state {
  text-align: center;
  padding: 20px;
  color: var(--app-text-muted);
  font-style: italic;
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

.save-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
