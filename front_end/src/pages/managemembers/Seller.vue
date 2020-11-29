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
    <PageSection icon="user" sectionTitle="기본 정보">
      <div>HELLO</div>
    </PageSection>
    <PageSection icon="user" sectionTitle="상세 정보">
      <div>HELLO</div>
    </PageSection>
    <PageSection icon="user" sectionTitle="수수료">
      <div>HELLO</div>
    </PageSection>
    <PageSection icon="user" sectionTitle="배송정보 및 교환/환불 정보">
      <div>HELLO</div>
    </PageSection>
  </main>
</template>
<script>
import PageHeading from '../../components/reusables/PageHeading.vue';
import PageBar from '../../components/reusables/PageBar.vue';
import PageSection from '../../components/reusables/PageSection.vue';

export default {
  name: 'Seller',
  components: {
    PageHeading,
    PageBar,
    PageSection
  }
};
</script>

<style lang="scss" scoped>
.page-heading {
  margin: 20px 0 10px 20px;
}
</style>
