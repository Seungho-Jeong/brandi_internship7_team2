<template>
  <div>
    <a-button type="primary" @click="showModal">
      Open Modal with customized footer
    </a-button>
    <a-modal v-model="visible" title="Title" on-ok="handleOk">
      <template v-slot:footer>
        <a-button key="back" @click="handleCancel"> Return </a-button>
        <a-button
          key="submit"
          type="primary"
          :loading="loading"
          @click="handleOk"
        >
          Submit
        </a-button>
      </template>
      <p>Some contents...</p>
      <p>Some contents...</p>
      <p>Some contents...</p>
      <p>Some contents...</p>
      <p>Some contents...</p>
    </a-modal>
  </div>
</template>
<script>
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

<template>
  <div>
    <a-radio-group v-model="value" @change="onChange">
      <a-radio :value="1"> A </a-radio>
      <a-radio :value="2"> B </a-radio>
      <a-radio :value="3"> C </a-radio>
      <a-radio :value="4"> D </a-radio>
    </a-radio-group>
  </div>
</template>
<script>
export default {
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

<template>
  <div>
    <a-radio :default-checked="false" :disabled="disabled"> Disabled </a-radio>
    <br />
    <a-radio default-checked :disabled="disabled"> Disabled </a-radio>
    <div :style="{ marginTop: 20 }">
      <a-button type="primary" @click="toggleDisabled">
        Toggle disabled
      </a-button>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      disabled: true
    };
  },
  methods: {
    toggleDisabled() {
      this.disabled = !this.disabled;
    }
  }
};
</script>
