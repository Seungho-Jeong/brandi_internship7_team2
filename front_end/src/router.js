import { createRouter, createWebHistory } from 'vue-router';

import Login from './pages/Login.vue';
import Signup from './pages/Signup.vue';
import Account from './pages/ManageMembers/Account.vue';
import Seller from './pages/ManageMembers/Seller.vue';
import Order from './pages/manageorders/Order.vue';

const router = createRouter({
  history: createWebHistory(),
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
      params: 'seller_my_page/:seller-id',
      component: Seller
    },
    {
      path: '/order',
      component: Order,
      children: [{ path: ':manage_order_status', component: Order }]
    }
  ]
});

export default router;
