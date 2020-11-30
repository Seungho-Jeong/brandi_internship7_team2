<template>
  <div class="radio-selection" :class="radioObject.name">
    <input
      type="radio"
      :name="radioObject.name"
      :id="category.categoryId"
      :value="modelValue"
      @input="setSelectedRadio"
    />
    <label :for="category.categoryId">{{ category.label }}</label>
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
    setSelectedRadio(e) {
      console.log(e.target.id);
      this.$emit('update:modelValue', e.target.id);
    }
  }
};
</script>

<style lang="scss" scoped>
.radio-selection {
  margin-right: 15px;
  cursor: pointer;

  input {
    margin-right: 5px;
    cursor: pointer;
  }

  label {
    font-size: 15px;
    cursor: pointer;
  }
}
</style>
