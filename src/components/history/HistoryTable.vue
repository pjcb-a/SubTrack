<script setup>
import { formatCurrency } from '../utils/subscriptionDates';

defineProps({
  records: Array
});
</script>

<template>
  <div class="table-container">
    <table class="custom-table">
      <thead>
        <tr>
          <th>Service</th>
          <th>Category</th>
          <th>Cycle</th>
          <th>Amount</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="record in records" :key="record.id">
          <td class="service-cell">
            <span class="avatar">{{ record.name.charAt(0) }}</span>
            {{ record.name }}
          </td>
          <td><span class="category-badge">{{ record.category }}</span></td>
          <td class="cycle-text">{{ record.cycle }}</td>
          <td class="amount-text">{{ formatCurrency(record.amount) }}</td>
          <td><span class="status-pill active">Active</span></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.table-container {
    font-family: 'Montserrat', sans-serif;
  background: var(--app-surface);
  border-radius: 20px;
  border: 1px solid var(--app-border);
  box-shadow: var(--app-shadow-soft);
  overflow: hidden;
}

.custom-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

th {
  background: var(--app-surface-alt);
  padding: 16px 20px;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--app-text-muted);
  font-weight: 700;
}

td {
  padding: 16px 20px;
  border-bottom: 1px solid var(--app-border);
  color: var(--app-text);
  font-size: 0.95rem;
}

.service-cell {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 700;
}

.avatar {
  width: 32px;
  height: 32px;
  background: var(--app-accent-soft);
  color: var(--app-accent);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
}

.category-badge {
  background: var(--app-surface-soft);
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
}

.amount-text {
  font-weight: 700;
  color: var(--app-accent);
}

.status-pill {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
}

.status-pill.active {
  background: #e7f5ee;
  color: #00a859;
}

body.dark-theme .status-pill.active {
  background: rgba(0, 168, 89, 0.2);
}
</style>