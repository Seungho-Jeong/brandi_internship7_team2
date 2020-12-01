<template>
  <div>
    <a-radio-group v-for="(item, idx) in radio"  v-model="value" @change="onChange"  :key="idx">
      <a-radio :value="{idx}">{{item}} </a-radio>
    </a-radio-group>
  </div>
</template>
<script>
export default {
  props: ['radio']
  data() {
    return {
      value: 1
    };
  },
  methods: {
    onChange(e) {
      console.log('radio checked', e.target.value);
    }
  }
};
</script>
