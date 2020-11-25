<template>
  <div id="nav">
    <Navbar></Navbar>
  </div>
</template>

<script>
import Navbar from '../components/Navbar.vue';
// import EventService from '@/services/EventService.js';

export default {
  name: 'Brandi',
  components: {
    Navbar
  },
  data() {
    return {
      events: null
    };
  }
  //   created() {
  //     EventService.getEvents()
  //       .then((response) => {
  //         this.events = response.data;
  //       })
  //       .catch((error) => {
  //         console.log(error);
  //       });
  //   }
};
</script>
