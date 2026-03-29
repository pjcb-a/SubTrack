<script setup>
import { computed } from 'vue';
import { useSubscriptions } from '../../composables/useSubscriptions';
import {
  differenceInDays,
  formatCurrency,
  formatMonthDay,
  parseDateString,
} from '../../utils/subscriptionDates';

const { subscriptions, currentFilter } = useSubscriptions();
const cycleLabels = {
  weekly: 'Weekly',
  monthly: 'Monthly',
  annual: 'Annual',
};

const filteredSubs = computed(() => {
  let list = [...subscriptions.value];

  if (currentFilter.value !== 'all') {
    list = list.filter((subscription) => subscription.cycle === currentFilter.value);
  }

  return list.sort((left, right) => {
    const leftDate = parseDateString(left.dueDate);
    const rightDate = parseDateString(right.dueDate);
    return leftDate - rightDate;
  });
});

const totalActive = computed(() => subscriptions.value.length);
const weeklyCount = computed(() => subscriptions.value.filter((subscription) => subscription.cycle === 'weekly').length);
const monthlyCount = computed(() => subscriptions.value.filter((subscription) => subscription.cycle === 'monthly').length);
const annualCount = computed(() => subscriptions.value.filter((subscription) => subscription.cycle === 'annual').length);

const weeklyPercent = computed(() => totalActive.value === 0 ? 0 : (weeklyCount.value / totalActive.value) * 100);
const monthlyPercent = computed(() => totalActive.value === 0 ? 0 : (monthlyCount.value / totalActive.value) * 100);
const annualPercent = computed(() => totalActive.value === 0 ? 0 : (annualCount.value / totalActive.value) * 100);
const dueSoonCount = computed(() => filteredSubs.value.filter((sub) => {
  const diff = differenceInDays(sub.dueDate);
  return diff >= 0 && diff <= 7;
}).length);
const nextRenewal = computed(() => filteredSubs.value[0] ?? null);

const totalAnnualSpend = computed(() => {
  const total = subscriptions.value.reduce((acc, sub) => {
    const amount = Number(sub.amount) || 0;

    if (sub.cycle === 'weekly') {
      return acc + (amount * 52);
    }

    if (sub.cycle === 'monthly') {
      return acc + (amount * 12);
    }

    return acc + amount;
  }, 0);

  return formatCurrency(total);
});

const getCycleLabel = (cycle) => cycleLabels[cycle] ?? 'Custom';

const getDueLabel = (dueDate) => {
  const dayDifference = differenceInDays(dueDate);

  if (dayDifference < 0) {
    return `${Math.abs(dayDifference)} day${Math.abs(dayDifference) === 1 ? '' : 's'} overdue`;
  }

  if (dayDifference === 0) {
    return 'Due today';
  }

  if (dayDifference === 1) {
    return 'Due tomorrow';
  }

  return `Due in ${dayDifference} days`;
};
</script>

<template>
  <!-- BLOCK 1: Upcoming Payments -->
  <div class="stats-grid">
    <div id="upcoming-payments-card" class="stat-card upcoming-payments">
      <h3>Upcoming ({{ currentFilter === 'all' ? 'All' : currentFilter }})</h3>
      <p class="stat-meta">{{ dueSoonCount }} renewal{{ dueSoonCount === 1 ? '' : 's' }} in the next 7 days</p>

      <TransitionGroup name="subscription-list" tag="div" class="stat-content">
        <div v-for="sub in filteredSubs" :key="sub.id" class="sub-item">
          <div class="sub-icon">{{ sub.name ? sub.name[0].toUpperCase() : '?' }}</div>

          <div class="sub-details">
            <div class="sub-heading">
              <p class="sub-name">{{ sub.name }}</p>
              <span class="cycle-pill" :class="sub.cycle">{{ getCycleLabel(sub.cycle) }}</span>
            </div>
            <p class="sub-date">{{ getDueLabel(sub.dueDate) }} • {{ formatMonthDay(sub.dueDate) }}</p>
          </div>

          <p class="sub-price">{{ formatCurrency(sub.amount) }}</p>
        </div>
      </TransitionGroup>

      <p v-if="filteredSubs.length === 0" class="empty-card-state">No subscriptions match the current filter.</p>
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
          <span class="legend-value">{{ Math.round(weeklyPercent) }}%</span>
        </div>
        <div class="legend-item">
          <span class="dot monthly-dot"></span>
          <span class="legend-text">Monthly ({{ monthlyCount }})</span>
          <span class="legend-value">{{ Math.round(monthlyPercent) }}%</span>
        </div>
        <div class="legend-item">
          <span class="dot annual-dot"></span>
          <span class="legend-text">Annual ({{ annualCount }})</span>
          <span class="legend-value">{{ Math.round(annualPercent) }}%</span>
        </div>
      </div>
    </div>

  <!-- BLOCK 3: Total Spend -->
    <div class="stat-card total-spend">
      <h3>Total Annual Spend</h3>
      <p class="total-amount">{{ totalAnnualSpend }}</p>
      <p v-if="nextRenewal" class="comparison">
        Next renewal: {{ nextRenewal.name }} on {{ formatMonthDay(nextRenewal.dueDate) }}
      </p>
      <p v-else class="comparison">Add a subscription to populate your dashboard.</p>
    </div>
</div>
</template>

<style scoped>
.stats-grid {
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  width: 100%;
  gap: 20px;
}

.stat-card {
  font-family: 'Montserrat', sans-serif;
  flex: 1;
  min-width: 300px;
  background: color-mix(in srgb, var(--app-surface) 92%, transparent);
  border-radius: 20px;
  padding: 20px;
  box-shadow: var(--app-shadow);
  display: flex;
  flex-direction: column;
  border: 1px solid var(--app-border);
  backdrop-filter: blur(16px);
}

.stat-card h3 {
  font-family: 'Montserrat', sans-serif;
  color: var(--app-heading);
  font-size: 1.1rem;
  margin-bottom: 15px;
  border-bottom: 2px solid var(--app-border);
  padding-bottom: 5px;
}

.stat-meta {
  font-size: 0.82rem;
  color: var(--app-text-muted);
  margin-bottom: 12px;
}

.upcoming-payments {
  flex: 1.5;
}

.upcoming-payments .stat-content {
  max-height: 220px;
  overflow-y: auto;
  padding-right: 8px;
}

.upcoming-payments .stat-content::-webkit-scrollbar {
  width: 6px;
}

.upcoming-payments .stat-content::-webkit-scrollbar-track {
  background: var(--app-surface-alt);
  border-radius: 10px;
}

.upcoming-payments .stat-content::-webkit-scrollbar-thumb {
  background: var(--app-accent-strong);
  border-radius: 10px;
}

.upcoming-payments .stat-content::-webkit-scrollbar-thumb:hover {
  background: #00361a;
}

.subscription-list-move,
.subscription-list-enter-active,
.subscription-list-leave-active {
  transition: all 0.25s ease;
}

.subscription-list-enter-from,
.subscription-list-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

.sub-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 0;
  border-bottom: 1px solid var(--app-border);
}

.sub-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: var(--app-surface-soft);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  color: var(--app-text-muted);
}

.sub-details {
  flex: 1;
}

.sub-details,
.sub-name,
.sub-date,
.sub-price {
  font-family: 'Montserrat', sans-serif;
}

.sub-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.sub-name {
  font-weight: 700;
  color: var(--app-text);
}

.sub-date {
  font-size: 0.8rem;
  color: var(--app-text-muted);
}

.sub-price {
  font-weight: 700;
  color: var(--app-accent);
}

.cycle-pill {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 4px 8px;
  border-radius: 999px;
  background: var(--app-surface-soft);
  color: var(--app-heading);
}

.cycle-pill.weekly {
  background: rgba(0, 168, 89, 0.12);
  color: #008549;
}

.cycle-pill.monthly {
  background: var(--app-accent-soft);
}

.cycle-pill.annual {
  background: color-mix(in srgb, var(--app-text-muted) 18%, transparent);
  color: var(--app-text-muted);
}

.subs-list {
  flex: 1;
  text-align: center;
}

.stat-summary .count {
  font-family: 'Montserrat', sans-serif;
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--app-text);
  margin-top: 10px;
}

.stat-summary .label {
  font-size: 0.9rem;
  color: var(--app-text-muted);
}

.progress-container {
  display: flex;
  height: 8px;
  border-radius: 4px;
  overflow: hidden;
  background-color: var(--app-surface-soft);
  margin-top: 15px;
}

.progress-bar.weekly {
  background-color: #00a859;
  transition: width 0.3s ease;
}

.progress-bar.monthly {
  background-color: var(--app-accent-strong);
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
  justify-content: space-between;
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
  color: var(--app-text-muted);
  font-weight: 600;
  flex: 1;
}

.legend-value {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--app-accent);
}

.total-spend {
  flex: 1;
  background: var(--app-highlight-panel);
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.total-spend h3 {
  color: white;
  border-color: rgba(255, 255, 255, 0.1);
  width: 100%;
  text-align: center;
}

.total-amount {
  font-size: 2.8rem;
  font-weight: 800;
  text-align: center;
}

.comparison {
  font-size: 0.8rem;
  opacity: 0.78;
  margin-top: 10px;
  text-align: center;
}

.empty-card-state {
  font-size: 0.9rem;
  color: var(--app-text-muted);
  padding: 18px 0 6px;
}

@media (max-width: 959px) {
  .sub-item {
    align-items: flex-start;
  }

  .sub-heading {
    flex-direction: column;
    align-items: flex-start;
    gap: 6px;
  }

  .sub-price {
    min-width: fit-content;
  }
}
</style>
