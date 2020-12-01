<template>
  <PageHeading></PageHeading>

  <PageBar></PageBar>

  <InfoBasic></InfoBasic>
  <InfoTagger></InfoTagger>
  <InfoOpt></InfoOpt>
  <InfoSell></InfoSell>
  <InfoRet></InfoRet>
  <InfoCodi></InfoCodi>
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
  props: ['heading', 'subHeading'],
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
