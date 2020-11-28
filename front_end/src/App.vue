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
