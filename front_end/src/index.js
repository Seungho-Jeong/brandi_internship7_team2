import { createApp } from 'vue';

import App from './App.vue';
import router from './router.js';
import './styles/common.scss';
import './styles/reset.scss';

const app = createApp(App);
app.use(router);
app.mount('#app');
