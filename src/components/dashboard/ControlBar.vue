<!-- Second row containing the logic for the CRUD buttons -->

<script setup>
import { ref } from 'vue';

const selectedCycle = ref('all');
</script>

<template>
  <div class="control-bar">
    <div class="crud-group">
      <button class="control-btn add-btn">
        <i class="fa solid fa-plus"></i>
        <span>Add</span>
      </button>

      <button class="control-btn update-btn">
        <i class="fa solid fa-edit"></i>
        <span>Update</span>
      </button>
      
      <button class="control-btn delete-btn">
        <i class="fa solid fa-trash"></i>
        <span>Delete</span>
      </button>
    </div>

    <div class="filter-group">
      <div class="select-wrapper">
        <select v-model="selectedCycle" class="payment-dropdown">
          <option value="all">Payment Cycle</option>
          <option value="monthly">Monthly</option>
          <option value="annual">Annual</option>
          <option value="weekly">Weekly</option>
        </select>
        <span class="dropdown-arrow">▼</span>
      </div>

      <button class="control-btn records-btn">
        <i class="fa-solid fa-bars"></i>
        <span>Records</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.control-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding: 0 10px;
}

.crud-group, .filter-group {
  display: flex;
  gap: 10px; /* Spacing between buttons */
  align-items: center;
}

/* Base button styling (The pill shapes from wireframe) */
.control-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  border: none;
  background-color: #f1f1f1;
  padding: 10px 20px;
  border-radius: 20px;
  cursor: pointer;
  font-family: 'Montserrat', sans-serif;
  font-weight: 700;
  color: #333;
  transition: all 0.2s ease;
}

.control-btn img { 
  width: 18px; 
  height: 18px; 
}

.control-btn:hover { 
  background-color: #e0e0e0; 
  transform: translateY(-1px); 
}

/* Customizing specific buttons */
.delete-btn { 
  background-color: #bcbcbc; 
  color: white; 
}

.delete-btn img { 
  filter: invert(1); 
} /* Make icon white */

.delete-btn:hover { 
  background-color: #aa3333; 
} /* Changes to danger red on hover */

.records-btn { 
  padding: 10px 25px; 
}

/* Custom Payment Dropdown */
.select-wrapper { 
  position: relative; 
}

.payment-dropdown {
  appearance: none; /* Hide default browser arrow */
  background-color: #f1f1f1;
  border: none;
  padding: 10px 35px 10px 20px;
  border-radius: 20px;
  font-family: 'Montserrat', sans-serif;
  font-weight: 700;
  cursor: pointer;
  color: #333;
}

.payment-dropdown:focus { 
  outline: none; 
  background-color: #e0e0e0; 
}

.dropdown-arrow {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.7rem;
  color: #666;
  pointer-events: none; /* Let clicks pass through to the select */
}

.delete-btn:hover i {
    color: #ff4d4d;
    transition: 0.3s ease;
}
</style>