<template>
  <div>
    <a-tag v-model="visible" closable> Movies </a-tag>
    <br />
    <a-button size="small" @click="visible = !visible"> Toggle </a-button>
  </div>
</template>
<script>
export default {
  data() {
    return {
      visible: true
    };
  }
};
</script>

<template>
  <div>
    <template v-for="(tag, index) in tags">
      <a-tooltip v-if="tag.length > 20" :key="tag" :title="tag">
        <a-tag
          :key="tag"
          :closable="index !== 0"
          @close="() => handleClose(tag)"
        >
          {{ `${tag.slice(0, 20)}...` }}
        </a-tag>
      </a-tooltip>
      <a-tag
        v-else
        :key="tag"
        :closable="index !== 0"
        @close="() => handleClose(tag)"
      >
        {{ tag }}
      </a-tag>
    </template>
    <a-input
      v-if="inputVisible"
      ref="input"
      type="text"
      size="small"
      :style="{ width: '78px' }"
      :value="inputValue"
      @change="handleInputChange"
      @blur="handleInputConfirm"
      @keyup.enter="handleInputConfirm"
    />
    <a-tag
      v-else
      style="background: #fff; borderstyle: dashed"
      @click="showInput"
    >
      <a-icon type="plus" /> New Tag
    </a-tag>
  </div>
</template>
<script>
export default {
  data() {
    return {
      tags: ['Unremovable', 'Tag 2', 'Tag 3Tag 3Tag 3Tag 3Tag 3Tag 3Tag 3'],
      inputVisible: false,
      inputValue: ''
    };
  },
  methods: {
    handleClose(removedTag) {
      const tags = this.tags.filter((tag) => tag !== removedTag);
      console.log(tags);
      this.tags = tags;
    },

    showInput() {
      this.inputVisible = true;
      this.$nextTick(function () {
        this.$refs.input.focus();
      });
    },

    handleInputChange(e) {
      this.inputValue = e.target.value;
    },

    handleInputConfirm() {
      const inputValue = this.inputValue;
      let tags = this.tags;
      if (inputValue && tags.indexOf(inputValue) === -1) {
        tags = [...tags, inputValue];
      }
      console.log(tags);
      Object.assign(this, {
        tags,
        inputVisible: false,
        inputValue: ''
      });
    }
  }
};
</script>

<template>
  <div>
    <h4 style="margin-bottom: 16px">Presets:</h4>
    <div>
      <a-tag color="pink"> pink </a-tag>
      <a-tag color="red"> red </a-tag>
      <a-tag color="orange"> orange </a-tag>
      <a-tag color="green"> green </a-tag>
      <a-tag color="cyan"> cyan </a-tag>
      <a-tag color="blue"> blue </a-tag>
      <a-tag color="purple"> purple </a-tag>
    </div>
    <h4 style="margin: '16px 0'">Custom:</h4>
    <div>
      <a-tag color="#f50"> #f50 </a-tag>
      <a-tag color="#2db7f5"> #2db7f5 </a-tag>
      <a-tag color="#87d068"> #87d068 </a-tag>
      <a-tag color="#108ee9"> #108ee9 </a-tag>
    </div>
  </div>
</template>
