// MOCK DATABASE

// src/composables/useSubscriptions.js
import { ref } from 'vue';

// Declared OUTSIDE the function so the state is shared across all components
const subscriptions = ref([
  // Initial dummy data so your StatGrid isn't empty immediately
  { id: 1, name: 'Netflix', category: 'Entertainment', amount: 1500, cycle: 'monthly', dueDate: '2026-04-02', notifyDays: 3 },
  { id: 2, name: 'Spotify', category: 'Music', amount: 2500, cycle: 'monthly', dueDate: '2026-04-05', notifyDays: 1 },
]);

export function useSubscriptions() {
  const addSubscription = (sub) => {
    subscriptions.value.push({ ...sub, id: Date.now() }); // Generates a unique ID
  };

  const updateSubscription = (id, updatedSub) => {
    const index = subscriptions.value.findIndex(s => s.id === id);
    if (index !== -1) subscriptions.value[index] = { ...updatedSub, id };
  };

  const deleteSubscription = (id) => {
    subscriptions.value = subscriptions.value.filter(s => s.id !== id);
  };

  return {
    subscriptions,
    addSubscription,
    updateSubscription,
    deleteSubscription
  };
}