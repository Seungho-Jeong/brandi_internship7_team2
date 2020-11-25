<template>
  <!-- <div>
    Brandi Admin Site Project -
    <span>Vue/Webpack Initial Setup<span /></span>
  </div> -->
  <main>
    <router-link :to="{ name: 'Brandi' }">Events</router-link>
    <div>
      <router-view></router-view>
    </div>
  </main>
</template>

<script>
export default {
  data() {
    return {};
  }
};
</script>

<style lang="scss">
* {
  font-family: arial, sans-serif;
}
</style>
