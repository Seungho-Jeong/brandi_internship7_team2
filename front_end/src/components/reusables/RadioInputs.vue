<template>
  <div class="radio-selection" :class="name">
    <input
      type="radio"
      :name="name"
      :id="id"
      :checked="checked"
      :value="modelValue"
      @input="setSelectedRadio"
    />
    <label :for="id">{{ label }}</label>
  </div>
</template>

<script>
export default {
  name: 'RadioInputs',
  props: ['name', 'id', 'label', 'checked', 'modelValue'],
  emit: ['update:modelValue'],
  data() {
    return {};
  },
  methods: {
    setSelectedRadio(e) {
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
    font-size: 14px;
    cursor: pointer;
  }
}
</style>
