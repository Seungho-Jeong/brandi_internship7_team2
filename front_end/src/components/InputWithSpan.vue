<template>
  <div class="input-form">
    <div
      class="input-and-icon"
      :class="{
        invalid:
          !input[`${input.id}IsValid`] && input[`${input.id}IsValid`] !== null
      }"
    >
      <i :class="input.iconClass"></i>
      <input
        :value="modelValue"
        @input="updateValue"
        :type="input.type"
        :placeholder="input.placeholder"
        :id="input.id"
      />
    </div>
    <span
      v-if="!input[`${input.id}IsValid`]"
      :class="input.id"
      :id="input.id"
      >{{ input.spanText[input.spanTextOption] }}</span
    >
  </div>
</template>

<script>
export default {
  name: 'InputWithSpan',
  props: ['input', 'modelValue', ''],
  emit: ['update:modelValue'],
  data() {
    return {};
  },
  methods: {
    updateValue(e) {
      console.log(e.target.value);
      this.$emit('update:modelValue', e.target.value);
    }
  }
};
</script>

<style lang="scss" scoped>
.input-form {
  .input-and-icon {
    width: 100%;
    height: 35px;
    border-radius: 3px;
    margin-top: 15px;
    margin-bottom: 5px;
    position: relative;
    border: 1px solid #e5e5e5;

    &.invalid {
      border: 1px solid #a94442;
    }

    .input-and-icon:first-child {
      margin-top: 0;
    }

    i {
      position: absolute;
      left: 0;
      color: red;
      left: 0;
      width: 8%;
      height: 100%;
    }

    input {
      position: absolute;
      width: 92%;
      height: 100%;
      right: 0;

      border: none;

      &::placeholder {
        font-size: 14px;
      }
    }
  }

  span {
    display: block;
    color: #a94442;
    font-size: 13px;
    margin-top: 7px;

    &.managerMobile {
      color: #349afe;
      font-size: 12px;
    }
  }
}
</style>
