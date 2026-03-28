<script setup>
import ControlBar from './components/dashboard/ControlBar.vue';
import SideNav from './components/dashboard/SideNav.vue';
import StatGrid from './components/dashboard/StatGrid.vue';
import TopHeader from './components/dashboard/TopHeader.vue';
import CalendarView from './components/dashboard/CalendarView.vue';
</script>

<template>
  <div class="dashboard-layout">
    <div class="sidebar-wrapper">
      <SideNav />
    </div>

    <div class="main-wrapper">
      <TopHeader />

      <main class="content-body">
        <ControlBar />

        <div class="data-container">
          <StatGrid />
          <CalendarView />
        </div>
      </main>
    </div>
    
  </div>
</template>

<style scoped>
.dashboard-layout {
  display: flex;
  width: 100vw;
  height: 100vh;
  margin: 0;
  padding: 0;
  background-color: #f8f8f8;
  overflow: hidden;
}


.sidebar-wrapper {
  /* Hard-locks the sidebar to 240px so it cannot smush */
  flex: 0 0 240px; 
  width: 240px;
  min-width: 240px;
  height: 100vh;
  z-index: 100;
}

.main-wrapper {
  flex: 1; 
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow-x: auto;
  overflow-y: auto; /* Only this part scrolls */
  background-color: #f8f8f8;
  min-width: 800px; /* Prevents content from pushing the width out */
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
}

.data-container > :first-child {
  flex: 1;
  min-width: 300px;
}

.data-container > :last-child {
  flex: 2.5;
  min-width: 500px;
}
</style>
