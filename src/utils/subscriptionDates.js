const DAY_IN_MS = 24 * 60 * 60 * 1000;

export function parseDateString(value) {
  if (!value) {
    return null;
  }

  const [year, month, day] = value.split('-').map(Number);

  if (!year || !month || !day) {
    return null;
  }

  return new Date(year, month - 1, day);
}

export function startOfDay(value = new Date()) {
  const date = new Date(value);
  date.setHours(0, 0, 0, 0);
  return date;
}

export function formatDateKey(value) {
  const date = value instanceof Date ? value : parseDateString(value);

  if (!date) {
    return '';
  }

  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');

  return `${year}-${month}-${day}`;
}

export function addDays(value, amount) {
  const date = new Date(value);
  date.setDate(date.getDate() + amount);
  return date;
}

export function startOfMonth(value = new Date()) {
  const date = value instanceof Date ? value : parseDateString(value);
  return new Date(date.getFullYear(), date.getMonth(), 1);
}

export function isSameCalendarDay(left, right) {
  return formatDateKey(left) === formatDateKey(right);
}

export function differenceInDays(left, right = new Date()) {
  const leftDate = startOfDay(left instanceof Date ? left : parseDateString(left));
  const rightDate = startOfDay(right instanceof Date ? right : parseDateString(right));

  if (!leftDate || !rightDate) {
    return 0;
  }

  return Math.round((leftDate.getTime() - rightDate.getTime()) / DAY_IN_MS);
}

export function formatCurrency(amount) {
  return new Intl.NumberFormat('en-PH', {
    style: 'currency',
    currency: 'PHP',
    currencyDisplay: 'narrowSymbol',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(Number(amount) || 0);
}

export function formatMonthDay(value) {
  const date = parseDateString(value);

  if (!date) {
    return '--';
  }

  return new Intl.DateTimeFormat('en-PH', {
    month: 'short',
    day: 'numeric',
  }).format(date);
}

export function formatLongDate(value) {
  const date = value instanceof Date ? value : parseDateString(value);

  if (!date) {
    return '--';
  }

  return new Intl.DateTimeFormat('en-PH', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
  }).format(date);
}

export function formatMonthTitle(value) {
  const date = value instanceof Date ? value : parseDateString(value);

  if (!date) {
    return '--';
  }

  return new Intl.DateTimeFormat('en-PH', {
    month: 'long',
    year: 'numeric',
  }).format(date);
}
