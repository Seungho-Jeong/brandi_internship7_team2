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
import { sellers } from '../public/data/SELLERS_API.js';

export default {
  components: {
    Navbar
  },
  data() {
    return {
      sellerData: sellers
    };
  },
  computed: {
    isNavShown() {
      const excludeNavPathsList = ['/login', '/signup'];
      return !excludeNavPathsList.includes(this.$route.path);
    }
  },
  // created() {
  //   const fetchSellerData = async () => {
  //     const SELLERS_API = './config.js';
  //     try {
  //       const res = await fetch(SELLERS_API);
  //       const data = await res;
  //       if (data) {
  //         alert(data.sellers);
  //         this.sellerData = data.sellers;
  //       } else {
  //         alert('server message: FAIL');
  //       }
  //     } catch (err) {
  //       alert('fetch error');
  //     }
  //   };
  //   fetchSellerData();
  // },
  provide() {
    return {
      sellerData: this.sellerData
    };
  }
};
</script>

<style lang="scss">
* {
  font-family: arial, sans-serif;
}
</style>
