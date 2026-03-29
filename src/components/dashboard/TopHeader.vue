<script setup>
import { ref } from 'vue';

const isTotalView = ref(false);
const isDarkMode = ref(false); // Default to light mode

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value;
  // Apply the class to the body so the whole app can respond to the theme
  document.body.classList.toggle('dark-theme', isDarkMode.value);
};
</script>

<template>
  <header class="top-header">
    <div class="logo">
      <h1>SubTrack</h1>
    </div>  

    <div class="header-controls">
      <div class="theme-slider" @click="toggleTheme" :class="{ 'is-dark': isDarkMode }">
        <div class="slider-segment">
          <i class="fa-solid fa-sun"></i>
        </div>
        <div class="slider-segment">
          <i class="fa-solid fa-moon"></i>
        </div>
        <div class="slider-knob"></div>
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
  height: 80px;
  box-sizing: border-box;
}

.top-header h1 {
  font-family: 'Montserrat', sans-serif;
  color: #004d26;
  font-weight: 800;
}

.logo h1 {
  margin: 0;
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

.theme-slider {
  position: relative;
  display: flex;
  width: 64px;   /* Specific width */
  height: 32px;  /* Specific height */
  background-color: #f1f1f1;
  border-radius: 16px;
  cursor: pointer;
  padding: 4px;
  transition: background-color 0.3s ease;
}

/* Fix: Ensure segments sit side-by-side */
.slider-segment {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
  color: #999;
  font-size: 0.8rem;
}

.slider-knob {
  position: absolute;
  top: 4px;
  left: 4px;
  width: 24px; /* Size of the knob */
  height: 24px;
  background-color: white;
  border-radius: 50%;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  z-index: 2;
}

.is-dark .slider-knob {
  transform: translateX(32px);
}

.is-dark { 
  transition: 0.3s ease;
  background-color: #333; 
}

.is-dark .slider-segment { 
  color: #f1f1f1; 
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