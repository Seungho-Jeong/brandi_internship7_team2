<template>
  <main>
    <Navbar v-if="isNavShown" />
    <router-view></router-view>
  </main>
</template>

<script>
import Navbar from './components/Navbar.vue';

export default {
  components: {
    Navbar
  },
  computed: {
    isNavShown() {
      const excludeNavPathsList = ['/login', '/signup'];
      return !excludeNavPathsList.includes(this.$route.path);
    }
  }
};
</script>

<style lang="scss">
* {
  font-family: arial, sans-serif;
}
</style>
