<script setup>
import { ref } from 'vue';
import { useSubscriptions } from '../../composables/useSubscriptions';

const emit = defineEmits(['close']);
const { subscriptions, deleteSubscription } = useSubscriptions();

const selectedId = ref('');

const confirmDelete = () => {
  if (!selectedId.value) {
    alert("Please select a subscription to delete.");
    return;
  }

  const subToDelete = subscriptions.value.find(s => s.id === selectedId.value);
  
  // Standard confirmation for safety
  if (confirm(`Are you sure you want to delete ${subToDelete.name}?`)) {
    deleteSubscription(selectedId.value);
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
        <select v-model="selectedId" class="delete-select">
          <option value="" disabled>-- Select a subscription --</option>
          <option v-for="sub in subscriptions" :key="sub.id" :value="sub.id">
            {{ sub.name }} (₱{{ sub.amount }})
          </option>
        </select>
      </div>

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

.modal-header {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #aa3333;
}

.warning-icon {
  font-size: 1.5rem;
}

.modal-instruction {
  font-size: 0.9rem;
  color: #666;
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
  border: 1px solid #ddd;
  border-radius: 8px;
  font-family: 'Montserrat', sans-serif;
  background-color: #f9f9f9;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 10px;
}

.cancel-btn {
  background: #bcbcbc;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 600;
}

.delete-confirm-btn {
  background: #aa3333;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.2s;
}

.delete-confirm-btn:hover:not(:disabled) {
  background: #882222;
}

.delete-confirm-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>