<script setup>
import { ref } from 'vue';
import { useSubscriptions } from '../../composables/useSubscriptions';
import {
  SUBSCRIPTION_CATEGORIES,
  getDefaultCategoryId,
} from '../../utils/subscriptionCategories';
import {
  buildRecurrenceFromForm,
  RECURRENCE_PRESET_OPTIONS,
  RECURRENCE_UNIT_OPTIONS,
} from '../../utils/subscriptionRecurrence';

const emit = defineEmits(['close', 'saved']);

const { addSubscription } = useSubscriptions();

const buildEmptySubscription = () => ({
  name: '',
  categoryId: getDefaultCategoryId(),
  amount: null,
  recurrencePreset: 'monthly',
  customRecurrenceUnit: 'day',
  customRecurrenceInterval: 2,
  anchorDate: '',
  notifyDays: 3,
});

const newSub = ref(buildEmptySubscription());
const submitError = ref('');

const submitAdd = async () => {
  submitError.value = '';

  if (!newSub.value.name || !newSub.value.amount || !newSub.value.anchorDate) {
    submitError.value = 'Please fill in the required fields.';
    return;
  }

  const recurrence = buildRecurrenceFromForm(newSub.value);

  try {
    const result = await addSubscription({
      ...newSub.value,
      recurrenceUnit: recurrence.recurrenceUnit,
      recurrenceInterval: recurrence.recurrenceInterval,
    });

    if (result.capWarning) {
      emit('saved', { tone: 'warning', message: result.capWarning.message });
    }
  } catch (error) {
    submitError.value = error.message;
    return;
  }

  newSub.value = buildEmptySubscription();
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
        <label>Category</label>
        <select v-model="newSub.categoryId">
          <option
            v-for="category in SUBSCRIPTION_CATEGORIES"
            :key="category.id"
            :value="category.id"
          >
            {{ category.name }}
          </option>
        </select>
      </div>

      <div class="input-group">
        <label>Amount </label>
        <input v-model="newSub.amount" type="number" step="0.01" placeholder="1000" />
      </div>

      <div class="input-group">
        <label>Schedule</label>
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

      <div v-if="newSub.recurrencePreset === 'custom'" class="custom-grid">
        <div class="input-group">
          <label>Every</label>
          <input v-model="newSub.customRecurrenceInterval" type="number" min="1" step="1" />
        </div>

        <div class="input-group">
          <label>Unit</label>
          <select v-model="newSub.customRecurrenceUnit">
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
        <label>Anchor Date</label>
        <input v-model="newSub.anchorDate" type="date" />
      </div>

      <p v-if="submitError" class="form-error">{{ submitError }}</p>

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
  top: 0; left: 0; width: 100vw; height: 100vh;
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
  width: 400px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  box-shadow: var(--app-shadow);
  border: 1px solid var(--app-border);
}

.custom-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.input-group {
  display: flex;
  flex-direction: column;
  text-align: left;
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

.input-group input::placeholder {
  color: var(--app-text-muted);
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

.save-btn:hover { 
  background: var(--app-accent); 
}

.cancel-btn:hover { 
  background: var(--app-surface-alt); 
}
</style>
