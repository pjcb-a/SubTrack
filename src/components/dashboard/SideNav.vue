<!-- Side Navigation Bar -->

<script setup>
import { ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const currentRoute = computed(() => route.name);

const handleLogout = () => {
  // Placeholder for logout logic
  alert('Logging out...');
  router.push('/'); // Redirect to login page after logout
};

const navLinks = ref([
  { id: 'dashboard', name: 'Dashboard', path: '/dashboard', iconClass: 'fa-solid fa-house' },
  { id: 'history',   name: 'History',   path: '/dashboard/history', iconClass: 'fa-solid fa-clock-rotate-left' },
  { id: 'settings',  name: 'Settings',  path: '/dashboard/settings', iconClass: 'fa-solid fa-gear' },
  { id: 'about',     name: 'About Us',  path: '/dashboard/about', iconClass: 'fa-solid fa-circle-info' },
]);
</script>

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

    <div class="logout-wrapper">
      <button class="logout-btn" @click="handleLogout">
        <i class="fa-solid fa-right-from-bracket"></i>
      </button>
    </div> 
  </nav>
</template>

<style scoped>
.sidebar {
  background-color: #004d26;
  width: 240px;
  height: 100vh; /* Lock to screen height */
  display: flex;
  flex-direction: column; /* Stack items vertically */
  align-items: center;
  padding: 40px 15px;
  box-sizing: border-box;
  position: fixed; /* Keep it from moving */
  left: 0;
  top: 0;
}

/* User Profile Styling */
.user-profile {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.nav-links {
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 100%;
  flex-grow: 1;
  margin-top: 40px;
}
.logout-wrapper {
  margin-top: auto; /* Safety fallback to ensure bottom alignment */
  padding-top: 20px;
  width: 100%;
  display: flex;
  justify-content: center;
  flex-shrink: 0; /* Keeps the button from getting squashed */
}
.profile-icon {
  width: 50px;
  height: 50px;
  background-color: white; /* Make it visible */
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #004d26;
  font-size: 1.5rem;
}

.icon-circle i {
  font-size: 1.2rem;
  color: #004d26; /* Dark green icon inside white circle */
}

.profile-icon i {
  font-size: 2rem;
  color: #666;
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
.nav-item.active .icon-circle { 
  background-color: white; 
}

.link-text {
  font-family: 'Montserrat', sans-serif;
  font-weight: 600;
  font-size: 0.9rem;
}

.logout-btn i {
  font-size: 1.5rem;
  color: white;
}
.logout-btn:hover i {
  color: #e25151; 
}
/* Logout Button */
.logout-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  width: 50px;
  height: 50px;
  border-radius: 12px;
  cursor: pointer;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.logout-btn:hover {
  transform: scale(1.1);
  background-color: rgba(255, 255, 255, 0.1);
}
</style>