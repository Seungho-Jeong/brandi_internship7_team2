<template>
  <div>
    <PageHeading heading="상품 등록" subHeading="상품 정보 등록"></PageHeading>

    <PageBar
      class="page-bar"
      page="order"
      menuLevel1="상품관리"
      menuLevel2="상품 관리"
      menuLevel3="상품 등록"
    ></PageBar>

    <InfoBasic></InfoBasic>
    <InfoTagger></InfoTagger>
    <InfoOpt></InfoOpt>
    <InfoSell></InfoSell>
    <InfoRet></InfoRet>
    <InfoCodi></InfoCodi>
  </div>
</template>

<script>
import PageHeading from '../reusables/PageHeading.vue';
import PageBar from '../reusables/PageBar.vue';
import InfoBasic from './InfoBasic.vue';
// import InfoTagger from './InfoTagger.vue';
// import InfoOpt from './InfoOpt.vue';
// import InfoSell from './InfoSell.vue';
// import InfoRet from './InfoRet.vue';
// import InfoCodi from './InfoCodi.vue';

export default {
  name: 'ProductRegist',
  components: {
    PageHeading,
    PageBar,
    InfoBasic
  },
  data() {
    return {
      table: [{ a: 12134, b: 24143141 }],
      table2: [2, 5, 6, 23, 213123],
      table3: {
        akaka: 13421244,
        ekfkdk: 355,
        adfasfd: 32940923
      }
    };
  }
};
</script>
