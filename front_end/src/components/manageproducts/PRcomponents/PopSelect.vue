<template>
  <a-popconfirm title="Are you sure？" ok-text="Yes" cancel-text="No">
    <a href="#">Delete</a>
  </a-popconfirm>
</template>

<template>
  <div>
    <a-popover title="Title" trigger="hover">
      <template slot="content">
        <p>Content</p>
        <p>Content</p>
      </template>
      <a-button type="primary"> Hover me </a-button>
    </a-popover>
    <a-popover title="Title" trigger="focus">
      <template slot="content">
        <p>Content</p>
        <p>Content</p>
      </template>
      <a-button type="primary"> Focus me </a-button>
    </a-popover>
    <a-popover title="Title" trigger="click">
      <template slot="content">
        <p>Content</p>
        <p>Content</p>
      </template>
      <a-button type="primary"> Click me </a-button>
    </a-popover>
  </div>
</template>
