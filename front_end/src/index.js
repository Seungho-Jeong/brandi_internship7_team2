import { createApp } from 'vue';
import { createRouter, createWebHashHistory } from 'vue-router';
// import { library } from '@fortawesome/fontawesome-svg-core';
// import { faUserSecret } from '@fortawesome/free-solid-svg-icons';
// import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

import App from './App.vue';
import Login from './pages/Login.vue';
import Signup from './pages/Signup.vue';
import Brandi from './pages/Brandi.vue';
import './styles/common.scss';
import './styles/reset.scss';

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes: [
    {
      path: '/login',
      component: Login
    },
    {
      path: '/signup',
      component: Signup
    },
    {
      path: '/brandi/:id',
      component: Brandi,
      name: 'Brandi',
      props: true
    }
  ]
});

const app = createApp(App);
app.use(router);
app.mount('#app');
