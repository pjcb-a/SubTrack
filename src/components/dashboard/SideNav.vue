<!-- Side Navigation Bar -->

<script setup>
import { computed, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuth } from '../../composables/useAuth';
import { useSubscriptions } from '../../composables/useSubscriptions';

defineProps({
  collapsed: {
    type: Boolean,
    default: false,
  },
});

const route = useRoute();
const router = useRouter();
const currentPath = computed(() => route.path);
const { currentUser, logout } = useAuth();
const { resetSubscriptionStore } = useSubscriptions();

const handleLogout = async () => {
  await logout();
  resetSubscriptionStore();
  router.push('/');
};

const navLinks = ref([
  { id: 'dashboard', name: 'Dashboard', path: '/dashboard', iconClass: 'fa-solid fa-house' },
  { id: 'history', name: 'History', path: '/dashboard/history', iconClass: 'fa-solid fa-clock-rotate-left' },
  { id: 'settings', name: 'Settings', path: '/dashboard/settings', iconClass: 'fa-solid fa-gear' },
  { id: 'about', name: 'About Us', path: '/dashboard/about', iconClass: 'fa-solid fa-circle-info' },
]);

const isActivePath = (path) => currentPath.value === path;
const isAvailablePath = (path) => ['/dashboard', '/dashboard/history'].includes(path);
</script>

<template>
  <nav class="sidebar" :class="{ collapsed }">
    <div class="user-profile nav-item">
      <div class="icon-circle profile-icon">
        <i class="fa-solid fa-user"></i>
      </div>
      <span class="link-text">{{ currentUser?.username || 'Guest User' }}</span>
    </div>

    <div class="nav-links">
      <component
        v-for="link in navLinks"
        :key="link.id"
        :is="isAvailablePath(link.path) ? 'router-link' : 'button'"
        :to="isAvailablePath(link.path) ? link.path : undefined"
        :type="isAvailablePath(link.path) ? undefined : 'button'"
        class="nav-item"
        :class="{ active: isActivePath(link.path), unavailable: !isAvailablePath(link.path) }"
      >
        <div class="icon-circle">
          <i :class="link.iconClass"></i>
        </div>
        <span class="link-text">{{ link.name }}</span>
      </component>
    </div>

    <div class="logout-wrapper">
      <button class="logout-btn nav-item" @click="handleLogout">
        <div class="icon-circle">
          <i class="fa-solid fa-right-from-bracket"></i>
        </div>
        <span class="link-text">Logout</span>
      </button>
    </div>
  </nav>
</template>

<style scoped>
.sidebar {
  background: var(--app-sidebar-bg);
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 40px 15px;
  box-sizing: border-box;
  border-radius: 0 18px 18px 0;
  transition: padding 0.28s ease, border-radius 0.28s ease;
}

.sidebar.collapsed {
  padding-inline: 12px;
}

.user-profile {
  margin-bottom: 20px;
}

.nav-links {
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 100%;
  flex-grow: 1;
  margin-top: 20px;
  margin-bottom: 0;
}

.logout-wrapper {
  margin-top: auto;
  width: 100%;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 15px;
  width: 100%;
  padding: 10px;
  border-radius: 12px;
  text-decoration: none;
  color: var(--app-sidebar-text);
  transition: all 0.2s ease;
  cursor: pointer;
  border: none;
  background: transparent;
  font-family: 'Montserrat', sans-serif;
}

.sidebar.collapsed .nav-item {
  justify-content: center;
  width: 56px;
  margin-inline: auto;
  padding: 8px 0;
  gap: 0;
}

.nav-item:hover,
.nav-item.active {
  background-color: var(--app-sidebar-hover);
  transform: translateX(2px);
}

.sidebar.collapsed .nav-item:hover,
.sidebar.collapsed .nav-item.active {
  transform: none;
}

.nav-item.unavailable {
  opacity: 0.65;
}

.icon-circle {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background-color: var(--app-icon-surface);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.icon-circle i {
  font-size: 1.1rem;
  color: var(--app-icon-text);
}

.link-text {
  font-weight: 600;
  font-size: 0.9rem;
  white-space: nowrap;
  overflow: hidden;
  opacity: 1;
  transform: translateX(0);
  transition: opacity 0.2s ease, width 0.2s ease, transform 0.2s ease;
}

.sidebar.collapsed .link-text {
  width: 0;
  opacity: 0;
  transform: translateX(-8px);
}

.sidebar.collapsed .user-profile,
.sidebar.collapsed .logout-btn {
  width: 56px;
  margin-inline: auto;
}

.logout-btn {
  text-align: left;
}

.logout-btn:hover i {
  color: var(--app-danger);
}

@media (max-width: 959px) {
  .sidebar {
    border-radius: 0 18px 18px 0;
    padding-inline: 15px;
  }

  .sidebar.collapsed .link-text {
    width: auto;
    opacity: 1;
    transform: none;
  }
}
</style>
