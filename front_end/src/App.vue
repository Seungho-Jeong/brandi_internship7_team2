<template>
  <div class="header">
    <div class="logo">
      <img :src="logo">
      <button />
      <span> staging(staging) </span>
    </div>
    <div class="logout">
      {{ userId }}
    </div>
  </div>

  <div class="sidebar">
    <ul>
      <li v-for="(item, idx) in sidebar"
@click="showSubmenu(idx)">
        {{ item.title }}
        <div :class="{ active: selected && selectedIdx === idx }">
          <li v-for="n in sidebar[idx].submenu.length">
            {{ sidebar[idx].submenu[n - 1] }}
          </li>
        </div>
      </li>
    </ul>
  </div>
</template>

<script lang="js">
export default {
  data(){
    return {
    logo: 'https://sadmin.brandi.co.kr/include/img/logo_2.png',
    userId: 'hahaha',
    sidebar: [
      {title: '홈', submenu: []},
      {title: '주문관리', submenu: ['결제완료관리', '상품준비관리', '배송중관리', '배송완료관리', '구매확정관리']},
      {title: '상품관리', submenu: ['상품 관리', '상품 등록']},
      {title: '회원 관리', submenu: ['셀러 계정 관리']},
    ],
    active: 1,
    selected:false,
    selectedIdx: 1,
    }
  },
  methods : {
    showSubmenu(idx) {
      //아니 뭐가 어려워? 별거 없어
      this.selected === false ? this.selected = true : this.selected = false;
      this.selectedIdx = idx;
      console.log(idx);
      console.log(this.selected);
    },
  }
}
</script>
