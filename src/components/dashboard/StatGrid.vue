<script setup>
import { computed } from 'vue';
import { useSubscriptions } from '../../composables/useSubscriptions';

const { subscriptions } = useSubscriptions();

// 1. Sort subscriptions by nearest due date
const upcomingSubs = computed(() => {
  return [...subscriptions.value]
    .sort((a, b) => new Date(a.dueDate) - new Date(b.dueDate))
    .slice(0, 3);
});

// 2. Calculate dynamic stats
const totalActive = computed(() => subscriptions.value.length);
const monthlyCount = computed(() => subscriptions.value.filter(s => s.cycle === 'monthly').length);
const annualCount = computed(() => subscriptions.value.filter(s => s.cycle === 'annual').length);

// 3. Calculate Progress Bar Percentages dynamically
const monthlyPercentage = computed(() => totalActive.value === 0 ? 0 : (monthlyCount.value / totalActive.value) * 100);
const annualPercentage = computed(() => totalActive.value === 0 ? 0 : (annualCount.value / totalActive.value) * 100);

/// Calculate Total Annual Spend dynamically in Peso
const totalAnnualSpend = computed(() => {
  const total = subscriptions.value.reduce((acc, sub) => {
    const amount = Number(sub.amount) || 0;
    if (sub.cycle === 'monthly') return acc + (amount * 12);
    if (sub.cycle === 'weekly') return acc + (amount * 52);
    return acc + amount; // Annual
  }, 0);
  
  // Format with Philippine Locale
  return total.toLocaleString('en-PH', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
});
</script>

<template>
  <div class="stats-grid">
    <div class="stat-card upcoming-payments">
      <h3>Upcoming Payments</h3>

      <div class="stat-content">
        <p v-if="upcomingSubs.length === 0" style="color: #666; font-style: italic; padding: 10px 0;">No upcoming payments.</p>
        
        <div v-for="sub in upcomingSubs" :key="sub.id" class="sub-item">
          <div class="sub-icon">{{ sub.name.charAt(0).toUpperCase() }}</div>
          <div class="sub-details">
            <p class="sub-name">{{ sub.name }}</p>
            <p class="sub-date">Due: {{ sub.dueDate }}</p>
          </div>
          <p class="sub-price">₱{{ sub.amount }}</p>
        </div>
      </div>
    </div>

    <div class="stat-card subs-list">
      <h3>Your Active Subs</h3>
      <div class="stat-summary">
        <p class="count">{{ totalActive }}</p>
        <p class="label">Total Active</p>
      </div>
      <div class="progress-container">
        <div class="progress-bar monthly" :style="{ width: monthlyPercentage + '%' }"></div>
        <div class="progress-bar annual" :style="{ width: annualPercentage + '%' }"></div>
      </div>
      <p class="legend"><span>● Monthly</span> / <span>● Annual</span></p>
    </div>

    <div class="stat-card total-spend">
      <h3>Total Annual Spend</h3>
      <p class="total-amount">₱{{ totalAnnualSpend }}</p>
      <p class="comparison">Based on active subscriptions</p>
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

/* Base card styling */
.stat-card {
  font-family: 'Montserrat', sans-serif;
  flex: 1;
  min-width: 300px;
  background-color: white;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.stat-card h3 {
  font-family: 'Montserrat', sans-serif;
  color: #004d26;
  font-size: 1.1rem;
  margin-bottom: 15px;
  border-bottom: 2px solid #f1f1f1;
  padding-bottom: 5px;
}

/* Block 1: Upcoming Payments Mockup */
.upcoming-payments { 
    flex: 1.5; 
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

.progress-bar.monthly { 
    background-color: #004d26; 
}

.progress-bar.annual { 
    background-color: #bcbcbc; 
}

.legend { 
    font-size: 0.75rem; 
    color: #999; 
    margin-top: 5px; 
}

.legend span:first-child { 
    color: #004d26; 
}

.legend span:last-child { 
    color: #bcbcbc; 
}

/* Block 3: Total Spend Mockup */
.total-spend { 
    flex: 1; 
    background-color: #004d26; 
    color: white; 
    display: flex; flex-direction: 
    column; justify-content: center; 
    align-items: center;
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