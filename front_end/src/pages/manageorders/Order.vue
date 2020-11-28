<template>
  <main>
    <PageHeading :heading="'주문관리'" :subHeading="'결제완료 관리'" />
  </main>
</template>

<script>
import PageHeading from '../../components/reusables/PageHeading.vue';

export default {
  name: 'Order',
  components: {
    PageHeading
  }
};
</script>

<style lang="scss" scoped></style>
