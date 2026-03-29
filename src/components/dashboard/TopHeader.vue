<script setup>
import { onMounted, ref } from 'vue';

const props = defineProps({
  sidebarCollapsed: {
    type: Boolean,
    default: true,
  },
  showSidebarToggle: {
    type: Boolean,
    default: false,
  },
});

defineEmits(['toggle-sidebar']);

const DARK_MODE_STORAGE_KEY = 'subtrack-dark-mode';
const isDarkMode = ref(false);

const applyTheme = (value) => {
  document.body.classList.toggle('dark-theme', value);
  window.localStorage.setItem(DARK_MODE_STORAGE_KEY, String(value));
};

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value;
  applyTheme(isDarkMode.value);
};

onMounted(() => {
  isDarkMode.value = window.localStorage.getItem(DARK_MODE_STORAGE_KEY) === 'true';
  applyTheme(isDarkMode.value);
});
</script>

<template>
  <header class="top-header">
    <div class="header-brand">
      <button
        v-if="props.showSidebarToggle"
        class="action-icon nav-toggle"
        type="button"
        :aria-label="props.sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
        @click="$emit('toggle-sidebar')"
      >
        <i class="fa-solid fa-bars"></i>
      </button>

      <div class="logo">
        <h1>SubTrack</h1>
      </div>
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
        <button class="action-icon" type="button">
          <i class="fa-solid fa-bell"></i>
        </button>
        <button class="action-icon" type="button">
          <i class="fa-solid fa-circle-question"></i>
        </button>
      </div>
    </div>
  </header>
</template>

<style scoped>
.top-header {
  background: color-mix(in srgb, var(--app-surface) 94%, transparent);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 30px;
  border-bottom: 1px solid var(--app-border);
  width: 100%;
  height: 80px;
  box-sizing: border-box;
  backdrop-filter: blur(18px);
}

.header-brand {
  display: flex;
  align-items: center;
  gap: 16px;
}

.top-header h1 {
  font-family: 'Montserrat', sans-serif;
  color: var(--app-heading);
  font-weight: 800;
}

.logo h1 {
  margin: 0;
  font-family: 'Montserrat', sans-serif;
  color: var(--app-heading);
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
  width: 64px;
  height: 32px;
  background-color: var(--app-surface-alt);
  border-radius: 16px;
  cursor: pointer;
  padding: 4px;
  transition: background-color 0.3s ease;
}

.slider-segment {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
  color: var(--app-text-muted);
  font-size: 0.8rem;
}

.slider-knob {
  position: absolute;
  top: 4px;
  left: 4px;
  width: 24px;
  height: 24px;
  background-color: var(--app-surface);
  border-radius: 50%;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 2;
}

.is-dark .slider-knob {
  transform: translateX(32px);
}

.is-dark {
  transition: 0.3s ease;
  background-color: var(--app-surface-soft);
}

.is-dark .slider-segment {
  color: var(--app-heading);
}

.action-circles {
  display: flex;
  gap: 10px;
}

.action-icon {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  border: none;
  background-color: var(--app-surface-alt);
  color: var(--app-text);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.nav-toggle {
  background-color: var(--app-surface-alt);
  color: var(--app-heading);
  border: 1px solid var(--app-border);
}

.action-icon:hover {
  background-color: var(--app-surface-soft);
}

.action-icon i {
  font-size: 1rem;
}

@media (max-width: 959px) {
  .top-header {
    padding: 18px 16px;
  }

  .header-controls {
    gap: 12px;
  }

  .action-circles {
    gap: 8px;
  }

  .action-icon {
    width: 42px;
    height: 42px;
  }
}
</style>
