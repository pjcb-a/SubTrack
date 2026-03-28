<script setup>
import { ref } from 'vue';

// State for the pill toggle
const isTotalView = ref(false);
</script>

<template>
  <header class="top-header">
    <div class="logo">
      <h1>SubTrack</h1>
    </div>

    <div class="header-controls">
      <div class="toggle-pill" :class="{ 'toggle-active': isTotalView }">
        <button @click="isTotalView = false" class="toggle-segment">Monthly</button>
        <button @click="isTotalView = true" class="toggle-segment">Total</button>
      </div>

      <div class="action-circles">
        <button class="action-icon">
          <i class="fa solid fa-bell"></i>
        </button>
        <button class="action-icon">
          <i class="fa solid fa-question-circle"></i>
        </button>
      </div>
    </div>
  </header>
</template>

<style scoped>
.top-header {
  background-color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 30px;
  border-bottom: 1px solid #f1f1f1;
  width: 100%;
  box-sizing: border-box;
}

.logo h1 {
  font-family: 'Montserrat', sans-serif;
  color: #004d26;
  font-weight: 800;
  font-size: 1.5rem;
}

.header-controls {
  display: flex;
  align-items: center;
  gap: 20px;
}

/* Toggle Pill Styling */
.toggle-pill {
  position: relative;
  display: flex;
  background-color: #f1f1f1;
  border-radius: 25px;
  padding: 3px;
  width: 200px;
}

.toggle-segment {
  flex: 1;
  border: none;
  background: none;
  color: #666;
  font-weight: 600;
  padding: 10px;
  cursor: pointer;
  z-index: 1;
  transition: color 0.3s ease;
}

.toggle-segment:focus { outline: none; }

/* The sliding background for the active toggle */
.toggle-pill::after {
  content: '';
  position: absolute;
  top: 3px;
  left: 3px;
  width: calc(50% - 3px);
  height: calc(100% - 6px);
  background-color: white;
  border-radius: 22px;
  transition: transform 0.3s ease;
  z-index: 0;
}

.toggle-active .toggle-segment:first-child { 
    color: #ccc;
 }

.toggle-active .toggle-segment:last-child { 
    color: #004d26;
 }

.toggle-active::after {
    transform: translateX(100%); 
    }

/* Action Icons */
.action-circles {
  display: flex;
  gap: 10px;
}

.action-icon {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  border: none;
  background-color: #f1f1f1;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.action-icon:hover { 
    background-color: #e0e0e0; 
}

.action-icon img { 
    width: 22px; 
    height: 22px; 
}
</style>