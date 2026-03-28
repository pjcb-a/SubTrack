<script setup>
import { ref } from 'vue';
import { useSubscriptions } from '../../composables/useSubscriptions';

// This allows the modal to tell its parent (ControlBar) to close it
const emit = defineEmits(['close']);

const { addSubscription } = useSubscriptions();

// Local state for the form
const newSub = ref({
  name: '',
  category: '',
  amount: null,
  cycle: 'monthly',
  dueDate: '',
  notifyDays: 3
});

const submitAdd = () => {
  if (!newSub.value.name || !newSub.value.amount || !newSub.value.dueDate) {
    alert("Please fill in the required fields.");
    return;
  }
  
  // Send data to global state
  addSubscription({ ...newSub.value });
  
  // Reset form
  newSub.value = { name: '', category: '', amount: null, cycle: 'monthly', dueDate: '', notifyDays: 3 };
  
  // Tell parent to close the modal
  emit('close');
};
</script>

<template>
  <div class="modal-overlay" @click.self="emit('close')">
    <div class="modal-card">
      <h3>Add New Subscription</h3>
      
      <div class="input-group">
        <label>Name</label>
        <input v-model="newSub.name" type="text" placeholder="e.g. Netflix" />
      </div>

      <div class="input-group">
        <label>Amount </label>
        <input v-model="newSub.amount" type="number" step="0.01" placeholder="1000" />
      </div>

      <div class="input-group">
        <label>Cycle</label>
        <select v-model="newSub.cycle">
            <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
          <option value="annual">Annual</option>
        </select>
      </div>

      <div class="input-group">
        <label>Due Date</label>
        <input v-model="newSub.dueDate" type="date" />
      </div>

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

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 15px;
}

.save-btn { background: #004d26; color: white; padding: 10px 20px; border-radius: 8px; border: none; cursor: pointer; font-weight: 600; }
.cancel-btn { background: #bcbcbc; color: white; padding: 10px 20px; border-radius: 8px; border: none; cursor: pointer; font-weight: 600;}
.save-btn:hover { background: #00361a; }
.cancel-btn:hover { background: #a0a0a0; }
</style>