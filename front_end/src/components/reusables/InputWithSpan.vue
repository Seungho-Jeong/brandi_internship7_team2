<template>
  <div class="input-form">
    <div
      tabindex="0"
      class="input-and-icon"
      :class="{
        invalid: !isValid && isValid !== null
      }"
    >
      <div v-if="icon !== undefined" class="icon-div">
        <UserOutlined
          v-if="icon === 'user'"
          class="icon"
          :class="{ invalidicon: !isValid && isValid !== null }"
        />
        <LockOutlined
          v-if="icon === 'lock'"
          class="icon"
          :class="{ invalidicon: !isValid && isValid !== null }"
        />
        <PhoneOutlined
          v-if="icon === 'phone'"
          class="icon"
          :class="{ invalidicon: !isValid && isValid !== null }"
        />
        <CheckOutlined
          v-if="icon === 'check'"
          class="icon"
          :class="{ invalidicon: !isValid && isValid !== null }"
        />
        <FontColorsOutlined
          v-if="icon === 'font'"
          class="icon"
          :class="{ invalidicon: !isValid && isValid !== null }"
        />
        <MailOutlined
          v-if="icon === 'email'"
          class="icon"
          :class="{ invalidicon: !isValid && isValid !== null }"
        />
      </div>
      <input
        class="input-box"
        :class="{ noIcon: icon == undefined }"
        :type="type"
        :placeholder="placeholder"
        :id="id"
        :value="modelValue"
        @input="updateValue"
      />
    </div>
    <span class="span-text" v-if="!isValid" :class="id" :id="id">{{
      spanText
    }}</span>
    <p v-if="explanation">{{ explanation }}</p>
  </div>
</template>

<script>
import {
  UserOutlined,
  LockOutlined,
  PhoneOutlined,
  CheckOutlined,
  FontColorsOutlined,
  MailOutlined
} from '@ant-design/icons-vue';

export default {
  name: 'InputWithSpan',
  props: [
    'id',
    'type',
    'placeholder',
    'spanText',
    'explanation',
    'icon',
    'isValid',
    'modelValue'
  ],
  emit: ['update:modelValue'],
  components: {
    UserOutlined,
    LockOutlined,
    PhoneOutlined,
    CheckOutlined,
    FontColorsOutlined,
    MailOutlined
  },
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
.input-form {
  .input-and-icon {
    width: 100%;
    height: 35px;
    z-index: 1;
    position: relative;
    border: 1px solid #e5e5e5;
    border-radius: 3px;
    transition: border 500ms;

    &:focus-within {
      border: 1px solid #000;
      outline: none;
    }

    &.invalid {
      border: 1px solid #a94442;
    }

    .icon-div {
      z-index: 0;
      position: absolute;
      left: 0;
      width: 8%;
      height: 100%;
      overflow: hidden;
      display: flex;
      justify-content: center;
      align-items: center;
      background: #fff;

      .icon {
        color: #000;
      }

      .invalidicon {
        color: #a94442;
      }
    }

    input {
      z-index: 0;
      position: absolute;
      right: 0;
      width: 92%;
      height: 100%;
      padding-left: 10px;
      border-radius: 3px;
      border: none;
    }

    .noIcon {
      width: 100%;
    }
  }

  .span-text {
    display: block;
    color: #a94442;
    font-size: 13px;
    margin-top: 7px;
  }

  p {
    color: #349afe;
    font-size: 12px;
    margin-top: 7px;
  }
}
</style>
