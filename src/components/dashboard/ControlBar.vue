<!-- Second row containing the logic for the CRUD buttons -->

<script setup>
import { computed, ref } from 'vue';
import AddSubscriptionModal from './AddSubscriptionModal.vue';
import UpdateSubscriptionModal from './UpdateSubscriptionModal.vue';
import DeleteSubscriptionModal from './DeleteSubscriptionModal.vue';
import { useSubscriptions } from '../../composables/useSubscriptions';

const { subscriptions, currentFilter } = useSubscriptions();
const showAddModal = ref(false);
const showUpdateModal = ref(false);
const showDeleteModal = ref(false);

const visibleRecordCount = computed(() => {
  if (currentFilter.value === 'all') {
    return subscriptions.value.length;
  }

  return subscriptions.value.filter((sub) => sub.cycle === currentFilter.value).length;
});
</script>

<template>
  <div class="control-bar">
    <div class="crud-group">
      <button class="control-btn add-btn" @click="showAddModal = true">
        <i class="fa-solid fa-plus"></i>
        <span>Add</span>
      </button>

      <button class="control-btn update-btn" @click="showUpdateModal = true">
        <i class="fa-solid fa-pen-to-square"></i>
        <span>Update</span>
      </button>
      
      <button class="control-btn delete-btn" @click="showDeleteModal = true">
        <i class="fa-solid fa-trash"></i>
        <span>Delete</span>
      </button>
    </div>

    <div class="filter-group">
      <div class="select-wrapper">
        <select v-model="currentFilter" class="payment-dropdown" value="Payment Cycle">
          <option value="all">All Cycles</option>
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
          <option value="annual">Annual</option>
        </select>
        <span class="dropdown-arrow">▼</span>
      </div>

      <button class="control-btn records-btn" type="button">
        <i class="fa-solid fa-bars"></i>
        <span>{{ visibleRecordCount }} Record{{ visibleRecordCount === 1 ? '' : 's' }}</span>
      </button>
    </div>
  </div>

  <AddSubscriptionModal
    v-if="showAddModal"
    @close="showAddModal = false"
  />

  <UpdateSubscriptionModal
    v-if="showUpdateModal"
    @close="showUpdateModal = false"
  />

  <DeleteSubscriptionModal
    v-if="showDeleteModal"
    @close="showDeleteModal = false"
  />
</template>

<style scoped>
.control-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding: 0 10px;
  gap: 16px;
  flex-wrap: wrap;
}

.crud-group,
.filter-group {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}

.control-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  border: none;
  background-color: var(--app-surface-alt);
  padding: 10px 20px;
  border-radius: 20px;
  cursor: pointer;
  font-family: 'Montserrat', sans-serif;
  font-weight: 700;
  color: var(--app-text);
  border: 1px solid var(--app-border);
  box-shadow: var(--app-shadow-soft);
  transition: all 0.2s ease;
}

.control-btn i {
  font-size: 0.9rem;
}

.control-btn:hover {
  background-color: var(--app-accent-strong);
  color: #f5f5f5;
  border-color: transparent;
  transform: translateY(-1px);
}

.delete-btn {
  background-color: color-mix(in srgb, var(--app-danger) 22%, var(--app-surface-alt));
  color: white;
  border-color: transparent;
}

.delete-btn:hover {
  background-color: var(--app-danger);
}

.records-btn {
  padding: 10px 25px;
}

.select-wrapper {
  position: relative;
}

.payment-dropdown {
  appearance: none;
  background-color: var(--app-surface-alt);
  border: 1px solid var(--app-border);
  padding: 10px 35px 10px 20px;
  border-radius: 20px;
  font-family: 'Montserrat', sans-serif;
  font-weight: 700;
  cursor: pointer;
  color: var(--app-text);
  box-shadow: var(--app-shadow-soft);
}

.payment-dropdown:focus {
  outline: none;
  background-color: var(--app-surface-soft);
}

.dropdown-arrow {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.7rem;
  color: var(--app-text-muted);
  pointer-events: none;
}

.delete-btn:hover i {
  color: #ffe5e5;
  transition: color 0.3s ease;
}

@media (max-width: 959px) {
  .control-bar {
    padding: 0;
  }
}
</style>
