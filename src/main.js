import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'

import AuthPage from './components/authorization/AuthPage.vue'
import Dashboard from './Dashboard.vue'
import { useAuth } from './composables/useAuth'
import { useSubscriptions } from './composables/useSubscriptions'

const routes = [
    { path: '/', component: AuthPage, meta: { guestOnly: true } },
    { 
      path: '/dashboard', 
      component: Dashboard, 
      meta: { requiresAuth: true },
      children: [
        { 
          path: 'history', 
          component: () => import('./components/history/HistoryView.vue') 
        },
        
        {
            path: 'settings', 
            component: () => import('./components/settings/SettingsView.vue')
        },
        {
            path: 'about',
            component: () => import('./components/about/AboutView.vue')
        }
      ]
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach(async (to) => {
    const { currentUser, restoreSession } = useAuth()
    const { resetSubscriptionStore } = useSubscriptions()

    await restoreSession()

    if (to.meta.requiresAuth && !currentUser.value) {
        resetSubscriptionStore()
        return '/'
    }

    if (to.meta.guestOnly && currentUser.value) {
        return '/dashboard'
    }
})

const app = createApp(App)
app.use(router)


app.mount('#app')
