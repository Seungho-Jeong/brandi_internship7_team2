import { createRouter, createWebHashHistory } from 'vue-router';

import Login from './pages/Login.vue';
import Signup from './pages/Signup.vue';
import Account from './pages/managemembers/Account.vue';
import Seller from './pages/managemembers/Seller.vue';
import Cproduct from './components/manageproducts/Cproduct.vue';
import ProductRegist from './components/manageproducts/ProductRegistPage.vue';
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
      path: '/seller/seller_my_page/:sellerId',
      component: Seller,
      props: true
    },
    {
      path: '/cproduct',
      component: Cproduct
    },
    {
      path: '/product_regist_page',
      component: ProductRegist
    },
    {
      path: '/test',
      component: ProductRegist
    },
    {
      path: '/order',
      component: Order,
      children: [{ path: ':manage_order_status', component: Order }]
    }
  ]
});

export default router;
