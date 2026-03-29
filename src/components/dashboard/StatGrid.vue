<script setup>
import { computed } from 'vue';
import { useSubscriptions } from '../../composables/useSubscriptions';

const { subscriptions, currentFilter } = useSubscriptions();

// 1. Sort subscriptions by nearest due date
// Filtered List for the "Upcoming Payments" column
const filteredSubs = computed(() => {
  let list = [...subscriptions.value];
  if (currentFilter.value !== 'all') {
    list = list.filter(s => s.cycle === currentFilter.value);
  }
  return list.sort((a, b) => new Date(a.dueDate) - new Date(b.dueDate));
});

const totalActive = computed(() => subscriptions.value.length);
const weeklyCount = computed(() => subscriptions.value.filter(s => s.cycle === 'weekly').length); // NEW
const monthlyCount = computed(() => subscriptions.value.filter(s => s.cycle === 'monthly').length);
const annualCount = computed(() => subscriptions.value.filter(s => s.cycle === 'annual').length);

const weeklyPercent = computed(() => totalActive.value === 0 ? 0 : (weeklyCount.value / totalActive.value) * 100);
const monthlyPercent = computed(() => totalActive.value === 0 ? 0 : (monthlyCount.value / totalActive.value) * 100);
const annualPercent = computed(() => totalActive.value === 0 ? 0 : (annualCount.value / totalActive.value) * 100);

const totalAnnualSpend = computed(() => {
  // 1. Filter the subscriptions based on the current dropdown selection
  let filteredList = [...subscriptions.value];
  if (currentFilter.value !== 'all') {
    filteredList = filteredList.filter(s => s.cycle === currentFilter.value);
  }

  // 2. Calculate total for the filtered list
  const total = filteredList.reduce((acc, sub) => {
    const amt = Number(sub.amount) || 0;
    // We still calculate the ANNUAL impact of these specific subs
    if (sub.cycle === 'weekly') return acc + (amt * 52);
    if (sub.cycle === 'monthly') return acc + (amt * 12);
    return acc + amt;
  }, 0);

  return total.toLocaleString('en-PH', { minimumFractionDigits: 2 });
});
</script>

<template>
  <!-- BLOCK 1: Upcoming Payments -->
  <div class="stats-grid">
    <div class="stat-card upcoming-payments">
      <h3>Upcoming ({{ currentFilter === 'all' ? 'All' : currentFilter }})</h3>
      <div class="stat-content">
        <div v-for="sub in filteredSubs" :key="sub.id" class="sub-item">
      <div class="sub-icon">{{ sub.name ? sub.name[0].toUpperCase() : '?' }}</div>

          <div class="progress-container">
                <div class="progress-bar weekly" :style="{ width: weeklyPercent + '%' }"></div>
                <div class="progress-bar monthly" :style="{ width: monthlyPercent + '%' }"></div>
                <div class="progress-bar annual" :style="{ width: annualPercent + '%' }"></div>
          </div>

          <div class="sub-details">
            <p class="sub-name">{{ sub.name }}</p>
            <p class="sub-date">Due: {{ sub.dueDate }}</p>
          </div>

          <p class="sub-price">₱{{ sub.amount }}</p>
        </div>
      </div>
    </div>

    <!-- BLOCK 2: Distribution -->
    <div class="stat-card subs-list">
        <h3>Distribution</h3>
        <div class="stat-summary">
          <p class="count">{{ totalActive }}</p>
          <p class="label">Active Subs</p>
        </div>
        
        <div class="progress-container">
          <div class="progress-bar weekly" :style="{ width: weeklyPercent + '%' }"></div>
          <div class="progress-bar monthly" :style="{ width: monthlyPercent + '%' }"></div>
          <div class="progress-bar annual" :style="{ width: annualPercent + '%' }"></div>
        </div>

          <div class="legend-grid">
            <div class="legend-item">
              <span class="dot weekly-dot"></span>
              <span class="legend-text">Weekly ({{ weeklyCount }})</span>
            </div>
            <div class="legend-item">
              <span class="dot monthly-dot"></span>
              <span class="legend-text">Monthly ({{ monthlyCount }})</span>
            </div>
            <div class="legend-item">
              <span class="dot annual-dot"></span>
              <span class="legend-text">Annual ({{ annualCount }})</span>
            </div>
          </div>
      </div>

  <!-- BLOCK 3: Total Spend -->
    <div class="stat-card total-spend">
      <h3>Total {{ currentFilter === 'all' ? 'All' : currentFilter[0].toUpperCase() + currentFilter.slice(1) }} Spend</h3>
      <p class="total-amount">₱{{ totalAnnualSpend }}</p>
      <p class="comparison">
    {{ currentFilter === 'all' ? 'Across all categories' : 'Filtered by ' + currentFilter }}
  </p>
    </div>
</div>
</template>

<style scoped>
.stats-grid {
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  width: 100%;
  gap: 20px; /* Spacing between the stacked blocks */
}

  /* BLOCK 1: Upcoming Payments */
.stat-card {
  font-family: 'Montserrat', sans-serif;
  flex: 1;
  min-width: 300px;
  background-color: white;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
  transition: background-color 0.3s ease, transform 0.3s ease;

}

.stat-card:hover {
  transform: scale(1.02);
}

.stat-card h3 {
  font-family: 'Montserrat', sans-serif;
  color: #004d26;
  font-size: 1.1rem;
  margin-bottom: 15px;
  border-bottom: 2px solid #f1f1f1;
  padding-bottom: 5px;
}

.upcoming-payments { 
    flex: 1.5; 
}

.upcoming-payments .stat-content {
  max-height: 150px; /* Adjust this height based on your preference */
  overflow-y: auto;
  padding-right: 8px; /* Space for the scrollbar */
}

/* Make the scrollbar look pretty (Webkit browsers like Chrome/Edge/Safari) */
.upcoming-payments .stat-content::-webkit-scrollbar {
  width: 6px;
}

.upcoming-payments .stat-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.upcoming-payments .stat-content::-webkit-scrollbar-thumb {
  background: #004d26; /* Matches your theme green */
  border-radius: 10px;
}

.upcoming-payments .stat-content::-webkit-scrollbar-thumb:hover {
  background: #00361a;
}

.sub-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 0;
  border-bottom: 1px solid #f1f1f1;
}

.sub-icon {
  width: 40px; 
  height: 40px; 
  border-radius: 8px; 
  background: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800; 
  color: #666;
}

.sub-details { 
    flex: 1; 
}

.sub-details, .sub-name, .sub-date, .sub-price {
    font-family: 'Montserrat', sans-serif;
}

.sub-name{ 
  font-family: 'Montserrat', sans-serif;
    font-weight: 700; 
    color: #333; 
}

.sub-date { 
    font-size: 0.8rem; 
    color: #999; 
}

.sub-price { 
    font-weight: 700; 
    color: #004d26; 
}

/* Block 2: Subs List Mockup */
.subs-list { 
    flex: 1; 
    text-align: center; 
    transition: background-color 0.3s ease, transform 0.3s ease;

}

.subs-list:hover {
    transform: scale(1.02);
}

.stat-summary .count { 
    font-family: 'Montserrat', sans-serif;
    font-size: 2.5rem; 
    font-weight: 800; 
    color: #333; 
    margin-top: 10px; 
}

.stat-summary .label { 
    font-size: 0.9rem;
    color: #666; 
    }

.progress-container {
  display: flex; 
  height: 8px; 
  border-radius: 4px; 
  overflow: hidden; 
  background-color: #f1f1f1; 
  margin-top: 15px;
}

.progress-bar.weekly { 
  background-color: #00a859; 
  transition: width 0.3s ease; 
}

.progress-bar.monthly { 
  background-color: #004d26; 
  transition: width 0.3s ease; 
}

.progress-bar.annual { 
  background-color: #bcbcbc; 
  transition: width 0.3s ease; 
}

.legend-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 8px;
  text-align: left;
  margin-top: 15px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
  margin-right: 8px;
}

.weekly-dot { 
  background-color: #00a859; 
}

.monthly-dot { 
  background-color: #004d26; 
}

.annual-dot { 
  background-color: #bcbcbc; 
}

.legend-text {
  font-size: 0.75rem;
  color: #666;
  font-weight: 600;
}

/* Block 3: Total Spend Mockup */
.total-spend { 
    flex: 1; 
    background-color: #004d26; 
    color: white; 
    display: flex; flex-direction: 
    column; justify-content: center; 
    align-items: center;
    transition: background-color 0.3s ease, transform 0.3s ease;
 }

 .total-spend:hover {
  transform: scale(1.02);
}

.total-spend h3 { 
    color: white; 
    border-color: rgba(255,255,255,0.1); 
    width: 100%; 
    text-align: center; 
}

.total-amount { 
    font-size: 2.8rem; 
    font-weight: 800; 
}

.comparison { 
    font-size: 0.8rem; 
    opacity: 0.7; 
}
</style>