<template>
  <h2 class="heading">
    {{ heading }}
    <span>{{ subHeading }}</span>
  </h2>
</template>

<script>
export default {
  name: 'PageHeading',
  props: ['heading', 'subHeading']
};
</script>

<style lang="scss" scoped>
.heading {
  margin: 25px 20px 15px 20px;
  font-size: 25px;
  font-weight: 400;
  color: #666666;

  span {
    font-size: 14px;
    color: #888888;
  }
}
</style>
