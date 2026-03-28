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

const submitUpdate = () => {
  if (!selectedId.value) {
    alert("Please select a subscription to update.");
    return;
  }
  if (!editData.value.name || !editData.value.amount || !editData.value.dueDate) {
    alert("Please fill in all required fields.");
    return;
  }
  
  // Send the updated data to the global state
  updateSubscription(selectedId.value, { ...editData.value });
  
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
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-card {
  background: white;
  padding: 30px;
  border-radius: 15px;
  width: 400px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

.input-group {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.highlight-group {
  background-color: #f8f8f8;
  padding: 15px;
  border-radius: 10px;
  border: 1px solid #e0e0e0;
  margin-bottom: 10px;
}

.select-target {
  font-weight: 600;
  color: #004d26;
}

.input-group label {
  font-weight: 600;
  font-size: 0.9rem;
  color: #333;
}

.input-group input, .input-group select {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  margin-top: 5px;
  font-family: inherit;
}

.form-fields {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.empty-state {
  text-align: center;
  padding: 20px;
  color: #666;
  font-style: italic;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 15px;
}

.save-btn { background: #004d26; color: white; padding: 10px 20px; border-radius: 8px; border: none; cursor: pointer; font-weight: 600; }
.cancel-btn { background: #bcbcbc; color: white; padding: 10px 20px; border-radius: 8px; border: none; cursor: pointer; font-weight: 600;}
.save-btn:hover:not(:disabled) { background: #00361a; }
.cancel-btn:hover { background: #a0a0a0; }
.save-btn:disabled { background: #a3c4b3; cursor: not-allowed; }
</style>