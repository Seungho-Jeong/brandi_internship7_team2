<template>
  <div class="section-container">
    <div class="section-title">
      <unordered-list-outlined v-if="icon === 'list'" class="icon" />
      <user-outlined v-if="icon === 'user'" class="icon" />
      <h3>{{ sectionTitle }}</h3>
    </div>
    <div class="section-slot">
      <slot></slot>
    </div>
  </div>
</template>

<script>
import { UnorderedListOutlined, UserOutlined } from '@ant-design/icons-vue';

export default {
  name: 'PageSection',
  components: {
    UnorderedListOutlined,
    UserOutlined
  },
  props: ['icon', 'sectionTitle']
};
</script>

<style lang="scss" scoped>
.section-container {
  margin: 10px 20px 10px 20px;
  border-radius: 5px;
  border: 1px solid #ddd;

  .section-title {
    min-height: 40px;
    background: #eee;
    display: flex;
    align-items: center;

    .icon {
      color: #666;
      padding: 0 5px 0 10px;
    }

    h3 {
      font-size: 16px;
      font-weight: 400;
      color: #333;
    }
  }

  .section-slot {
    margin: 10px;
  }
}
</style>
