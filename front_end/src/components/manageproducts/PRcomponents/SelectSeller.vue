<template>
  <div>
    <a-button type="primary" @click="showModal" @focus="add"> Modal </a-button>
    <a-modal
      v-model="visible"
      title="Modal"
      ok-text="셀러 선택하기"
      cancel-text="닫기"
      @ok="hideModal"
      ref="modal"
    >
      <p>Bla bla ...</p>
      <p>Bla bla ...</p>
      <p>Bla bla ...</p>
    </a-modal>
    <!-- <br />
    <br />
    <a-button @click="confirm"> Confirm </a-button> -->
  </div>
</template>
<script>
export default {
  data() {
    return {
      visible: true
    };
  },
  methods: {
    add() {
      this.$refs.modal.show();
    },
    showModal() {
      this.visible = true;
    },
    hideModal() {
      this.visible = false;
    },
    confirm() {
      this.$confirm({
        title: 'Confirm',
        content: 'Bla bla ...',
        okText: '确认',
        cancelText: '取消'
      });
    }
  }
};
</script>
<style scoped>
a-modal {
  z-index: 100;
}
</style>
