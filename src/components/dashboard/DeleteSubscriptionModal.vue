<script setup>
import { ref } from 'vue';
import { useSubscriptions } from '../../composables/useSubscriptions';

const emit = defineEmits(['close']);
const { subscriptions, deleteSubscription } = useSubscriptions();

const selectedId = ref(null);
const submitError = ref('');

const confirmDelete = async () => {
  submitError.value = '';

  if (!selectedId.value) {
    submitError.value = 'Please select a subscription to delete.';
    return;
  }

  const subToDelete = subscriptions.value.find((subscription) => (
    Number(subscription.id) === Number(selectedId.value)
  ));

  if (!subToDelete) {
    submitError.value = 'Selected subscription could not be found. Please reopen the dialog.';
    return;
  }
  
  // Standard confirmation for safety
  if (confirm(`Are you sure you want to delete ${subToDelete.name}?`)) {
    try {
      await deleteSubscription(selectedId.value);
    } catch (error) {
      submitError.value = error.message;
      return;
    }
    emit('close');
  }
};
</script>

<template>
  <div class="modal-overlay" @click.self="emit('close')">
    <div class="modal-card">
      <div class="modal-header">
        <i class="fa-solid fa-triangle-exclamation warning-icon"></i>
        <h3>Delete Subscription</h3>
      </div>
      
      <p class="modal-instruction">Choose the service you wish to remove from your tracker.</p>

      <div class="input-group">
        <label>Select Subscription</label>
        <select v-model.number="selectedId" class="delete-select">
          <option value="" disabled>-- Select a subscription --</option>
          <option v-for="sub in subscriptions" :key="sub.id" :value="sub.id">
            {{ sub.name }} (₱{{ sub.amount }})
          </option>
        </select>
      </div>

      <p v-if="submitError" class="form-error">{{ submitError }}</p>

      <div class="modal-actions">
        <button class="cancel-btn" @click="emit('close')">Cancel</button>
        <button 
          class="delete-confirm-btn" 
          @click="confirmDelete" 
          :disabled="!selectedId"
        >
          Remove Service
        </button>
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

.modal-header {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--app-danger);
}

.warning-icon {
  font-size: 1.5rem;
}

.modal-instruction {
  font-size: 0.9rem;
  color: var(--app-text-muted);
  line-height: 1.4;
}

.input-group {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.input-group label {
  font-weight: 600;
  font-size: 0.85rem;
  margin-bottom: 5px;
}

.delete-select {
  padding: 12px;
  border: 1px solid var(--app-border);
  border-radius: 8px;
  font-family: 'Montserrat', sans-serif;
  background-color: var(--app-surface-alt);
  color: var(--app-text);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 10px;
}

.form-error {
  color: #aa3333;
  font-size: 0.9rem;
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

.delete-confirm-btn {
  background: var(--app-danger);
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.2s;
}

.delete-confirm-btn:hover:not(:disabled) {
  background: var(--app-danger-strong);
}

.delete-confirm-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
