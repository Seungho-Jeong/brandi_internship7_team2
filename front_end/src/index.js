import { createApp } from 'vue';
import axios from 'axios';
import App from './App.vue';
import router from './router.js';
import './styles/common.scss';
import './styles/reset.scss';
import {
  Dropdown,
  Button,
  Menu,
  Modal,
  Radio,
  Input,
  Upload
} from 'ant-design-vue';

const app = createApp(App);
app.config.productionTip = false;
axios.defaults.withCredentials = true;
app.use(router);
app.use(Dropdown);
app.use(Button);
app.use(Menu);
app.use(Modal);
app.use(Radio);
app.use(Input);
app.use(Upload);
app.mount('#app');
