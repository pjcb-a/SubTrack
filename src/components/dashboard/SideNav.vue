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
    <div class="user-profile nav-item">
      <div class="icon-circle profile-icon">
        <i class="fa-solid fa-user"></i>
      </div>
      <span class="link-text"> Nigga </span>
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
  background-color: #004d26;
  width: 240px;
  height: 100vh;
  display: flex;
  flex-direction: column; 
  padding: 40px 15px;
  box-sizing: border-box;
}

/* 1. Reset User Profile */
.user-profile {
  margin-bottom: 20px; 
}

/* 2. The Navigation Links "Spacer" */
.nav-links {
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 100%;
  flex-grow: 1; 
  margin-top: 20px;
  margin-bottom: 0; 
}

/* 3. The Logout Wrapper */
.logout-wrapper {
  margin-top: auto; 
  width: 100%;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1); /* Adds a nice divider */
}

/* 4. Unified Nav Item */
.nav-item {
  display: flex;
  align-items: center;
  gap: 15px;
  width: 100%;
  padding: 10px;
  border-radius: 12px;
  text-decoration: none;
  color: white;
  transition: all 0.2s ease;
  cursor: pointer;
  border: none; 
  background: transparent;
  font-family: 'Montserrat', sans-serif;
}

.nav-item:hover,
.nav-item.active {
  background-color: rgba(255, 255, 255, 0.1);
}

/* 5. Icon Circles (Ensuring they are identical) */
.icon-circle {
  width: 45px; 
  height: 45px;
  border-radius: 50%;
  background-color: white; 
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.icon-circle i {
  font-size: 1.1rem;
  color: #004d26;
}

.link-text {
  font-weight: 600;
  font-size: 0.9rem;
  white-space: nowrap;
}


.logout-btn {
  text-align: left; 
}

.logout-btn:hover i {
  color: #e25151; 
}
</style>