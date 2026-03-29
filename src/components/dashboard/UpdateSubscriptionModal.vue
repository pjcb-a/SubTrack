<script setup>
import { ref, watch } from 'vue';
import { useSubscriptions } from '../../composables/useSubscriptions';

const emit = defineEmits(['close']);
const { subscriptions, updateSubscription } = useSubscriptions();

// State to track which subscription the user wants to edit
const selectedId = ref('');

// State to hold the form data
const editData = ref({
  name: '',
  category: '',
  amount: null,
  cycle: 'monthly',
  dueDate: '',
  notifyDays: 3
});
const submitError = ref('');

// Watch for changes: When the user selects a subscription from the dropdown,
// automatically fill the form fields with that subscription's current data.
watch(selectedId, (newId) => {
  if (newId) {
    const subToEdit = subscriptions.value.find(s => s.id === newId);
    if (subToEdit) {
      // Create a copy so we don't edit the live data until "Save" is clicked
      editData.value = { ...subToEdit };
    }
  } else {
    // Reset if they deselect
    editData.value = { name: '', category: '', amount: null, cycle: 'monthly', dueDate: '', notifyDays: 3 };
  }
});

const submitUpdate = async () => {
  submitError.value = '';

  if (!selectedId.value) {
    submitError.value = 'Please select a subscription to update.';
    return;
  }
  if (!editData.value.name || !editData.value.amount || !editData.value.dueDate) {
    submitError.value = 'Please fill in all required fields.';
    return;
  }
  
  try {
    await updateSubscription(selectedId.value, { ...editData.value });
  } catch (error) {
    submitError.value = error.message;
    return;
  }
  
  // Close the modal
  emit('close');
};
</script>

<template>
  <div class="modal-overlay" @click.self="emit('close')">
    <div class="modal-card">
      <h3>Update Subscription</h3>
      
      <div class="input-group highlight-group">
        <label>Select Subscription to Edit</label>
        <select v-model="selectedId" class="select-target">
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
          <label>Amount </label>
          <input v-model="editData.amount" type="number" step="0.01" />
        </div>

        <div class="input-group">
          <label>Cycle</label>
          <select v-model="editData.cycle">
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
            <option value="annual">Annual</option>
          </select>
        </div>

        <div class="input-group">
          <label>Due Date</label>
          <input v-model="editData.dueDate" type="date" />
        </div>
      </div>
      <div v-else class="empty-state">
        <p>Please select a subscription above to view its details.</p>
      </div>

      <p v-if="submitError" class="form-error">{{ submitError }}</p>

      <div class="modal-actions">
        <button class="cancel-btn" @click="emit('close')">Cancel</button>
        <button class="save-btn" @click="submitUpdate" :disabled="!selectedId">Update</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* These styles are identical to your AddModal for UI consistency */
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

.input-group {
  display: flex;
  flex-direction: column;
  text-align: left;
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

.save-btn { background: var(--app-accent-strong); color: white; padding: 10px 20px; border-radius: 8px; border: none; cursor: pointer; font-weight: 600; }
.cancel-btn { background: var(--app-surface-soft); color: var(--app-text); padding: 10px 20px; border-radius: 8px; border: 1px solid var(--app-border); cursor: pointer; font-weight: 600;}
.save-btn:hover:not(:disabled) { background: var(--app-accent); }
.cancel-btn:hover { background: var(--app-surface-alt); }
.save-btn:disabled { background: color-mix(in srgb, var(--app-accent-strong) 40%, var(--app-surface-soft)); cursor: not-allowed; }
</style>
