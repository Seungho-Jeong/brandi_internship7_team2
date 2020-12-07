<template>
  <main>
    <Navbar v-if="isNavShown" />
    <div v-if="!isNavShown" class="content">
      <router-view></router-view>
    </div>
  </main>
</template>

<script>
import Navbar from './components/Navbar.vue';
// import { seller_list } from '../public/data/SELLERS_API.js';
import { SELLER_LIST } from './config.js';

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
      sellerData: []
    };
  },
  computed: {
    isNavShown() {
      const excludeNavPathsList = ['/login', '/signup'];
      return !excludeNavPathsList.includes(this.$route.path);
    }
  },
  methods: {
    async fetchSellerData() {
      try {
        const res = await fetch(SELLER_LIST, {
          method: 'GET',
          headers: {
            Authorization:
              'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50IjoibWFzdGVyMyIsImV4cCI6MTYwNzQwNTAzNH0.JiooF5kfRHafQdx2jtsw4AT7c0oujD0guyCXdLPmAxA'
          }
        });
        const data = await res.json();
        if (data.message === 'success') {
          alert(data.seller_list);
          this.sellerData = data.seller_list;
          console.log(data.seller_list);
        } else {
          alert('server message: FAIL');
        }
      } catch (err) {
        alert('get error: get request to server failed');
      }
    }
  },
  created() {
    this.fetchSellerData();
  }
};
</script>

<style lang="scss">
* {
  font-family: arial, sans-serif;
}
</style>
