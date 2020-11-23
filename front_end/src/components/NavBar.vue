<template>
  <div class="header">
    <div>
      <img :src="logo">
      staging(staging)
    </div>
    <div>
      {{ userId }}
    </div>
  </div>

  <div class="sidebar">
    <ul>
      <li v-for="item in sidebar">
        {{ item.title }}
        <!-- <ul>
              <li v-for="item in sidebar">{{item.list}}</li>
          </ul> -->
      </li>
    </ul>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import './NavBar.scss';
export default {
  name: 'NavBar',
  setup() {
    const logo = ref('src/assets/logo_2.png');

    const userId = ref('hahaha');
    const sidebar = ref([
      { title: '주문관리' },
      { title: '상품관리' },
      { title: '회원 관리' },
      { title: '홈' },
      { title: '' }
    ]);
  }
};
</script>
