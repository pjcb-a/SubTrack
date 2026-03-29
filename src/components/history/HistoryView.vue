<script setup>
import { useRouter } from 'vue-router';    
import { useSubscriptions } from '../../composables/useSubscriptions';

const router = useRouter();
const { deletedSubscriptions } = useSubscriptions();

const goBack = () => {
  router.push('/dashboard');
};

const clearHistory = () => {
  if (confirm('Are you sure you want to permanently clear all history records?')) {
    deletedSubscriptions.value = [];
  }
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
};
</script>

<template>
  <div class="history-container">
    <div class="history-actions">
        <button class="back-btn" @click="goBack">
            <i class="fa-solid fa-arrow-left"></i> Back to Dashboard
        </button>

        <button v-if="deletedSubscriptions.length > 0" class="clear-btn" @click="clearHistory">
            <i class="fa-solid fa-trash"></i> Clear History
        </button>
    </div>

    <header class="history-header">
      <h2><i class="fa-solid fa-clock-rotate-left"></i> Subscription History</h2>
      <p>Viewing deleted and archived subscriptions</p>
    </header>

    <div v-if="deletedSubscriptions.length === 0" class="empty-history">
      <i class="fa-solid fa-ghost"></i>
      <p>No history found. Delete a subscription to see it here!</p>
    </div>

    <div v-else class="history-list">
      <table class="history-table">
        <thead>
          <tr>
            <th>Service</th>
            <th>Category</th>
            <th>Amount</th>
            <th>Cycle</th>
            <th>Date Deleted</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sub in deletedSubscriptions" :key="sub.id">
            <td class="name-cell"><strong>{{ sub.name }}</strong></td>
            <td>{{ sub.category }}</td>
            <td>₱{{ sub.amount.toLocaleDateString() }}</td>
            <td><span class="cycle-badge">{{ sub.cycle }}</span></td>
            <td class="date-cell">{{ formatDate(sub.deletedAt) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.history-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.back-btn {
  background: var(--app-surface-soft);
  border: 1px solid var(--app-border);
  color: var(--app-text);
  padding: 8px 16px;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  transition: all 0.2s ease;
}

.back-btn:hover {
  background: var(--app-accent);
  color: white;
  border-color: var(--app-accent);
}

.clear-btn {
  background: transparent;
  border: 1px solid var(--app-danger);
  color: var(--app-danger);
  padding: 8px 16px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
}

.clear-btn:hover {
  background: var(--app-danger);
  color: white;
}

.return-btn {
  margin-top: 20px;
  padding: 10px 25px;
  background: var(--app-accent);
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 600;
}

.history-container {
    font-family: 'Montserrat', sans-serif;
  color: var(--app-text);
  animation: fadeIn 0.3s ease;
}

.history-header {
  margin-bottom: 30px;
}

.history-header h2 {
  color: var(--app-heading);
  display: flex;
  align-items: center;
  gap: 12px;
}

.empty-history {
  text-align: center;
  padding: 100px 20px;
  background: var(--app-surface-alt);
  border-radius: 20px;
  color: var(--app-text-muted);
}

.empty-history i { 
  font-size: 3rem; margin-bottom: 15px; display: block; 
}

.history-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--app-surface);
  border-radius: 15px;
  overflow: hidden;
  box-shadow: var(--app-shadow-soft);
}

.history-table th {
  text-align: left;
  padding: 15px;
  background: var(--app-surface-soft);
  color: var(--app-text-muted);
  font-size: 0.85rem;
  text-transform: uppercase;
}

.history-table td {
  padding: 15px;
  border-bottom: 1px solid var(--app-border);
}

.cycle-badge {
  background: var(--app-accent-soft);
  color: var(--app-accent);
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: capitalize;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>