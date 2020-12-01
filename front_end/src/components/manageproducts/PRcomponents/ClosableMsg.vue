<template>
  <div>
    <a-alert
      message="Warning Text Warning Text Warning TextW arning Text Warning Text Warning TextWarning Text"
      type="warning"
      closable
      @close="onClose"
    />
    <a-alert
      message="Error Text"
      description="Error Description Error Description Error Description Error Description Error Description Error Description"
      type="error"
      closable
      @close="onClose"
    />
  </div>
</template>
<script>
export default {
  methods: {
    onClose(e) {
      console.log(e, 'I was closed.');
    }
  }
};
</script>
