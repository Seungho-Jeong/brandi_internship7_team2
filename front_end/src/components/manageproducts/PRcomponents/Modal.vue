<template>
  <div>
    <a-button type="primary" @click="showModal">
      Open Modal with customized footer
    </a-button>
    <a-modal v-model="visible" title="셀러 선택" on-ok="handleOk">
      <template v-slot:footer>
        <a-button key="back" @click="handleCancel"> 닫기 </a-button>
        <a-button
          key="submit"
          type="primary"
          :loading="loading"
          @click="handleOk"
        >
          셀러 선택하기
        </a-button>
      </template>
      <a-icon type="info-circle" theme="filled" :style="{ fontSize: '16px', color: '#08c' }"/>
     
      <p>상품을 등록할 셀러를 선택해주세요. (검색 10건)</p>

      <p>셀러 검색</p>
      <p><Select></p>
    </a-modal>
  </div>
</template>
<script>
import { Modal, Button, Icon } from 'ant-design-vue';
export default {
  data() {
    return {
      loading: false,
      visible: false
    };
  },
  methods: {
    showModal() {
      this.visible = true;
    },
    handleOk(e) {
      this.loading = true;
      setTimeout(() => {
        this.visible = false;
        this.loading = false;
      }, 3000);
    },
    handleCancel(e) {
      this.visible = false;
    }
  }
};
</script>