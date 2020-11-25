import { createRouter, createWebHashHistory } from 'vue-router';

import Login from './pages/Login.vue';
import Signup from './pages/Signup.vue';
import Account from './pages/ManageMembers/Account.vue';
import Seller from './pages/ManageMembers/Seller.vue';
import Order from './pages/manageorders/Order.vue';

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      component: Login
    },
    {
      path: '/signup',
      component: Signup
    },
    {
      path: '/account',
      component: Account
    },
    {
      path: '/seller',
      component: Seller
    },
    {
      path: '/order',
      component: Order,
      children: [{ path: ':manageOrderStatus', component: Order }]
    }
  ]
});

export default router;
