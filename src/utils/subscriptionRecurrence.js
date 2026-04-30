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
  { value: 'custom', label: 'Custom' },
];

export function getRecurrenceFilterKey(recurrenceUnit = 'month', recurrenceInterval = 1) {
  const normalizedUnit = String(recurrenceUnit || 'month').toLowerCase();
  const normalizedInterval = Number(recurrenceInterval) || 1;

  if (normalizedInterval > 1) {
    return 'custom';
  }

  if (normalizedUnit === 'day') {
    return 'daily';
  }

  if (normalizedUnit === 'week') {
    return 'weekly';
  }

  if (normalizedUnit === 'month') {
    return 'monthly';
  }

  if (normalizedUnit === 'year') {
    return 'yearly';
  }

  return 'custom';
}

export function getRecurrenceLabel(recurrenceUnit = 'month', recurrenceInterval = 1) {
  const normalizedUnit = String(recurrenceUnit || 'month').toLowerCase();
  const normalizedInterval = Math.max(Number(recurrenceInterval) || 1, 1);

  if (normalizedInterval === 1) {
    if (normalizedUnit === 'day') {
      return 'Daily';
    }

    if (normalizedUnit === 'week') {
      return 'Weekly';
    }

    if (normalizedUnit === 'month') {
      return 'Monthly';
    }

    if (normalizedUnit === 'year') {
      return 'Yearly';
    }
  }

  const unitLabel = normalizedUnit === 'day'
    ? 'day'
    : normalizedUnit === 'week'
      ? 'week'
      : normalizedUnit === 'month'
        ? 'month'
        : 'year';

  const pluralSuffix = normalizedInterval === 1 ? '' : 's';
  return `Every ${normalizedInterval} ${unitLabel}${pluralSuffix}`;
}

export function getRecurrencePreset(recurrenceUnit = 'month', recurrenceInterval = 1) {
  return getRecurrenceFilterKey(recurrenceUnit, recurrenceInterval);
}

export function buildRecurrenceFromForm({
  preset = 'monthly',
  customInterval = 1,
  customUnit = 'month',
} = {}) {
  if (preset === 'daily') {
    return { recurrenceUnit: 'day', recurrenceInterval: 1 };
  }

  if (preset === 'weekly') {
    return { recurrenceUnit: 'week', recurrenceInterval: 1 };
  }

  if (preset === 'monthly') {
    return { recurrenceUnit: 'month', recurrenceInterval: 1 };
  }

  if (preset === 'yearly') {
    return { recurrenceUnit: 'year', recurrenceInterval: 1 };
  }

  return {
    recurrenceUnit: customUnit || 'month',
    recurrenceInterval: Math.max(Number(customInterval) || 1, 1),
  };
}

export function buildRecurrenceForm(subscription = {}) {
  const recurrenceUnit = subscription.recurrenceUnit || 'month';
  const recurrenceInterval = Math.max(Number(subscription.recurrenceInterval) || 1, 1);

  return {
    preset: getRecurrencePreset(recurrenceUnit, recurrenceInterval),
    customInterval: recurrenceInterval,
    customUnit: recurrenceUnit,
  };
}
