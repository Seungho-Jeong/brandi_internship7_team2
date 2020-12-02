<template>
  <table>
    <thead>
      {{
        thead
      }}
    </thead>

    <tbody>
      <tr>
        <th><{{ tbody.th }}</th>
        <td><ModalSeller></td>
      </tr>
      <tr>
        <th><{{ tbody.th }}</th>
        <td><Radio </td>
      </tr>
      <tr>
        <th><{{ tbody.th }}</th>
        <td></td>
      </tr>
      <tr>
        <th><{{ tbody.th }}</th>
        <td></td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import Modal from './PRcomponents/Modal.vue';
['thead', 'tbody'];

export default {
  data() {
    return {};
  }
};
</script>
