import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'

import AuthPage from './components/authorization/AuthPage.vue'
import Dashboard from './Dashboard.vue'

const routes = [
    { path: '/', component: AuthPage },
    { path: '/dashboard', component: Dashboard }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

const app = createApp(App)
app.use(router)


app.mount('#app')
