<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue';
import ControlBar from './components/dashboard/ControlBar.vue';
import SideNav from './components/dashboard/SideNav.vue';
import StatGrid from './components/dashboard/StatGrid.vue';
import TopHeader from './components/dashboard/TopHeader.vue';
import CalendarView from './components/dashboard/CalendarView.vue';
import { useSubscriptions } from './composables/useSubscriptions';
import { useRouter } from 'vue-router';

const SIDEBAR_STORAGE_KEY = 'subtrack-sidebar-collapsed';
const SIDEBAR_EXPANDED_WIDTH = 240;
const SIDEBAR_COLLAPSED_WIDTH = 88;
const isSidebarCollapsed = ref(true);
const isMobileViewport = ref(false);
const router = useRouter();
const { fetchSubscriptions } = useSubscriptions();

const sidebarWidth = computed(() => {
  if (isMobileViewport.value) {
    return 0;
  }

  return isSidebarCollapsed.value ? SIDEBAR_COLLAPSED_WIDTH : SIDEBAR_EXPANDED_WIDTH;
});

const layoutStyle = computed(() => ({
  '--sidebar-width': `${sidebarWidth.value}px`,
}));

const syncSidebarState = () => {
  if (typeof window === 'undefined') {
    return;
  }

  isMobileViewport.value = window.innerWidth < 960;

  if (isMobileViewport.value) {
    isSidebarCollapsed.value = true;
    return;
  }

  const savedState = window.localStorage.getItem(SIDEBAR_STORAGE_KEY);
  isSidebarCollapsed.value = savedState === null ? true : savedState === 'true';
};

const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value;

  if (!isMobileViewport.value && typeof window !== 'undefined') {
    window.localStorage.setItem(SIDEBAR_STORAGE_KEY, String(isSidebarCollapsed.value));
  }
};

onMounted(() => {
  syncSidebarState();
  window.addEventListener('resize', syncSidebarState);
  fetchSubscriptions().catch(() => {
    router.push('/');
  });
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', syncSidebarState);
});
</script>

<template>
  <div
    class="dashboard-layout"
    :style="layoutStyle"
    :class="{
      'sidebar-collapsed': isSidebarCollapsed,
      'sidebar-mobile-open': isMobileViewport && !isSidebarCollapsed,
    }"
  >
    <button
      v-if="isMobileViewport && !isSidebarCollapsed"
      class="sidebar-backdrop"
      type="button"
      aria-label="Close sidebar"
      @click="toggleSidebar"
    ></button>

    <div class="sidebar-wrapper" :class="{ mobile: isMobileViewport }">
      <SideNav :collapsed="isSidebarCollapsed" />
    </div>

    <div class="main-wrapper">
      <TopHeader
        :show-sidebar-toggle="true"
        :sidebar-collapsed="isSidebarCollapsed"
        @toggle-sidebar="toggleSidebar"
      />

      <main class="content-body">
        <template v-if="router.currentRoute.value.path === '/dashboard'">
          <ControlBar />
          <div class="data-container">
            <StatGrid />
            <CalendarView />
          </div>
        </template>

        <template v-else>
          <router-view />
        </template>
      </main>
    </div>
  </div>
</template>

<style scoped>
.dashboard-layout {
  display: grid;
  grid-template-columns: var(--sidebar-width) minmax(0, 1fr);
  width: 100vw;
  height: 100vh;
  margin: 0;
  padding: 0;
  background: var(--app-bg);
  overflow: hidden;
  position: relative;
}

.sidebar-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(5, 17, 11, 0.22);
  border: none;
  z-index: 80;
}

.sidebar-wrapper {
  width: var(--sidebar-width);
  min-width: var(--sidebar-width);
  height: 100vh;
  z-index: 100;
  transition: width 0.28s ease, min-width 0.28s ease, transform 0.28s ease;
}

.main-wrapper {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow-x: hidden;
  overflow-y: auto;
  background: transparent;
  min-width: 0;
}

.content-body {
  padding: 30px;
  width: 100%;
  box-sizing: border-box;
}

.data-container {
  display: flex;
  gap: 30px;
  width: 100%;
  align-items: stretch;
}

.data-container > :first-child {
  flex: 1;
  min-width: 300px;
}

.data-container > :last-child {
  flex: 2.5;
  min-width: 500px;
}

@media (max-width: 959px) {
  .dashboard-layout {
    display: block;
  }

  .sidebar-wrapper {
    position: fixed;
    top: 0;
    left: 0;
    width: 240px;
    min-width: 240px;
    transform: translateX(-100%);
    box-shadow: 0 20px 45px rgba(0, 0, 0, 0.16);
  }

  .dashboard-layout.sidebar-mobile-open .sidebar-wrapper.mobile {
    transform: translateX(0);
  }

  .main-wrapper {
    width: 100%;
  }

  .content-body {
    padding: 20px 16px 24px;
  }

  .data-container {
    flex-direction: column;
    gap: 20px;
  }

  .data-container > :first-child,
  .data-container > :last-child {
    min-width: 0;
  }
}
</style>
