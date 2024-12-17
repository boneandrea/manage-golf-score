import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import { createMemoryHistory, createRouter } from 'vue-router'
import HdcpView from './components/HdcpView.vue'
import ScoreFormView from './components/ScoreFormView.vue'
import ToastPlugin from 'vue-toast-notification'

const routes = [
  {
    path: '/new',
    component: ScoreFormView,
    props: true,
  },
  {
    path: '/hdcp',
    component: HdcpView,
    props: true,
  },
]

const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

createApp(App).use(router).use(ToastPlugin).mount('#app')
