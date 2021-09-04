<template>
  <app-header page-title="日历视图" height="64px"></app-header>
  <main>
    <month-view/>
  </main>
</template>

<script>
import AppHeader from '../public/Header.vue'
import MonthView from './MonthView.vue'
export default {
  name: 'CalendarView',
  components: {
    AppHeader,
    MonthView
  },

  data: () => ({
    //
  }),
}
</script>