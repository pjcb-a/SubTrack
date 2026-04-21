<script setup>
import { computed, ref } from 'vue';
import { useSubscriptions } from '../../composables/useSubscriptions';
import {
  addDays,
  formatCurrency,
  formatDateKey,
  formatLongDate,
  formatMonthTitle,
  isSameCalendarDay,
  parseDateString,
  startOfMonth,
} from '../../utils/subscriptionDates';

const weekDays = ref(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']);
const { subscriptions, currentFilter } = useSubscriptions();
const today = new Date();
const visibleMonth = ref(startOfMonth(today));
const selectedDate = ref(formatDateKey(today));

const cycleColors = {
  weekly: '#00a859',
  monthly: '#004d26',
  annual: '#bcbcbc',
};

const filteredSubscriptions = computed(() => {
  if (currentFilter.value === 'all') {
    return subscriptions.value;
  }

  return subscriptions.value.filter((subscription) => subscription.cycle === currentFilter.value);
});

const paymentMap = computed(() => {
  const map = new Map();

  filteredSubscriptions.value.forEach((subscription) => {
    if (!subscription.dueDate) {
      return;
    }

    const list = map.get(subscription.dueDate) ?? [];
    list.push(subscription);
    map.set(subscription.dueDate, list);
  });

  return map;
});

const monthLabel = computed(() => formatMonthTitle(visibleMonth.value));
const monthStart = computed(() => startOfMonth(visibleMonth.value));
const calendarDates = computed(() => {
  const firstDayOfMonth = monthStart.value;
  const mondayIndex = (firstDayOfMonth.getDay() + 6) % 7;
  const gridStart = addDays(firstDayOfMonth, -mondayIndex);

  return Array.from({ length: 42 }, (_, index) => {
    const date = addDays(gridStart, index);
    const fullDate = formatDateKey(date);
    const payments = paymentMap.value.get(fullDate) ?? [];

    return {
      dayNumber: date.getDate(),
      fullDate,
      isCurrentMonth: date.getMonth() === visibleMonth.value.getMonth() && date.getFullYear() === visibleMonth.value.getFullYear(),
      isToday: isSameCalendarDay(date, today),
      payments,
      paymentColors: payments.slice(0, 3).map((payment) => cycleColors[payment.cycle] ?? '#004d26'),
    };
  });
});

const monthRenewalCount = computed(() => calendarDates.value
  .filter((date) => date.isCurrentMonth)
  .reduce((count, date) => count + date.payments.length, 0));

const selectedDayPayments = computed(() => paymentMap.value.get(selectedDate.value) ?? []);
const selectedDateLabel = computed(() => formatLongDate(selectedDate.value));
const selectedDateTotal = computed(() => selectedDayPayments.value.reduce(
  (total, payment) => total + (Number(payment.amount) || 0),
  0,
));

const shiftMonth = (offset) => {
  const nextMonth = new Date(visibleMonth.value);
  nextMonth.setMonth(nextMonth.getMonth() + offset);
  visibleMonth.value = startOfMonth(nextMonth);

  if (
    today.getMonth() === visibleMonth.value.getMonth() &&
    today.getFullYear() === visibleMonth.value.getFullYear()
  ) {
    selectedDate.value = formatDateKey(today);
    return;
  }

  selectedDate.value = formatDateKey(visibleMonth.value);
};

const selectDate = (fullDate) => {
  selectedDate.value = fullDate;
};

const formatPaymentAmount = (amount) => formatCurrency(amount);
const formatPaymentDate = (value) => formatLongDate(parseDateString(value));
</script>

<template>
  <div class="calendar-container">
    <div class="calendar-header">
      <div>
        <h2>{{ monthLabel }}</h2>
        <p class="calendar-subtitle">{{ monthRenewalCount }} scheduled renewal{{ monthRenewalCount === 1 ? '' : 's' }}</p>
      </div>

      <div class="calendar-nav">
        <button class="nav-btn" type="button" aria-label="Previous month" @click="shiftMonth(-1)">
          <i class="fa-solid fa-chevron-left"></i>
        </button>
        <button class="nav-btn" type="button" aria-label="Next month" @click="shiftMonth(1)">
          <i class="fa-solid fa-chevron-right"></i>
        </button>
      </div>
    </div>

    <div class="calendar-grid">
      <div v-for="day in weekDays" :key="day" class="weekday-header">{{ day }}</div>

      <div
        v-for="date in calendarDates"
        :key="date.fullDate"
        class="calendar-day"
        :class="{
          'other-month': !date.isCurrentMonth,
          today: date.isToday,
          selected: date.fullDate === selectedDate,
        }"
        @click="selectDate(date.fullDate)"
      >
        <span class="day-number">{{ date.dayNumber }}</span>

        <p v-if="date.payments.length" class="day-count">{{ date.payments.length }} due</p>

        <div v-if="date.payments.length" class="payment-dots">
          <span v-for="color in date.paymentColors" :key="color" :style="{ backgroundColor: color }"></span>
        </div>
      </div>
    </div>

    <div class="agenda-panel">
      <div class="agenda-header">
        <div>
          <p class="agenda-label">Selected day</p>
          <h3>{{ selectedDateLabel }}</h3>
        </div>

        <div class="agenda-total">
          <span>Total</span>
          <strong>{{ formatPaymentAmount(selectedDateTotal) }}</strong>
        </div>
      </div>

      <div v-if="selectedDayPayments.length" class="agenda-list">
        <div v-for="payment in selectedDayPayments" :key="payment.id" class="agenda-item">
          <div>
            <p class="agenda-name">{{ payment.name }}</p>
            <p class="agenda-date">{{ formatPaymentDate(payment.dueDate) }}</p>
          </div>
          <p class="agenda-amount">{{ formatPaymentAmount(payment.amount) }}</p>
        </div>
      </div>

      <p v-else class="agenda-empty">No subscription renewals are scheduled for this day.</p>
    </div>
  </div>
</template>

<style scoped>
.calendar-container {
  background: color-mix(in srgb, var(--app-surface) 92%, transparent);
  min-width: 500px;
  border-radius: 20px;
  padding: 25px;
  box-shadow: var(--app-shadow);
  display: flex;
  flex-direction: column;
  border: 1px solid var(--app-border);
  backdrop-filter: blur(16px);
  transition: background-color 0.3s ease, transform 0.3s ease;
  font-family: 'Montserrat', sans-serif;
}

.calendar-container:hover {
  background-color: color-mix(in srgb, var(--app-surface) 96%, transparent);
  transform: scale(1.02)
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.calendar-header h2 {
  font-family: 'Montserrat', sans-serif;
  color: var(--app-heading);
  font-weight: 800;
  font-size: 1.4rem;
}

.calendar-subtitle {
  font-size: 0.85rem;
  color: var(--app-text-muted);
  margin-top: 4px;
}

.calendar-nav {
  display: flex;
  gap: 5px;
}

.nav-btn {
  background-color: var(--app-surface-alt);
  border: 1px solid var(--app-border);
  border-radius: 8px;
  padding: 8px 12px;
  cursor: pointer;
  font-weight: 800;
  color: var(--app-text);
  transition: background-color 0.2s ease, transform 0.2s ease;
}

.nav-btn:hover {
  background-color: var(--app-surface-soft);
  transform: translateY(-1px);
}

.calendar-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(7, minmax(60px, 1fr));
  gap: 8px;
}

.weekday-header {
  text-align: center;
  font-weight: 700;
  color: var(--app-heading);
  font-size: 0.9rem;
  padding-bottom: 10px;
}

.calendar-day {
  background-color: var(--app-surface-alt);
  border-radius: 12px;
  padding: 10px;
  position: relative;
  min-height: 88px;
  transition: background-color 0.2s ease, transform 0.2s ease, border-color 0.2s ease;
  border: 1px solid var(--app-border);
}

.calendar-day:hover {
  background-color: var(--app-surface-soft);
  cursor: pointer;
  transform: translateY(-1px);
}

.day-number {
  position: absolute;
  top: 8px;
  right: 10px;
  font-weight: 700;
  font-size: 0.9rem;
  color: var(--app-text-muted);
}

.day-count {
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--app-accent);
  margin-top: 28px;
}

.calendar-day.other-month {
  opacity: 0.4;
  background-color: transparent;
}

.calendar-day.today {
  background-color: var(--app-accent-soft);
  border: 1px solid var(--app-accent-strong);
}

.calendar-day.today .day-number {
  color: var(--app-accent);
}

.calendar-day.selected {
  border-color: var(--app-accent-strong);
  box-shadow: inset 0 0 0 1px var(--app-accent-soft);
}

.payment-dots {
  position: absolute;
  bottom: 8px;
  left: 10px;
  display: flex;
  gap: 4px;
}

.payment-dots span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.agenda-panel {
  margin-top: 18px;
  border-top: 1px solid var(--app-border);
  padding-top: 18px;
  font-family: 'Montserrat', sans-serif;
}

.agenda-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}

.agenda-label {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--app-text-muted);
  margin-bottom: 4px;
}

.agenda-header h3 {
  color: var(--app-heading);
  font-size: 1rem;
}

.agenda-total {
  text-align: right;
  font-size: 0.75rem;
  color: var(--app-text-muted);
}

.agenda-total strong {
  display: block;
  margin-top: 4px;
  color: var(--app-accent);
  font-size: 1rem;
}

.agenda-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.agenda-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 14px;
  background: var(--app-surface-alt);
  border-radius: 12px;
  padding: 12px 14px;
}

.agenda-name {
  font-weight: 700;
  color: var(--app-text);
}

.agenda-date {
  font-size: 0.8rem;
  color: var(--app-text-muted);
  margin-top: 3px;
}

.agenda-amount {
  font-weight: 700;
  color: var(--app-accent);
}

.agenda-empty {
  color: var(--app-text-muted);
  font-size: 0.88rem;
}

@media (max-width: 959px) {
  .calendar-container {
    min-width: 0;
    padding: 20px 16px;
  }

  .calendar-grid {
    grid-template-columns: repeat(7, minmax(0, 1fr));
  }

  .calendar-day {
    min-height: 78px;
  }

  .agenda-header,
  .agenda-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .agenda-total {
    text-align: left;
  }
}
</style>
