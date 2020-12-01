<template>
  <div>
    <a-button type="primary"> Primary </a-button>
    <a-button>secondary</a-button>
    <a-dropdown>
      <a-menu slot="overlay" @click="handleMenuClick">
        <a-menu-item key="1"> 1st item </a-menu-item>
        <a-menu-item key="2"> 2nd item </a-menu-item>
        <a-menu-item key="3"> 3rd item </a-menu-item>
      </a-menu>
      <a-button> Actions <a-icon type="down" /> </a-button>
    </a-dropdown>
  </div>
</template>
<script>
import { Dropdown, Button, Menu } from 'ant-design-vue';
export default {
  methods: {
    handleMenuClick(e) {
      console.log('click', e);
    }
  }
};
</script>
