<template>
  <main>
    <PageHeading
      class="page-heading"
      heading="셀러정보 수정페이지"
      subHeading="셀러 정보 조회 / 수정"
    />
    <PageBar
      class="page-bar"
      page="account"
      menuLevel1="회원 관리"
      menuLevel2="셀러 계정 관리"
      menuLevel3="셀러 정보 조회 / 수정"
    />
  </main>
</template>
<script>
import PageHeading from '../../components/reusables/PageHeading.vue';
import PageBar from '../../components/reusables/PageBar.vue';

export default {
  name: 'Seller',
  components: {
    PageHeading,
    PageBar
  }
};
</script>

<style lang="scss" scoped>
.page-heading {
  margin: 20px 0 10px 20px;
}
</style>
