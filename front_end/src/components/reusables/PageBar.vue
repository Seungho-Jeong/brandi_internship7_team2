<template>
  <div class="page-bar">
    <a-breadcrumb class="page-bar-items" separator="">
      <a-breadcrumb-item class="page-bar-item">
        <home-outlined class="icon" v-if="pagesWithHomeIcon.includes(page)" />
        <unordered-list-outlined
          class="icon"
          v-if="pagesWithListIcon.includes(page)"
        />
        <span>{{ menuLevel1 }}</span>
      </a-breadcrumb-item>
      <a-breadcrumb-separator class="separator">></a-breadcrumb-separator>
      <a-breadcrumb-item class="page-bar-item">{{
        menuLevel2
      }}</a-breadcrumb-item>
      <a-breadcrumb-separator class="separator">></a-breadcrumb-separator>
      <a-breadcrumb-item class="page-bar-item">{{
        menuLevel3
      }}</a-breadcrumb-item>
    </a-breadcrumb>
  </div>
</template>

<script>
import { Breadcrumb } from 'ant-design-vue';
import { HomeOutlined, UnorderedListOutlined } from '@ant-design/icons-vue';

export default {
  name: 'PageBar',
  //*props 정의*//
  //page: 최상위 메뉴(페이지)명 ('account', 'proudct', 'order, etc.)
  //menuLevel1: 상위 메뉴명 ('회원 관리', '상품 관리', '주문 관리', etc.)
  //menuLevel2: 중위 메뉴명 ('셀러 계정 관리', '상품관리 관리', '결제 완료 관리', etc.)
  //menuLevel3: 하위 메뉴명 ('셀러 회원 리스트', '상품 리스트', '결제 완료 리스트', etc.)
  //hasDropdown1: 리스트 filter order dropdown 존재 여부
  //hasDropsdown2: 리스트 filter limit dropwdown 존재 여부
  props: {
    page: String,
    menuLevel1: String,
    menuLevel2: String,
    menuLevel3: String,
    hasDropdown1: Boolean,
    hasDropdown2: Boolean
  },
  components: {
    'a-breadcrumb': Breadcrumb,
    'a-breadcrumb-item': Breadcrumb.Item,
    'a-breadcrumb-separator': Breadcrumb.Separator,
    HomeOutlined,
    UnorderedListOutlined
  },
  data() {
    return {
      pagesWithHomeIcon: ['account'],
      pagesWithListIcon: ['product, order']
    };
  }
};
</script>

<style lang="scss" scoped>
.page-bar {
  min-height: 40px;
  background: #eee;
  display: flex;
  flex-direction: column;
  justify-content: center;

  .page-bar-items {
    padding-left: 20px;

    .page-bar-item {
      font-size: 14px;
      color: #2b2b2b;

      .icon {
        padding-right: 5px;
      }
    }
    .separator {
      color: #9a9a9a;
      padding: 0 5px;
    }
  }
}
</style>
