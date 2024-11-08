import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: () => import('../views/environment.vue'),
    },
    {
      path: '/environment',
      name: 'environment',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/environment.vue'),
    },
    {
      path: '/deepflow',
      name: 'deepflow',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/deepflow.vue'),
    },
    {
      path: '/nessus',
      name: 'nessus',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/nessus.vue'),
    },
    {
      path: '/cn-nuclei',
      name: 'cn-nuclei',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/cn-nuclei.vue'),
    },
    {
      path: '/attack-agent',
      name: 'attack-agent',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/attack-agent.vue'),
    },
  ],
})

export default router
