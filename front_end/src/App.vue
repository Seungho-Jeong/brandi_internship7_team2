<template>
  <main>
    <router-view v-if="!isNavShown"></router-view>
    <Navbar v-if="isNavShown">
      <router-view></router-view>
    </Navbar>
  </main>
</template>

<script>
import Navbar from './components/Navbar.vue';
import { seller_list } from '../public/data/SELLERS_API.js';
// import { SELLER_LIST } from './config.js';

export default {
  provide() {
    return {
      sellerData: this.sellerData
    };
  },
  components: {
    Navbar
  },
  data() {
    return {
      sellerData: {
        sellerList: seller_list
      }
    };
  },
  computed: {
    isNavShown() {
      const excludeNavPathsList = ['/login', '/signup'];
      return !excludeNavPathsList.includes(this.$route.path);
    }
  }
  // methods: {
  //   async fetchSellerData() {
  //     try {
  //       const res = await fetch(SELLER_LIST, {
  //         method: 'GET',
  //         headers: {
  //           Authorization:
  //             'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50IjoibWFzdGVyMyIsImV4cCI6MTYwNzQwNTAzNH0.JiooF5kfRHafQdx2jtsw4AT7c0oujD0guyCXdLPmAxA'
  //         }
  //       });
  //       const data = await res.json();
  //       if (data.message === 'success') {
  //         this.sellerData.sellerList = data.seller_list;
  //         console.log(data.seller_list);
  //       } else {
  //         alert('server message: FAIL');
  //       }
  //     } catch (err) {
  //       alert('get error: get request to server failed');
  //     }
  //   }
  // },
  // mounted() {
  //   this.fetchSellerData();
  // },
  // beforeUpdate() {
  //   console.log(this.sellerData.sellerList);
  // }
};
</script>

<style lang="scss">
* {
  font-family: arial, sans-serif;
}
</style>
