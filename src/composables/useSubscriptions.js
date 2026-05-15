import { ref } from 'vue';
import { apiRequest } from '../lib/api';
import {
  getDefaultCategoryId,
  getCategoryNameById,
} from '../utils/subscriptionCategories';
import {
  getRecurrenceFilterKey,
  getRecurrenceLabel,
} from '../utils/subscriptionRecurrence';

const MOCK_SUBSCRIPTIONS = [
  {
    name: 'Netflix',
    categoryId: 1,
    amount: 549,
    recurrenceUnit: 'month',
    recurrenceInterval: 1,
    anchorDate: '2026-04-15',
    notifyDays: 3,
  },
  {
    name: 'Spotify',
    categoryId: 3,
    amount: 149,
    recurrenceUnit: 'month',
    recurrenceInterval: 1,
    anchorDate: '2026-04-05',
    notifyDays: 1,
  },
];

const subscriptions = ref([]);
const deletedSubscriptions = ref([]);
const calendarOccurrences = ref([]);
const currentFilter = ref('all');
const subscriptionsLoading = ref(false);
const subscriptionsLoaded = ref(false);
const subscriptionsError = ref('');
const calendarLoading = ref(false);
const calendarError = ref('');

let fetchPromise = null;
let calendarPromise = null;
const lastCalendarRange = ref(null);

function formatUiSubscription(subscription) {
  const recurrenceUnit = subscription.recurrence_unit ?? 'month';
  const recurrenceInterval = subscription.recurrence_interval ?? 1;

  return {
    id: subscription.subscription_id,
    name: subscription.subscription_name,
    category: subscription.category_name || getCategoryNameById(subscription.category_id),
    categoryId: subscription.category_id,
    amount: Number(subscription.amount) || 0,
    cycle: getRecurrenceFilterKey(recurrenceUnit),
    scheduleLabel: getRecurrenceLabel(recurrenceUnit, recurrenceInterval),
    recurrenceUnit,
    recurrenceInterval,
    anchorDate: subscription.anchor_date || subscription.start_date,
    dueDate: subscription.next_due_date || subscription.anchor_date || subscription.start_date,
    notifyDays: subscription.notification_setting?.notify_days_before ?? 3,
    notificationEnabled: subscription.notification_setting?.notification_enabled ?? true,
    isActive: subscription.is_active,
    deletedAt: subscription.deleted_at || null,
  };
}

function formatCalendarOccurrence(occurrence) {
  const recurrenceUnit = occurrence.recurrence_unit ?? 'month';
  const recurrenceInterval = occurrence.recurrence_interval ?? 1;

  return {
    id: `${occurrence.subscription_id}-${occurrence.occurrence_date}`,
    subscriptionId: occurrence.subscription_id,
    name: occurrence.subscription_name,
    categoryId: occurrence.category_id,
    category: occurrence.category_name || getCategoryNameById(occurrence.category_id),
    amount: Number(occurrence.amount) || 0,
    dueDate: occurrence.occurrence_date,
    recurrenceUnit,
    recurrenceInterval,
    cycle: getRecurrenceFilterKey(recurrenceUnit),
    scheduleLabel: getRecurrenceLabel(recurrenceUnit, recurrenceInterval),
  };
}

function buildApiPayload(subscription) {
  const recurrenceUnit = subscription.recurrenceUnit || 'month';
  const recurrenceInterval = Math.max(Number(subscription.recurrenceInterval) || 1, 1);
  const anchorDate = subscription.anchorDate || new Date().toISOString().slice(0, 10);

  return {
    category_id: Number(subscription.categoryId) || getDefaultCategoryId(),
    subscription_name: subscription.name,
    amount: Number(subscription.amount) || 0,
    recurrence_unit: recurrenceUnit,
    recurrence_interval: recurrenceInterval,
    anchor_date: anchorDate,
    is_active: subscription.isActive ?? true,
    notification_setting: {
      notify_days_before: Number(subscription.notifyDays) || 0,
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

async function refreshCurrentCalendarRange() {
  if (!lastCalendarRange.value) {
    return;
  }

  await fetchCalendarOccurrences({
    ...lastCalendarRange.value,
    force: true,
  });
}

async function fetchSubscriptions({ seedIfEmpty = true, force = false } = {}) {
  if (fetchPromise && !force) {
    return fetchPromise;
  }

  subscriptionsLoading.value = true;
  subscriptionsError.value = '';

  fetchPromise = (async () => {
    try {
      const [response, historyResponse] = await Promise.all([
        apiRequest('/api/subscriptions'),
        apiRequest('/api/subscriptions/history'),
      ]);
      let nextSubscriptions = response.subscriptions?.map(formatUiSubscription) ?? [];
      let nextDeletedSubscriptions = historyResponse.subscriptions?.map(formatUiSubscription) ?? [];

      if (seedIfEmpty && nextSubscriptions.length === 0 && nextDeletedSubscriptions.length === 0) {
        await seedMockSubscriptionsForUser();
        [response, historyResponse] = await Promise.all([
          apiRequest('/api/subscriptions'),
          apiRequest('/api/subscriptions/history'),
        ]);
        nextSubscriptions = response.subscriptions?.map(formatUiSubscription) ?? [];
        nextDeletedSubscriptions = historyResponse.subscriptions?.map(formatUiSubscription) ?? [];
      }

      subscriptions.value = nextSubscriptions;
      deletedSubscriptions.value = nextDeletedSubscriptions;
      subscriptionsLoaded.value = true;

      if (lastCalendarRange.value) {
        await refreshCurrentCalendarRange();
      }

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

async function fetchCalendarOccurrences({ from, to, force = false }) {
  const nextRangeKey = `${from}:${to}`;

  if (
    calendarPromise
    && !force
    && lastCalendarRange.value
    && `${lastCalendarRange.value.from}:${lastCalendarRange.value.to}` === nextRangeKey
  ) {
    return calendarPromise;
  }

  calendarLoading.value = true;
  calendarError.value = '';
  lastCalendarRange.value = { from, to };

  calendarPromise = (async () => {
    try {
      const response = await apiRequest(
        `/api/subscriptions/calendar?from=${from}&to=${to}`,
      );
      calendarOccurrences.value = response.occurrences?.map(formatCalendarOccurrence) ?? [];
      return calendarOccurrences.value;
    } catch (error) {
      calendarError.value = error.message;
      throw error;
    } finally {
      calendarLoading.value = false;
      calendarPromise = null;
    }
  })();

  return calendarPromise;
}

async function addSubscription(subscription) {
  const response = await apiRequest('/api/subscriptions', {
    method: 'POST',
    body: buildApiPayload(subscription),
  });
  const nextSubscription = formatUiSubscription(response.subscription);

  subscriptions.value = [nextSubscription, ...subscriptions.value];
  await refreshCurrentCalendarRange();

  return {
    subscription: nextSubscription,
    capWarning: response.cap_warning ?? null,
  };
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
  await refreshCurrentCalendarRange();

  return {
    subscription: nextSubscription,
    capWarning: response.cap_warning ?? null,
  };
}

async function deleteSubscription(id) {
  const response = await apiRequest(`/api/subscriptions/${id}`, {
    method: 'DELETE',
  });
  const archivedSubscription = formatUiSubscription(response.subscription);

  subscriptions.value = subscriptions.value.filter((subscription) => subscription.id !== id);
  deletedSubscriptions.value = [archivedSubscription, ...deletedSubscriptions.value];
  await refreshCurrentCalendarRange();
}

async function clearDeletedSubscriptions() {
  await apiRequest('/api/subscriptions/history', {
    method: 'DELETE',
  });

  deletedSubscriptions.value = [];
}

function resetSubscriptionStore() {
  subscriptions.value = [];
  deletedSubscriptions.value = [];
  calendarOccurrences.value = [];
  subscriptionsLoaded.value = false;
  subscriptionsLoading.value = false;
  subscriptionsError.value = '';
  calendarLoading.value = false;
  calendarError.value = '';
  lastCalendarRange.value = null;
}

export function useSubscriptions() {
  return {
    subscriptions,
    deletedSubscriptions,
    calendarOccurrences,
    currentFilter,
    subscriptionsLoading,
    subscriptionsLoaded,
    subscriptionsError,
    calendarLoading,
    calendarError,
    fetchSubscriptions,
    fetchCalendarOccurrences,
    addSubscription,
    updateSubscription,
    deleteSubscription,
    clearDeletedSubscriptions,
    resetSubscriptionStore,
  };
}
