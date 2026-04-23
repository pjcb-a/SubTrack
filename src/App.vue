<script setup>
import { Analytics } from '@vercel/analytics/vue';
import { SpeedInsights } from "@vercel/speed-insights/vue"
</script>

<template>
  <Analytics/>
  <SpeedInsights/>
  <router-view />
</template>

<style scoped>
  body, html {
  margin: 0;
  padding: 0;
  overflow: hidden;
  }
</style>
