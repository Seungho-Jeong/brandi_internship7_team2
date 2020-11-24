import { createApp } from 'vue';
import { createRouter, createWebHashHistory } from 'vue-router';
// import { library } from '@fortawesome/fontawesome-svg-core';
// import { faUserSecret } from '@fortawesome/free-solid-svg-icons';
// import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

import App from './App.vue';
import Login from './pages/Login.vue';
import Signup from './pages/Signup.vue';
import './styles/common.scss';
import './styles/reset.scss';

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/login',
      component: Login
    },
    {
      path: '/signup',
      component: Signup
    }
  ]
});

const app = createApp(App);
app.use(router);
app.mount('#app');
