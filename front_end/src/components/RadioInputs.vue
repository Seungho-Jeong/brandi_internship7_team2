<template>
  <div class="radio-selection" :class="radioObject.name">
    <input
      type="radio"
      :name="radioObject.name"
      :id="category.label"
      :value="modelValue"
      @input="updateValue"
    />
    <label :for="category.label">{{ category.label }}</label>
  </div>
</template>

<script>
export default {
  name: 'RadioInputs',
  props: ['radioObject', 'category', 'modelValue'],
  emit: ['update:modelValue'],
  data() {
    return {};
  },
  methods: {
    updateValue(e) {
      this.$emit('update:modelValue', e.target.value);
    }
  }
};
</script>

<style lang="scss" scoped>
.radio-selection {
  margin-right: 15px;
  cursor: pointer;

  input {
    cursor: pointer;
  }

  label {
    font-size: 14px;
    cursor: pointer;
  }
}
</style>
