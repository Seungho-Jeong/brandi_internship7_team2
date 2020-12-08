<template>
  <div>
    <PageHeading
      class="page-heading"
      heading="셀러정보 수정페이지"
      subHeading="셀러 정보 조회 / 수정"
    />
    <PageBar
      class="page-bar"
      page="account"
      menuLevel1="회원 관리"
      menuLevel2="셀러 계정 관리"
      menuLevel3="셀러 정보 조회 / 수정"
    />
    <PageSection icon="user" sectionTitle="기본 정보">
      <table>
        <tbody>
          <tr>
            <th>셀러 프로필</th>
            <td>
              <a-upload
                v-model="profileImgList"
                name="avatar"
                list-type="picture-card"
                class="avatar-uploader seller-profile"
                :show-upload-list="false"
                :action="SELLER_FILEUPLOAD"
                :before-upload="beforeUploadProfile"
                @change="handleChangeProfile"
                ref="aUploadProfile"
              >
                <img
                  class="uploaded-image"
                  v-if="profileImageUrl"
                  :src="profileImageUrl"
                  alt="seller profile"
                />
                <div v-else>
                  <!-- todo -->
                  <loading-outlined v-if="profileLoading" />
                  <plus-outlined v-else />
                  <div class="ant-upload-text">Upload</div>
                </div>
              </a-upload>
              <div
                v-if="profileImageUrl"
                class="dual-buttons upload-img-buttons"
              >
                <button
                  class="change"
                  type="button"
                  @click="changeImage('profile')"
                >
                  변경
                </button>
                <button
                  class="delete"
                  type="button"
                  @click="deleteImage('profile')"
                >
                  삭제
                </button>
              </div>
              <p class="explanation">
                {{
                  `\u24D8 셀러 프로필 확장자는 jpg, jpeg, png 만 가능하며, 허용 가능한
                최대 파일사이즈 크기는 5MB 입니다.`
                }}
              </p>
            </td>
          </tr>
          <tr>
            <th>셀러 상태</th>
            <td>{{ shop_status }}</td>
          </tr>
          <tr>
            <th>셀러 속성</th>
            <td class="seller-categories">
              <RadioInputs
                class="radio"
                v-for="category in sellerCategoriesByType[category_type_id]"
                :key="category.categoryId"
                :id="category.categoryId"
                :name="sellerCategoriesByType.name"
                :label="category.label"
                :value="category.categoryId"
                :checked="category.categoryId === category_id"
                v-model="sellerCategoriesByType.selectedCategory"
                @update:modelValue="setSelectedCategory()"
              />
            </td>
          </tr>
          <tr>
            <td class="explanation" colspan="2">
              {{
                `\u24D8 셀러명(한글, 영문) 변경시 셀러명과 동일하게 등록된 브랜드 정보는
              자동으로 변경되지 않습니다. 관리자께서는 이점 유의해주시기 바라며,
              브랜드 정보 수정은 [이전 버전 관리 > 브랜드관리] 에서 가능합니다.`
              }}
            </td>
          </tr>
          <tr>
            <th>셀러 한글명</th>
            <td>{{ seller_name_ko }}</td>
          </tr>
          <tr>
            <th>셀러 영문명</th>
            <td>{{ seller_name_en }}</td>
          </tr>
          <tr>
            <th>셀러 계정</th>
            <td>{{ account }}</td>
          </tr>
        </tbody>
      </table>
    </PageSection>
    <PageSection icon="user" sectionTitle="상세 정보">
      <table>
        <tbody>
          <tr>
            <th>셀러페이지 배경이미지</th>
            <td>
              <a-upload
                v-model="backgroundImgList"
                name="avatar"
                list-type="picture-card"
                class="avatar-uploader seller-background"
                :show-upload-list="false"
                :action="SELLER_FILEUPLOAD"
                :before-upload="beforeUploadBackground"
                @change="handleChangeBackground"
                ref="aUploadBackground"
              >
                <img
                  class="uploaded-image"
                  v-if="backgroundImageUrl"
                  :src="backgroundImageUrl"
                  alt="seller background"
                />
                <div v-else>
                  <!-- todo -->
                  <loading-outlined v-if="backgroundLoading" />
                  <plus-outlined v-else />
                  <div class="ant-upload-text">Upload</div>
                </div>
              </a-upload>
              <div
                v-if="backgroundImageUrl"
                class="dual-buttons upload-img-buttons"
              >
                <button
                  class="change"
                  type="button"
                  @click="changeImage('background')"
                >
                  변경
                </button>
                <button
                  class="delete"
                  type="button"
                  @click="deleteImage('background')"
                >
                  삭제
                </button>
              </div>
              <p class="explanation">
                {{
                  `\u24D8 브랜디 앱과 웹 사이트의 셀러 페이지에 보여질
                배경이미지입니다.`
                }}
              </p>
              <p class="explanation">
                {{
                  `\u24D8 배경이미지는
                1200 * 850 사이즈 이상으로 등록해주세요.`
                }}
              </p>
              <p class="explanation">
                {{
                  `\u24D8 확장자는 jpg, jpeg, png 만 가능하며,
                허용 가능한 최대 파일사이즈 크기는 5MB 입니다.`
                }}
              </p>
            </td>
          </tr>
          <tr>
            <th>셀러 한줄소개</th>
            <td>
              <InputWithSpan
                class="input short-introduction"
                id="short_introduction"
                type="text"
                placeholder="셀러 한줄 소개"
                icon="user"
                :isValid="short_introduction.isValid"
                v-model.trim="short_introduction.value"
                @update:modelValue="validateInputs('short_introduction')"
              />
            </td>
          </tr>
          <tr>
            <th>셀러 상세소개</th>
            <td>
              <textarea
                class="textarea long-introduction"
                id="long_introduction"
                placeholder="셀러 상세 소개"
                :isValid="long_introduction.isValid"
                v-model.trim="long_introduction.value"
              />
              <p class="explanation">
                {{ `\u24D8 셀러 상세 소개 글은 최소10자 이상 입니다.` }}
              </p>
            </td>
          </tr>
          <tr>
            <th>담당자 정보</th>
            <td>
              <div class="manager-info">
                <div class="manager-inputs">
                  <InputWithSpan
                    class="input manager"
                    id="manager1_name"
                    type="text"
                    placeholder="담당자명"
                    icon="user"
                    :isValid="manager_input_isValid"
                    v-model.trim="managers[0].manager_name"
                    @update:modelValue="validateInputs('manager')"
                  />
                  <InputWithSpan
                    class="input manager"
                    id="manager1_mobile"
                    type="text"
                    placeholder="담당자 핸드폰번호"
                    icon="phone"
                    :isValid="manager_input_isValid"
                    v-model.trim="managers[0].manager_mobile"
                    @update:modelValue="validateInputs('manager')"
                  />
                  <InputWithSpan
                    class="input manager"
                    id="manager1_email"
                    type="text"
                    placeholder="담당자 이메일"
                    icon="email"
                    :isValid="manager_input_isValid"
                    v-model.trim="managers[0].manager_email"
                    @update:modelValue="validateInputs('manager')"
                  />
                </div>
                <div class="manager-buttons">
                  <button class="button plus" @click="addManager(2)">
                    <PlusOutlined class="button-icon" />
                  </button>
                </div>
              </div>
              <div v-if="managers[1].manager_id" class="divider top"></div>
              <div v-if="managers[1].manager_id" class="divider bottom"></div>
              <div v-if="managers[1].manager_id" class="manager-info">
                <div class="manager-inputs">
                  <InputWithSpan
                    class="input manager"
                    id="manager2_name"
                    type="text"
                    placeholder="담당자명2"
                    icon="user"
                    :isValid="manager_input_isValid"
                    v-model.trim="managers[1].manager_name"
                    @update:modelValue="validateInputs('manager')"
                  />
                  <InputWithSpan
                    class="input manager"
                    id="manager2_mobile"
                    type="text"
                    placeholder="담당자 핸드폰번호2"
                    icon="phone"
                    :isValid="manager_input_isValid"
                    v-model.trim="managers[1].manager_mobile"
                    @update:modelValue="validateInputs('manager')"
                  />
                  <InputWithSpan
                    class="input manager"
                    id="manager2_email"
                    type="text"
                    placeholder="담당자 이메일2"
                    icon="email"
                    :isValid="manager_input_isValid"
                    v-model.trim="managers[1].manager_email"
                    @update:modelValue="validateInputs('manager')"
                  />
                </div>
                <div class="manager-buttons">
                  <button class="button plus" @click="addManager(3)">
                    <PlusOutlined class="button-icon" />
                  </button>
                  <button class="button minus" @click="hideManager(2)">
                    <MinusOutlined class="button-icon" />
                  </button>
                </div>
              </div>
              <div v-if="managers[2].manager_id" class="divider top"></div>
              <div v-if="managers[2].manager_id" class="divider bottom"></div>
              <div v-if="managers[2].manager_id !== null" class="manager-info">
                <div class="manager-inputs">
                  <InputWithSpan
                    class="input manager"
                    id="manager3_name"
                    type="text"
                    placeholder="담당자명3"
                    icon="user"
                    :isValid="manager_input_isValid"
                    v-model.trim="managers[2].manager_name"
                    @update:modelValue="validateInputs('manager')"
                  />
                  <InputWithSpan
                    class="input manager"
                    id="manager3_mobile"
                    type="text"
                    placeholder="담당자 핸드폰번호3"
                    icon="phone"
                    :isValid="manager_input_isValid"
                    v-model.trim="managers[2].manager_mobile"
                    @update:modelValue="validateInputs('manager')"
                  />
                  <InputWithSpan
                    class="input manager"
                    id="manager3_email"
                    type="text"
                    placeholder="담당자 이메일3"
                    icon="email"
                    :isValid="manager_input_isValid"
                    v-model.trim="managers[2].manager_email"
                    @update:modelValue="validateInputs('manager')"
                  />
                </div>
                <div class="manager-buttons">
                  <button class="button minus" @click="hideManager(3)">
                    <MinusOutlined class="button-icon" />
                  </button>
                  <p class="explanation manager-limit">
                    {{ `\u24D8 담당자는 최대 3명까지 등록 가능합니다.` }}
                  </p>
                </div>
              </div>
            </td>
          </tr>
          <tr>
            <th>고객센터</th>
            <td>
              <InputWithSpan
                class="input cs-contact"
                id="cs_contact"
                type="text"
                placeholder="고객센터 전화번호"
                icon="phone"
                :isValid="cs_contact.isValid"
                v-model.trim="cs_contact.value"
                @update:modelValue="validateInputs('cs_contact')"
              />
            </td>
          </tr>
          <tr>
            <th>고객센터 운영시간 (주중)</th>
            <td class="cs-hours">
              <a-time-picker
                :value="cs_opening_time"
                format="hh:mm a"
                @change="updateCsOpeningTime"
              />
              <div class="time-connector">~</div>
              <a-time-picker
                :value="cs_closing_time"
                format="hh:mm a"
                @change="updateCsClosingTime"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </PageSection>
    <PageSection icon="user" sectionTitle="수수료">
      <div class="container"></div>
    </PageSection>
    <PageSection icon="user" sectionTitle="배송정보 및 교환/환불 정보">
      <table>
        <tbody>
          <tr>
            <th>배송 정보</th>
            <td>
              <textarea
                class="textarea delivery-info"
                id="delivery_info"
                :placeholder="`ex)\n도서산간 지역은 배송비가 추가비용이 발생할 수 있습니다.\n결제 완료 후 1~3일 후 출고됩니다.`"
                :isValid="delivery_information.isValid"
                v-model.trim="delivery_information.value"
              />
              <p class="explanation">
                {{ `\u24D8 문장이 끝나면 엔터로 줄바꿈을 해주세요.` }}
              </p>
            </td>
          </tr>
          <tr>
            <th>교환/환불 정보</th>
            <td>
              <textarea
                class="textarea exchange-refund-info"
                id="exchange_refund_info"
                :placeholder="`ex)\n브랜디는 소비자보호법 및 전자상거래법을 기반한 환불보장제를 운영 중에 있습니다.\n정당하지 않은 사유로 인한 환불 거부 등은 제재 사유가 될 수 있는 점 참고 부탁드립니다.`"
                :isValid="exchange_refund_information.isValid"
                v-model.trim="exchange_refund_information.value"
              />
              <p class="explanation">
                {{ `\u24D8 문장이 끝나면 엔터로 줄바꿈을 해주세요.` }}
              </p>
            </td>
          </tr>
        </tbody>
      </table>
    </PageSection>
    <div class="dual-buttons submit-buttons">
      <button
        class="submit"
        :class="{ disabled: shop_status_id === 1 }"
        type="button"
        :disabled="shop_status_id === 1"
        @click="requestEdit"
      >
        수정
      </button>
      <button class="cancel" type="button" @click="cancelEdit">취소</button>
    </div>
  </div>
</template>

<script>
import PageHeading from '../../components/reusables/PageHeading.vue';
import PageBar from '../../components/reusables/PageBar.vue';
import PageSection from '../../components/reusables/PageSection.vue';
import InputWithSpan from '../../components/reusables/InputWithSpan.vue';
import RadioInputs from '../../components/reusables/RadioInputs.vue';
import { seller_info } from '../../../public/data/USER_API.js';
import {
  SELLER_INFO,
  SELLER_FILEUPLOAD,
  SELLER_FILEUPLOAD_TEST
} from '../../config.js';

// const PageHeading = () => import('../../components/reusables/PageHeading.vue');
// const PageBar = () => import('../../components/reusables/PageBar.vue');
// const PageSection = () => import('../../components/reusables/PageSection.vue');
// const InputWithSpan = () =>
//   import('../../components/reusables/InputWithSpan.vue');

import moment from 'moment';
import { Upload, TimePicker } from 'ant-design-vue';
import {
  PlusOutlined,
  LoadingOutlined,
  MinusOutlined
} from '@ant-design/icons-vue';
import 'ant-design-vue/dist/antd.less';
import { message } from 'ant-design-vue';
function getBase64(img, callback) {
  const reader = new FileReader();
  reader.addEventListener('load', () => callback(reader.result));
  reader.readAsDataURL(img);
}

export default {
  name: 'Seller',
  inject: ['sellerData'],
  props: ['sellerId'],
  components: {
    'a-upload': Upload,
    'a-time-picker': TimePicker,
    PlusOutlined,
    LoadingOutlined,
    MinusOutlined,
    PageHeading,
    PageBar,
    PageSection,
    InputWithSpan,
    RadioInputs
  },
  data() {
    return {
      SELLER_INFO,
      SELLER_FILEUPLOAD,
      SELLER_FILEUPLOAD_TEST,
      is_master: this.sellerData.is_master,
      id: '',
      seller_id: '',
      account: '',
      seller_name_en: '',
      seller_name_ko: '',
      shop_status: '',
      shop_status_id: '',
      category: '',
      category_id: 6,
      category_type_id: 2,
      created_at: '',
      //이미지 업로드 컴포넌트
      profileImgList: [],
      backgroundImgList: [],
      profileLoading: false,
      profileImageUrl: '',
      backgroundLoading: false,
      backgroundImageUrl: '',
      //셀러소개
      short_introduction: {
        value: '',
        isValid: true
      },
      long_introduction: {
        value: '',
        isValid: true
      },
      //담당자 정보
      managers: [
        {
          manager_id: null,
          manager_email: '',
          manager_mobile: '',
          manager_name: '',
          isValid: true
        },
        {
          manager_id: null,
          manager_email: '',
          manager_mobile: '',
          manager_name: '',
          isValid: true
        },
        {
          manager_id: null,
          manager_email: '',
          manager_mobile: '',
          manager_name: '',
          isValid: true
        }
      ],
      manager_input_isValid: true,
      //고객센터
      cs_contact: {
        value: '',
        isValid: true
      },
      cs_opening_time: '',
      cs_closing_time: '',
      //배송/환불
      delivery_information: {
        value: '',
        isValid: true
      },
      exchange_refund_information: {
        value: '',
        isValid: true
      },
      //for radio input render (radioObject)
      sellerCategoriesByType: {
        name: 'sellerCategory',
        selectedCategory: null,
        1: [
          { categoryId: 1, label: '쇼핑몰' },
          { categoryId: 2, label: '마켓' },
          { categoryId: 3, label: '로드샵' }
        ],
        2: [
          { categoryId: 4, label: '디자이너브랜드' },
          { categoryId: 5, label: '제너럴브랜드' },
          { categoryId: 6, label: '내셔널브랜드' }
        ],
        3: [{ categoryId: 7, label: '뷰티' }]
      }
    };
  },
  methods: {
    loadSeller(sellerId) {
      if (seller_info.seller_id === Number(sellerId)) {
        const selectedSeller = seller_info;
        this.seller_id = selectedSeller.seller_id;
        this.account = selectedSeller.account;
        this.profileImageUrl = selectedSeller.profile_image;
        this.backgroundImageUrl = selectedSeller.background_image;
        this.seller_name_en = selectedSeller.seller_name_en;
        this.seller_name_ko = selectedSeller.seller_name_ko;
        this.shop_status = selectedSeller.shop_status;
        this.shop_status_id = selectedSeller.shop_status_id;
        let i = selectedSeller.managers.length;
        while (i > 0) {
          this.managers[i - 1].manager_id =
            selectedSeller.managers[i - 1].manager_id;
          this.managers[i - 1].manager_name =
            selectedSeller.managers[i - 1].manager_name;
          this.managers[i - 1].manager_mobile =
            selectedSeller.managers[i - 1].manager_mobile;
          this.managers[i - 1].manager_email =
            selectedSeller.managers[i - 1].manager_email;
          i--;
        }
        this.category = selectedSeller.category;
        this.category_id = selectedSeller.category_id;
        this.sellerCategoriesByType.selectedCategory =
          selectedSeller.category_id;
        this.category_type_id = selectedSeller.category_type_id;
        this.created_at = selectedSeller.created_at;
        this.short_introduction.value = selectedSeller.short_introduction;
        this.long_introduction.value = selectedSeller.long_introduction;
        this.cs_opening_time = moment(selectedSeller.cs_opening_time, 'HH:mm');
        this.cs_closing_time = moment(selectedSeller.cs_closing_time, 'HH:mm');
        this.cs_contact.value = selectedSeller.cs_contact;
        this.delivery_information.value = selectedSeller.delivery_information;
        this.exchange_refund_information.value =
          selectedSeller.exchange_refund_information;
      }
    },
    async getUserData(sellerId) {
      try {
        const res = await fetch(`${SELLER_INFO}/${sellerId}`, {
          method: 'GET',
          headers: {
            Authorization:
              'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50IjoibWFzdGVyMyIsImV4cCI6MTYwNzQwNTAzNH0.JiooF5kfRHafQdx2jtsw4AT7c0oujD0guyCXdLPmAxA'
          }
        });
        const data = await res.json();
        if (data.message === 'success') {
          if (data.seller_info.seller_id === Number(sellerId)) {
            const selectedSeller = data.seller_info;
            this.seller_id = selectedSeller.seller_id;
            this.account = selectedSeller.account;
            this.profileImageUrl = selectedSeller.profile_image;
            this.backgroundImageUrl = selectedSeller.background_image;
            this.seller_name_en = selectedSeller.seller_name_en;
            this.seller_name_ko = selectedSeller.seller_name_ko;
            this.shop_status = selectedSeller.shop_status;
            this.shop_status_id = selectedSeller.shop_status_id;
            let i = selectedSeller.managers.length;
            while (i > 0) {
              this.managers[i - 1].manager_id =
                selectedSeller.managers[i - 1].manager_id;
              this.managers[i - 1].manager_name =
                selectedSeller.managers[i - 1].manager_name;
              this.managers[i - 1].manager_mobile =
                selectedSeller.managers[i - 1].manager_mobile;
              this.managers[i - 1].manager_email =
                selectedSeller.managers[i - 1].manager_email;
              i--;
            }
            this.category = selectedSeller.category;
            this.category_id = selectedSeller.category_id;
            this.sellerCategoriesByType.selectedCategory =
              selectedSeller.category_id;
            this.category_type_id = selectedSeller.category_type_id;
            this.created_at = selectedSeller.created_at;
            this.short_introduction.value = selectedSeller.short_introduction;
            this.long_introduction.value = selectedSeller.long_introduction;
            this.cs_opening_time = moment(
              selectedSeller.cs_opening_time,
              'HH:mm'
            );
            this.cs_closing_time = moment(
              selectedSeller.cs_closing_time,
              'HH:mm'
            );
            this.cs_contact.value = selectedSeller.cs_contact;
            this.delivery_information.value =
              selectedSeller.delivery_information;
            this.exchange_refund_information.value =
              selectedSeller.exchange_refund_information;
          } else {
            alert("fetched data's seller_id doesn't match URL path id");
          }
        } else {
          alert('server message: FAIL');
        }
      } catch (err) {
        alert('get error: get request to server failed');
      }
    },
    // 이미지 업로드 methods
    handleChangeProfile(info) {
      if (info.file.status === 'uploading') {
        this.profileLoading = true;
        return;
      }
      if (info.file.status === 'done') {
        getBase64(info.file.originFileObj, (response) => {
          this.profileImageUrl = response;
          this.profileLoading = false;
        });
      }
      if (info.file.status === 'error') {
        this.profileLoading = false;
      }
    },
    handleChangeBackground(info) {
      if (info.file.status === 'uploading') {
        this.backgroundLoading = true;
        return;
      }
      if (info.file.status === 'done') {
        getBase64(info.file.originFileObj, (response) => {
          this.backgroundImageUrl = response;
          this.backgroundLoading = false;
        });
      }
      if (info.file.status === 'error') {
        this.backgroundLoading = false;
      }
    },
    beforeUploadProfile(file) {
      // console.log(file);
      const isJpgOrPng =
        file.type === 'image/jpeg' ||
        file.type === 'image/jpg' ||
        file.type === 'image/png';
      if (!isJpgOrPng) {
        message.error('셀러 프로필 확장자는 jpg, jpeg, png 만 가능합니다');
      }
      const isLt5M = file.size / 1024 / 1024 < 5;
      if (!isLt5M) {
        message.error('허용 가능한 최대 파일사이즈 크기는 5MB 입니다.');
      }
      this.profileImgList.unshift(file);
    },
    beforeUploadBackground(file) {
      const isJpgOrPng =
        file.type === 'image/jpeg' ||
        file.type === 'image/jpg' ||
        file.type === 'image/png';
      if (!isJpgOrPng) {
        message.error('셀러 프로필 확장자는 jpg, jpeg, png 만 가능합니다');
      }
      const isLt5M = file.size / 1024 / 1024 < 5;
      if (!isLt5M) {
        message.error('허용 가능한 최대 파일사이즈 크기는 5MB 입니다.');
      }
      this.backgroundImgList.unshift(file);
    },
    changeImage(imageCategory) {
      switch (imageCategory) {
        case 'profile':
          this.profileImgList = [];
          this.$refs.aUploadProfile.$el.children[0].children[0].children[0].value =
            '';
          this.$refs.aUploadProfile.$el.children[0].children[0].children[0].click();
          break;
        case 'background':
          this.backgroundImgList = [];
          this.$refs.aUploadBackground.$el.children[0].children[0].children[0].value =
            '';
          this.$refs.aUploadBackground.$el.children[0].children[0].children[0].click();
          break;
        default:
          console.log('error');
          break;
      }
    },
    deleteImage(imageCategory) {
      switch (imageCategory) {
        case 'profile':
          this.profileImgList = [];
          this.profileLoading = false;
          this.profileImageUrl = '';
          break;
        case 'background':
          this.backgroundImgList = [];
          this.backgroundLoading = false;
          this.backgroundImageUrl = '';
          break;
        default:
          console.log('error');
          break;
      }
    },
    setSelectedCategory() {
      console.log(this.sellerCategoriesByType.selectedCategory);
    },
    //
    validateInputs(input) {
      console.log(input);
    },
    addManager(managerNum) {
      this.managers[managerNum - 1].manager_id =
        this.sellerId + this.id + managerNum;
    },
    hideManager(managerNum) {
      this.managers[managerNum - 1].manager_id = null;
      this.managers[managerNum - 1].manager_name = '';
      this.managers[managerNum - 1].manager_mobile = '';
      this.managers[managerNum - 1].manager_email = '';
    },
    updateCsOpeningTime(time) {
      this.cs_opening_time = time;
      console.log(this.cs_opening_time.format('HH:mm'));
    },
    updateCsClosingTime(time) {
      this.cs_closing_time = time;
      console.log(this.cs_closing_time.format('HH:mm'));
    },
    requestEdit() {},
    cancelEdit() {
      const action = confirm(
        '수정을 취소하시겠습니까?\n확인을 누르시면 새로고침됩니다.'
      );
      if (action) {
        location.reload();
      }
    }
  },
  mounted() {
    // this.loadSeller(this.sellerId);
    this.getUserData(this.sellerId);
    if (this.shop_status_id === 1) {
      alert('입점대기 중인 셀러의 정보는 수정할 수 없습니다.');
    }
  }
  // watch: {
  //   sellerId(newSellerId) {
  //     this.loadSeller(newSellerId);
  //   }
  // }
};
</script>

<style lang="scss" scoped>
table {
  width: 100%;

  tbody {
    tr {
      min-height: 40px;
      &:nth-child(odd) {
        background: #eee;
      }
    }

    th,
    td {
      font-size: 13px;
      font-weight: 400;
      text-align: left;
      vertical-align: middle;
      padding: 10px;
      border: 0.5px solid #ddd;
    }

    th {
      width: 22%;
      background: #555;
      color: #fff;
    }

    .explanation {
      line-height: 1.3em;
      color: #1f91ff;
    }
  }

  .avatar-uploader > .ant-upload {
    width: 128px;
    height: 128px;
  }

  .ant-upload-select-picture-card {
    i {
      font-size: 32px;
      color: #999;
    }
  }

  .ant-upload-select-picture-card .ant-upload-text {
    margin-top: 8px;
    color: #666;
  }

  .uploaded-image {
    height: 100px;
    width: auto;
  }

  .input {
    width: 400px;
    border-radius: 10px;

    .input-box {
      &:focus ~ .input {
        border: 1px solid #000;
      }
    }
  }

  .seller-categories {
    display: flex;

    .radio {
      padding: 3px 10px;
    }
  }

  .textarea {
    height: 100px;
    min-width: 400px;
    width: 70%;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #e5e5e5;
    transition: border 500ms;

    &:focus {
      border: 1px solid #000;
      outline: none;
    }
  }

  .long-introduction {
    width: 400px;
  }

  .divider {
    width: 100%;
    height: 30px;
  }
  .divider.top {
    border-bottom: 1px solid #e5e5e5;
  }

  .manager-info {
    position: relative;
    display: flex;
    align-items: flex-end;

    .manager-inputs {
      .input.manager:not(:last-of-type) {
        margin-bottom: 5px;
      }
    }

    .manager-buttons {
      padding: 0 10px;
      display: flex;
      align-items: center;

      .button {
        border-radius: 5px;
        height: 30px;
        width: 40px;
        margin: 0 3px;
        cursor: pointer;

        .button-icon {
          color: #fff;
        }
      }

      .button.plus {
        background: #5db85b;
      }
      .button.minus {
        background: #d8534f;
      }

      p.manager-limit {
        padding-left: 5px;
      }
    }
  }

  .cs-hours {
    display: flex;
    align-items: center;

    .time-connector {
      display: flex;
      justify-content: center;
      align-items: center;
      width: 70px;
    }
  }
}
.dual-buttons {
  display: flex;
  margin-bottom: 10px;

  button {
    width: 50px;
    height: 35px;
    border-radius: 5px;
    margin: 3px;
    cursor: pointer;

    &.delete {
      color: white;
      background: #d8534f;
      border: 1px solid #d43f3a;
    }

    &.submit {
      color: white;
      background-color: #5db85b;
      border: 1px solid #4dae4c;
    }
    &.disabled {
      background: rgba(135, 199, 131, 1);
      cursor: default;
    }

    &.change,
    &.cancel {
      background-color: #fff;
      border: 1px solid #ddd;
    }
  }
}

.submit-buttons {
  justify-content: center;
  margin: 20px 0 30px 0;
}

button.disabled {
  color: black;
  background: white;
  cursor: default;
}
</style>
