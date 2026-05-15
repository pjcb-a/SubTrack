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

function parseIsoDate(value) {
  if (!value) {
    return null;
  }

  const parsed = new Date(`${value}T00:00:00`);
  return Number.isNaN(parsed.getTime()) ? null : parsed;
}

function formatIsoDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function getMonthDayLimit(year, monthIndex) {
  return new Date(year, monthIndex + 1, 0).getDate();
}

function addMonthsClamped(date, monthsToAdd, anchorDay) {
  const monthIndex = date.getMonth() + monthsToAdd;
  const year = date.getFullYear() + Math.floor(monthIndex / 12);
  const normalizedMonth = ((monthIndex % 12) + 12) % 12;
  const safeDay = Math.min(anchorDay, getMonthDayLimit(year, normalizedMonth));
  return new Date(year, normalizedMonth, safeDay);
}

function addYearsClamped(date, yearsToAdd, anchorMonth, anchorDay) {
  const year = date.getFullYear() + yearsToAdd;
  const safeDay = Math.min(anchorDay, getMonthDayLimit(year, anchorMonth));
  return new Date(year, anchorMonth, safeDay);
}

function advanceOccurrence(date, unit, interval, anchorDate) {
  if (unit === 'day') {
    const next = new Date(date);
    next.setDate(next.getDate() + interval);
    return next;
  }

  if (unit === 'week') {
    const next = new Date(date);
    next.setDate(next.getDate() + (interval * 7));
    return next;
  }

  if (unit === 'year') {
    return addYearsClamped(
      date,
      interval,
      anchorDate.getMonth(),
      anchorDate.getDate(),
    );
  }

  return addMonthsClamped(date, interval, anchorDate.getDate());
}

function buildLocalCalendarOccurrences(from, to) {
  const fromDate = parseIsoDate(from);
  const toDate = parseIsoDate(to);

  if (!fromDate || !toDate) {
    return [];
  }

  const occurrences = [];

  subscriptions.value.forEach((subscription) => {
    if (!subscription.isActive) {
      return;
    }

    const anchorDate = parseIsoDate(subscription.anchorDate || subscription.dueDate);
    const recurrenceEndDate = parseIsoDate(subscription.recurrenceEndDate);
    if (!anchorDate) {
      return;
    }

    const recurrenceUnit = subscription.recurrenceUnit || 'month';
    const recurrenceInterval = Math.max(Number(subscription.recurrenceInterval) || 1, 1);
    let cursor = new Date(anchorDate);
    let guard = 0;

    while (cursor < fromDate && guard < 500) {
      cursor = advanceOccurrence(cursor, recurrenceUnit, recurrenceInterval, anchorDate);
      guard += 1;
    }

    while (cursor <= toDate && guard < 1000) {
      if (recurrenceEndDate && cursor > recurrenceEndDate) {
        break;
      }

      occurrences.push({
        id: `${subscription.id}-${formatIsoDate(cursor)}`,
        subscriptionId: subscription.id,
        name: subscription.name,
        categoryId: subscription.categoryId,
        category: subscription.category,
        amount: Number(subscription.amount) || 0,
        dueDate: formatIsoDate(cursor),
        recurrenceUnit,
        recurrenceInterval,
        cycle: subscription.cycle,
        scheduleLabel: subscription.scheduleLabel,
      });

      cursor = advanceOccurrence(cursor, recurrenceUnit, recurrenceInterval, anchorDate);
      guard += 1;
    }
  });

  return occurrences.sort((left, right) => left.dueDate.localeCompare(right.dueDate));
}

function formatUiSubscription(subscription) {
  const recurrenceUnit = subscription.recurrence_unit
    ?? (subscription.billing_cycle === 'weekly'
      ? 'week'
      : subscription.billing_cycle === 'annual'
        ? 'year'
        : 'month');
  const recurrenceInterval = subscription.recurrence_interval ?? 1;
  const cycle = subscription.billing_cycle
    ?? (
      recurrenceUnit === 'year' && recurrenceInterval === 1
        ? 'annual'
        : getRecurrenceFilterKey(recurrenceUnit, recurrenceInterval)
    );

  return {
    id: subscription.subscription_id,
    name: subscription.subscription_name,
    category: subscription.category_name || getCategoryNameById(subscription.category_id),
    categoryId: subscription.category_id,
    amount: Number(subscription.amount) || 0,
    cycle,
    scheduleLabel: getRecurrenceLabel(recurrenceUnit, recurrenceInterval),
    recurrenceUnit,
    recurrenceInterval,
    recurrenceEndMode: subscription.recurrence_end_mode || 'forever',
    recurrenceEndDate: subscription.recurrence_end_date || null,
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
  const cycle = recurrenceUnit === 'year' && recurrenceInterval === 1
    ? 'annual'
    : getRecurrenceFilterKey(recurrenceUnit, recurrenceInterval);

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
    cycle,
    scheduleLabel: getRecurrenceLabel(recurrenceUnit, recurrenceInterval),
  };
}

function buildApiPayload(subscription) {
  const dueDate = subscription.dueDate || subscription.anchorDate || new Date().toISOString().slice(0, 10);
  const parsedDueDate = new Date(`${dueDate}T00:00:00`);
  const dueDay = Number.isNaN(parsedDueDate.getTime()) ? 1 : parsedDueDate.getDate();
  const recurrenceUnit = subscription.recurrenceUnit || 'month';
  const recurrenceInterval = Math.max(Number(subscription.recurrenceInterval) || 1, 1);
  let normalizedCycle = 'custom';

  if (recurrenceInterval === 1) {
    if (recurrenceUnit === 'day') {
      normalizedCycle = 'daily';
    } else if (recurrenceUnit === 'week') {
      normalizedCycle = 'weekly';
    } else if (recurrenceUnit === 'month') {
      normalizedCycle = 'monthly';
    } else if (recurrenceUnit === 'year') {
      normalizedCycle = 'annual';
    }
  }

  return {
    category_id: Number(subscription.categoryId) || getDefaultCategoryId(),
    subscription_name: subscription.name,
    amount: Number(subscription.amount) || 0,
    billing_cycle: normalizedCycle || 'monthly',
    start_date: dueDate,
    due_day: dueDay,
    recurrence_unit: recurrenceUnit,
    recurrence_interval: recurrenceInterval,
    recurrence_end_mode: subscription.recurrenceEndMode || 'forever',
    recurrence_end_date: (
      subscription.recurrenceEndMode === 'until'
        ? subscription.recurrenceEndDate || null
        : null
    ),
    is_active: subscription.isActive ?? true,
    notification_setting: {
      notify_days_before: Number(subscription.notifyDays) || 3,
      notification_enabled: subscription.notificationEnabled ?? true,
    },
  };
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

async function fetchSubscriptions({ force = false } = {}) {
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
      const nextSubscriptions = response.subscriptions?.map(formatUiSubscription) ?? [];
      const nextDeletedSubscriptions = historyResponse.subscriptions?.map(formatUiSubscription) ?? [];

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
      if (!subscriptionsLoaded.value) {
        await fetchSubscriptions();
      }

      let responseOccurrences = [];

      try {
        const response = await apiRequest(
          `/api/subscriptions/calendar?from=${from}&to=${to}`,
        );
        responseOccurrences = response.occurrences?.map(formatCalendarOccurrence) ?? [];
      } catch {
        responseOccurrences = [];
      }

      calendarOccurrences.value = responseOccurrences.length
        ? responseOccurrences
        : buildLocalCalendarOccurrences(from, to);
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
