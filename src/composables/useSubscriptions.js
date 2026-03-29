import { ref } from 'vue';
import { apiRequest } from '../lib/api';

const MOCK_SUBSCRIPTIONS = [
  { id: 1, name: 'Netflix', category: 'Entertainment', amount: 1500, cycle: 'monthly', dueDate: '2026-04-02', notifyDays: 3 },
  { id: 2, name: 'Spotify', category: 'Music', amount: 2500, cycle: 'monthly', dueDate: '2026-04-05', notifyDays: 1 },
];

const CATEGORY_ID_BY_NAME = {
  Entertainment: 1,
  Productivity: 2,
  Music: 3,
  'Cloud Storage': 4,
  Education: 5,
};

const subscriptions = ref([]);
const currentFilter = ref('all');
const subscriptionsLoading = ref(false);
const subscriptionsLoaded = ref(false);
const subscriptionsError = ref('');

let fetchPromise = null;

function formatUiSubscription(subscription) {
  return {
    id: subscription.subscription_id,
    name: subscription.subscription_name,
    category: subscription.category_name || 'Entertainment',
    categoryId: subscription.category_id,
    amount: Number(subscription.amount) || 0,
    cycle: subscription.billing_cycle,
    dueDate: subscription.next_due_date || subscription.start_date,
    notifyDays: subscription.notification_setting?.notify_days_before ?? 3,
    notificationEnabled: subscription.notification_setting?.notification_enabled ?? true,
    startDate: subscription.start_date,
    dueDay: subscription.due_day,
    isActive: subscription.is_active,
  };
}

function getCategoryId(subscription) {
  return subscription.categoryId || CATEGORY_ID_BY_NAME[subscription.category] || 1;
}

function buildApiPayload(subscription) {
  const effectiveDueDate = subscription.dueDate || subscription.startDate || new Date().toISOString().slice(0, 10);
  const dueDate = new Date(`${effectiveDueDate}T00:00:00`);
  const derivedDueDay = Number.isNaN(dueDate.getTime()) ? 1 : dueDate.getDate();

  return {
    category_id: getCategoryId(subscription),
    subscription_name: subscription.name,
    amount: Number(subscription.amount) || 0,
    billing_cycle: subscription.cycle,
    start_date: subscription.cycle === 'weekly'
      ? effectiveDueDate
      : (subscription.startDate || effectiveDueDate),
    due_day: derivedDueDay,
    is_active: subscription.isActive ?? true,
    notification_setting: {
      notify_days_before: subscription.notifyDays ?? 3,
      notification_enabled: subscription.notificationEnabled ?? true,
    },
  };
}

async function seedMockSubscriptionsForUser() {
  for (const mockSubscription of MOCK_SUBSCRIPTIONS) {
    await apiRequest('/api/subscriptions', {
      method: 'POST',
      body: buildApiPayload(mockSubscription),
    });
  }
}

async function fetchSubscriptions({ seedIfEmpty = true, force = false } = {}) {
  if (fetchPromise && !force) {
    return fetchPromise;
  }

  subscriptionsLoading.value = true;
  subscriptionsError.value = '';

  fetchPromise = (async () => {
    try {
      let response = await apiRequest('/api/subscriptions');
      let nextSubscriptions = response.subscriptions?.map(formatUiSubscription) ?? [];

      if (seedIfEmpty && nextSubscriptions.length === 0) {
        await seedMockSubscriptionsForUser();
        response = await apiRequest('/api/subscriptions');
        nextSubscriptions = response.subscriptions?.map(formatUiSubscription) ?? [];
      }

      subscriptions.value = nextSubscriptions;
      subscriptionsLoaded.value = true;
      return subscriptions.value;
    } catch (error) {
      subscriptionsError.value = error.message;
      throw error;
    } finally {
      subscriptionsLoading.value = false;
      fetchPromise = null;
    }
  })();

  return fetchPromise;
}

async function addSubscription(subscription) {
  const response = await apiRequest('/api/subscriptions', {
    method: 'POST',
    body: buildApiPayload(subscription),
  });
  const nextSubscription = formatUiSubscription(response.subscription);

  subscriptions.value = [nextSubscription, ...subscriptions.value];
  return nextSubscription;
}

async function updateSubscription(id, updatedSubscription) {
  const currentSubscription = subscriptions.value.find((subscription) => subscription.id === id);
  const response = await apiRequest(`/api/subscriptions/${id}`, {
    method: 'PUT',
    body: buildApiPayload({ ...currentSubscription, ...updatedSubscription }),
  });
  const nextSubscription = formatUiSubscription(response.subscription);

  subscriptions.value = subscriptions.value.map((subscription) => (
    subscription.id === id ? nextSubscription : subscription
  ));

  return nextSubscription;
}

async function deleteSubscription(id) {
  await apiRequest(`/api/subscriptions/${id}`, {
    method: 'DELETE',
  });

  subscriptions.value = subscriptions.value.filter((subscription) => subscription.id !== id);
}

function resetSubscriptionStore() {
  subscriptions.value = [];
  subscriptionsLoaded.value = false;
  subscriptionsLoading.value = false;
  subscriptionsError.value = '';
}

export function useSubscriptions() {
  return {
    subscriptions,
    currentFilter,
    subscriptionsLoading,
    subscriptionsLoaded,
    subscriptionsError,
    fetchSubscriptions,
    addSubscription,
    updateSubscription,
    deleteSubscription,
    resetSubscriptionStore,
  };
}
