<!-- Second row containing the logic for the CRUD buttons -->

<script setup>
import { ref } from 'vue';
import AddSubscriptionModal from './AddSubscriptionModal.vue';
import UpdateSubscriptionModal from './UpdateSubscriptionModal.vue';
import DeleteSubscriptionModal from './DeleteSubscriptionModal.vue';
import { useSubscriptions } from '../../composables/useSubscriptions';
import { RECURRENCE_FILTER_OPTIONS } from '../../utils/subscriptionRecurrence';

const { subscriptions, currentFilter } = useSubscriptions();
const showAddModal = ref(false);
const showUpdateModal = ref(false);
const showDeleteModal = ref(false);
const controlNotice = ref(null);

const handleModalNotice = (notice) => {
  controlNotice.value = notice;

  if (notice) {
    window.setTimeout(() => {
      controlNotice.value = null;
    }, 4000);
  }
};
</script>

<template>
  <div v-if="controlNotice" class="control-notice" :class="controlNotice.tone">
    {{ controlNotice.message }}
  </div>

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
          <option
            v-for="option in RECURRENCE_FILTER_OPTIONS"
            :key="option.value"
            :value="option.value"
          >
            {{ option.label }}
          </option>
        </select>
        <span class="dropdown-arrow">▼</span>
      </div>

    </div>
  </div>

  <AddSubscriptionModal
    v-if="showAddModal"
    @close="showAddModal = false"
    @saved="handleModalNotice"
  />

  <UpdateSubscriptionModal
    v-if="showUpdateModal"
    @close="showUpdateModal = false"
    @saved="handleModalNotice"
  />

  <DeleteSubscriptionModal
    v-if="showDeleteModal"
    @close="showDeleteModal = false"
  />
</template>

<style scoped>
.control-notice {
  margin-bottom: 16px;
  padding: 12px 16px;
  border-radius: 14px;
  font-family: 'Montserrat', sans-serif;
  font-size: 0.9rem;
  font-weight: 600;
}

.control-notice.success {
  background: color-mix(in srgb, var(--app-accent) 14%, var(--app-surface));
  color: var(--app-accent);
  border: 1px solid color-mix(in srgb, var(--app-accent) 30%, transparent);
}

.control-notice.warning {
  background: color-mix(in srgb, #d48100 14%, var(--app-surface));
  color: #c27500;
  border: 1px solid color-mix(in srgb, #d48100 28%, transparent);
}

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
