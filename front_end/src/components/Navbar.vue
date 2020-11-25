/* eslint-disable vue/require-v-for-key */

<template>
  <div>
    <div class="header">
      <div class="logo">
        <img :src="logo" />
        <button />
        <span> staging(staging) </span>
      </div>
      <div class="logout" @mouseover="showLogout()">
        {{ userId }}
      </div>
    </div>

    <div class="sidebar">
      <div class="button">
        <button @click="narrowSidebar()">button</button>
      </div>
      <ul>
        <li v-for="(item, idx) in sidebar" @click="showSubmenu(idx)">
          {{ item.title }}
          <div :class="{ active: selected && selectedIdx === idx }">
            <router-link
              v-for="n in sidebar[idx].submenu.length"
              class="event-link"
              to="signup"
            >
              <li class="submenu">
                {{ sidebar[idx].submenu[n - 1] }}
              </li>
            </router-link>
          </div>
        </li>
      </ul>
    </div>

    <div class="content">
      <router-view />
      content goes here
    </div>
  </div>
</template>

<script lang="js">
// import './Navbar.scss'
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
    sidebarButton: false,
    }
  },
  methods : {
    showSubmenu(idx) {
      this.selected === false ? this.selected = true : this.selected = false;
      this.selectedIdx = idx;
      console.log(idx);
      console.log(this.selected);
    },
    narrowSidebar(){
      this.sidebarButton === false ? this.sidebarButton = true : this.sidebarButton = false;
    },
    showLogout(){
    }
  }
}
</script>

<style lang="scss" scoped>
body {
  margin: 0;
}

.header {
  z-index: 10;
  position: fixed;
  top: 0;
  background-color: #873b53;
  width: 100vw;
  height: 45px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
  div.logo {
    img {
      width: 100px;
      height: 21.47px;
    }
  }

  div.logout {
    width: 100px;
    height: 45px;

    color: #cecfd3;
  }
}
.sidebar {
  /* position: relative; */
  position: fixed;
  top: 45px;
  left: 0;
  width: 215px;
  height: 100vh;
  background-color: #35363a;

  .button {
    height: 20px;
    width: auto;
    display: flex;
    justify-content: flex-end;
    button {
      position: relative;
      top: 20px;
      right: 0;
      width: 10px;
      height: 10px;
    }
  }
  ul {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    margin-top: 20px;
    padding: 0;
    li {
      display: block;
      list-style-type: none;
      width: 215px;
      min-height: 40px;
      color: #eee;
      border: 1px solid white;

      div {
        margin-top: 20px;
        display: none;
        .submenu {
          text-indent: 8px;
        }
      }
      .active {
        display: block;
      }
    }
  }
}

.content {
  width: calc(100vw - 215px);
  height: calc(100vh - 45px);
  overflow-x: hidden;
  overflow-y: scroll;
  position: fixed;
  bottom: 0;
  right: 0;
}
</style>
