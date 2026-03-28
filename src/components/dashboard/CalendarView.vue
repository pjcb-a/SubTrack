<script setup>
import { ref } from 'vue';

const weekDays = ref(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']);

// Mock Data for a prototype calendar grid
const calendarDates = ref([
  { dayNumber: 29, isCurrentMonth: false, fullDate: '2026-03-29' },
  { dayNumber: 30, isCurrentMonth: false, fullDate: '2026-03-30' },
  { dayNumber: 31, isCurrentMonth: false, fullDate: '2026-03-31' },
  { dayNumber: 1,  isCurrentMonth: true,  fullDate: '2026-04-01' },
  { dayNumber: 2,  isCurrentMonth: true,  fullDate: '2026-04-02', hasPayments: true, paymentColors: ['#004d26'] },
  { dayNumber: 3,  isCurrentMonth: true,  fullDate: '2026-04-03', isToday: true },
  { dayNumber: 4,  isCurrentMonth: true,  fullDate: '2026-04-04' },
  { dayNumber: 5,  isCurrentMonth: true,  fullDate: '2026-04-05', hasPayments: true, paymentColors: ['#bcbcbc', '#004d26'] },
  // ... more mock dates to fill the grid ...
  { dayNumber: 10, isCurrentMonth: false, fullDate: '2026-05-10' }
]);
</script>

<template>
  <div class="calendar-container">
    <div class="calendar-header">
      <h2>April 2026</h2>
      <div class="calendar-nav">
        <button class="nav-btn">&lt;</button>
        <button class="nav-btn">&gt;</button>
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
          'today': date.isToday
        }"
      >
        <span class="day-number">{{ date.dayNumber }}</span>
        
        <div v-if="date.hasPayments" class="payment-dots">
          <span v-for="color in date.paymentColors" :key="color" :style="{ backgroundColor: color }"></span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.calendar-container {
  background-color: white;
  min-width: 500px;
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.calendar-header h2 {
  font-family: 'Montserrat', sans-serif;
  color: #004d26;
  font-weight: 800;
  font-size: 1.4rem;
}

.calendar-nav { 
  display: flex; gap: 5px;
 }

.nav-btn {
  background-color: #f1f1f1;
  border: none;
  border-radius: 8px;
  padding: 8px 12px;
  cursor: pointer;
  font-weight: 800;
  color: #333;
}
.nav-btn:hover { 
  background-color: #e0e0e0;
 }

.calendar-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(7, minmax(60px, 1fr)); /* 7 days of the week */
  gap: 8px; /* Consistent spacing between days */
}

.weekday-header {
  text-align: center;
  font-weight: 700;
  color: #004d26;
  font-size: 0.9rem;
  padding-bottom: 10px;
}

.calendar-day {
  background-color: #f8f8f8;
  border-radius: 12px;
  padding: 10px;
  position: relative;
  min-height: 80px; /* Minimum height for prototype look */
  transition: background-color 0.2s ease;
}
.calendar-day:hover { background-color: #f1f1f1; cursor: pointer; }

.day-number {
  position: absolute;
  top: 8px;
  right: 10px;
  font-weight: 700;
  font-size: 0.9rem;
  color: #666;
}

/* Specific state styling */
.calendar-day.other-month { opacity: 0.4; background-color: transparent; }
.calendar-day.today { background-color: rgba(0, 77, 38, 0.05); border: 1px solid #004d26; }
.calendar-day.today .day-number { color: #004d26; }

/* Payment Indicators */
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
</style>