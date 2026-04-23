const PRESET_UNIT_MAP = {
  daily: 'day',
  weekly: 'week',
  monthly: 'month',
  yearly: 'year',
};

const FILTER_KEY_BY_UNIT = {
  day: 'daily',
  week: 'weekly',
  month: 'monthly',
  year: 'yearly',
};

export const RECURRENCE_PRESET_OPTIONS = [
  { value: 'daily', label: 'Daily' },
  { value: 'weekly', label: 'Weekly' },
  { value: 'monthly', label: 'Monthly' },
  { value: 'yearly', label: 'Yearly' },
  { value: 'custom', label: 'Custom' },
];

export const RECURRENCE_UNIT_OPTIONS = [
  { value: 'day', label: 'Days' },
  { value: 'week', label: 'Weeks' },
  { value: 'month', label: 'Months' },
  { value: 'year', label: 'Years' },
];

export const RECURRENCE_FILTER_OPTIONS = [
  { value: 'all', label: 'All Schedules' },
  { value: 'daily', label: 'Daily' },
  { value: 'weekly', label: 'Weekly' },
  { value: 'monthly', label: 'Monthly' },
  { value: 'yearly', label: 'Yearly' },
];

function pluralize(unit, interval) {
  if (interval === 1) {
    return unit;
  }

  if (unit === 'day') return 'days';
  if (unit === 'week') return 'weeks';
  if (unit === 'month') return 'months';
  return 'years';
}

export function getRecurrenceFilterKey(recurrenceUnit = 'month') {
  return FILTER_KEY_BY_UNIT[recurrenceUnit] ?? 'monthly';
}

export function getRecurrenceLabel(recurrenceUnit = 'month', recurrenceInterval = 1) {
  if (recurrenceInterval === 1) {
    if (recurrenceUnit === 'day') return 'Daily';
    if (recurrenceUnit === 'week') return 'Weekly';
    if (recurrenceUnit === 'month') return 'Monthly';
    return 'Yearly';
  }

  return `Every ${recurrenceInterval} ${pluralize(recurrenceUnit, recurrenceInterval)}`;
}

export function getRecurrencePreset(recurrenceUnit = 'month', recurrenceInterval = 1) {
  if (recurrenceInterval === 1) {
    return FILTER_KEY_BY_UNIT[recurrenceUnit] ?? 'monthly';
  }

  return 'custom';
}

export function buildRecurrenceFromForm({
  recurrencePreset,
  customRecurrenceUnit,
  customRecurrenceInterval,
}) {
  if (recurrencePreset === 'custom') {
    return {
      recurrenceUnit: customRecurrenceUnit || 'day',
      recurrenceInterval: Math.max(Number(customRecurrenceInterval) || 1, 1),
    };
  }

  return {
    recurrenceUnit: PRESET_UNIT_MAP[recurrencePreset] ?? 'month',
    recurrenceInterval: 1,
  };
}

export function buildRecurrenceForm(subscription) {
  const recurrencePreset = getRecurrencePreset(
    subscription.recurrenceUnit,
    subscription.recurrenceInterval,
  );

  return {
    recurrencePreset,
    customRecurrenceUnit: subscription.recurrenceUnit ?? 'day',
    customRecurrenceInterval: subscription.recurrenceInterval ?? 1,
  };
}
