/* eslint-disable vue/require-v-for-key */

<template>
  <div>
    <div class="header">
      <div class="logo">
        <img :src="logo" />
        <span> staging (staging) </span>
      </div>
      <div class="logout" @mouseover="showLogout()">
        {{ userId }}
      </div>
    </div>

    <div class="sidebar" :class="{ narrow: isSidebarNarrow }">
      <div class="button" @click="narrowSidebar">
        <left-outlined v-if="!isSidebarNarrow" class="buttonIcon" />
        <right-outlined v-if="isSidebarNarrow" class="buttonIcon" />
      </div>
      <ul>
        <li
          class="menu"
          v-for="(item, idx) in sidebar"
          @click="showSubmenu(idx)"
          :key="item.title"
        >
          {{ !isSidebarNarrow ? item.title : '' }}
          <div :class="{ active: selected && selectedIdx === idx }">
            <router-link
              v-for="n in sidebar[idx].submenu.length"
              class="event-link"
              :to="sidebar[idx].submenu[n - 1].path"
              :key="n"
            >
              <li class="submenu">
                {{ sidebar[idx].submenu[n - 1].name }}
              </li>
            </router-link>
          </div>
        </li>
      </ul>
    </div>

    <div class="content" :class="{ wide: isSidebarNarrow }">
      <router-view />
    </div>
  </div>
</template>

<script lang="js">
import {LeftOutlined, RightOutlined} from '@ant-design/icons-vue';

export default {
  components: {
    LeftOutlined,
    RightOutlined
  },
  data(){
    return {
    logo: 'https://sadmin.brandi.co.kr/include/img/logo_2.png',
    userId: 'intern_master',
    sidebar: [
      {title: '홈', submenu: []},
      {title: '주문관리', submenu: [{name: '결제완료관리', path: '/order'}, {name: '상품준비관리', path: '/order'}, {name: '배송중관리', path: '/order'}, {name: '배송완료관리', path: '/order'}, {name: '구매확정관리', path: '/order'}]},
      {title: '상품관리', submenu: [{name: '상품 관리', path: '/cproduct'}, {name: '상품 등록', path: '/product_regist_page'}]},
      {title: '회원 관리', submenu: [{name: '셀러 계정 관리', path: '/account'}]},
    ],
    active: 1,
    selected:false,
    selectedIdx: 1,
    sidebarButton: false,
    isSidebarNarrow: false,
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
      this.isSidebarNarrow = !this.isSidebarNarrow;
      // !this.sidebarButton;
    },
    showLogout(){
    }
  }
}
</script>

<style lang="scss" scoped>
.header {
  z-index: 10;
  position: fixed;
  top: 0;
  left: 0;
  background-color: #873b53;
  width: 100vw;
  height: 45px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
  div.logo {
    margin-left: 20px;
    display: flex;
    align-items: center;

    img {
      width: 100px;
      height: 21.47px;
    }

    span {
      font-size: 13px;
      font-weight: 200;
      margin-left: 30px;
    }
  }

  div.logout {
    width: 130px;
    font-size: 13px;
    color: #cecfd3;
  }
}
.sidebar {
  position: fixed;
  top: 45px;
  left: 0;
  width: 215px;
  height: 100vh;
  background-color: #35363a;

  .button {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 22px;
    height: 22px;
    border-radius: 3px 0 0 3px;
    background: white;
    position: absolute;
    top: 20px;
    right: 0%;
    cursor: pointer;
  }

  ul {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    position: absolute;
    top: 60px;
    padding: 0;
    li {
      display: block;
      list-style-type: none;
      width: 215px;
      min-height: 40px;
      color: #eee;
      font-size: 14px;
      padding-top: 10px;
      padding-left: 40px;
      cursor: pointer;

      &:not(:last-child) {
        border-bottom: 1px solid grey;
      }

      div {
        margin-top: 10px;
        margin-bottom: 10px;
        display: none;

        .submenu {
          min-height: 30px;
          font-size: 13px;
          padding-left: 10px;
        }
      }
      .active {
        display: block;
      }
    }
  }
}
.sidebar.narrow {
  width: 40px;
  overflow: hidden;

  ul {
    li {
      border: none;
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

.content.wide {
  width: calc(100vw - 40px);
}
</style>
