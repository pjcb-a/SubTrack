<script setup>
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const currentRoute = computed(() => route.name);

const navLinks = ref([
  { id: 'dashboard', name: 'Dashboard', path: '/dashboard', iconClass: 'fa-solid fa-house' },
  { id: 'history',   name: 'History',   path: '/dashboard/history', iconClass: 'fa-solid fa-clock-rotate-left' },
  { id: 'settings',  name: 'Settings',  path: '/dashboard/settings', iconClass: 'fa-solid fa-gear' },
  { id: 'about',     name: 'About Us',  path: '/dashboard/about', iconClass: 'fa-solid fa-circle-info' },
]);
</script>

<!-- Left side nav bar -->

<template>
    <nav class="sidebar">
    <div class="user-profile">
      <div class="profile-icon">
        <i class="fa-solid fa-user"></i>
      </div>
    </div>

    <div class="nav-links">
      <router-link
        v-for="link in navLinks"
        :key="link.id"
        :to="link.path"
        class="nav-item"
        :class="{ active: currentRoute === link.id }"
      >
        <div class="icon-circle">
          <i :class="link.iconClass"></i>
        </div>
        <span class="link-text">{{ link.name }}</span>
      </router-link>
    </div>

    <button class="logout-btn" @click="handleLogout">
      <i class="fa-solid fa-right-from-bracket"></i>
    </button>
  </nav>
</template>

<style scoped>
.sidebar {
  grid-area: sidebar;
  background-color: #004d26; /* Wireframe Forest Green */
  color: white;
  display: flex;
  left: 0;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  padding: 30px 15px;
  min-height: 100vh;
}

/* User Profile Styling */
.user-profile {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
}
.icon-circle i {
  font-size: 1.2rem;
  color: #004d26; /* Dark green icon inside white circle */
}

.profile-icon i {
  font-size: 2rem;
  color: #666;
}

.logout-btn i {
  font-size: 1.5rem;
  color: white;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 10px;
  border-radius: 12px;
  text-decoration: none;
  color: white;
  transition: background-color 0.2s ease;
}
.nav-item:hover,
.nav-item.active {
  background-color: rgba(255, 255, 255, 0.1);
}

.icon-circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #f1f1f1;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s ease;
}
.nav-item.active .icon-circle { background-color: white; }
.icon-circle img { width: 25px; height: 25px; }

.link-text {
  font-family: 'Montserrat', sans-serif;
  font-weight: 600;
  font-size: 0.9rem;
}

/* Logout Button */
.logout-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 10px;
  border-radius: 10px;
  transition: transform 0.2s ease;
}
.logout-btn:hover {
  transform: scale(1.1);
  background-color: rgba(255, 255, 255, 0.1);
}
.logout-btn img { width: 30px; height: 30px; }
</style>