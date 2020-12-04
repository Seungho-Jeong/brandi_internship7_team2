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
                action="https://www.mocky.io/v2/5cc8019d300000980a055e76"
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
            <td>{{ seller_category_id }}</td>
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
                action="https://www.mocky.io/v2/5cc8019d300000980a055e76"
                :before-upload="beforeUploadBackground"
                @change="handleChangeBackground"
                ref="aUploadBackground"
              >
                <img
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
                @update:modelValue="setInputValue('short_introduction')"
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
                    :isValid="manager1.name.isValid"
                    v-model.trim="manager1.name.value"
                    @update:modelValue="setInputValue('manager1_name')"
                  />
                  <InputWithSpan
                    class="input manager"
                    id="manager1_mobile"
                    type="text"
                    placeholder="담당자 핸드폰번호"
                    icon="phone"
                    :isValid="manager1.mobile.isValid"
                    v-model.trim="manager1.mobile.value"
                    @update:modelValue="setInputValue('manager1_mobile')"
                  />
                  <InputWithSpan
                    class="input manager"
                    id="manager1_email"
                    type="text"
                    placeholder="담당자 이메일"
                    icon="email"
                    :isValid="manager1.email.isValid"
                    v-model.trim="manager1.email.value"
                    @update:modelValue="setInputValue('manager1_email')"
                  />
                </div>
                <div class="manager-buttons">
                  <button class="button plus" @click="addManager(2)">
                    <PlusOutlined class="button-icon" />
                  </button>
                </div>
              </div>
              <div v-if="manager2.isAdded" class="divider top"></div>
              <div v-if="manager2.isAdded" class="divider bottom"></div>
              <div
                v-if="manager2.isAdded"
                class="manager-info"
                :class="{ isActive: manager2.isAdded }"
              >
                <div class="manager-inputs">
                  <InputWithSpan
                    class="input manager"
                    id="manager2_name"
                    type="text"
                    placeholder="담당자명2"
                    icon="user"
                    :isValid="manager2.name.isValid"
                    v-model.trim="manager2.name.value"
                    @update:modelValue="setInputValue('manager2_name')"
                  />
                  <InputWithSpan
                    class="input manager"
                    id="manager2_mobile"
                    type="text"
                    placeholder="담당자 핸드폰번호2"
                    icon="phone"
                    :isValid="manager2.mobile.isValid"
                    v-model.trim="manager2.mobile.value"
                    @update:modelValue="setInputValue('manager2_mobile')"
                  />
                  <InputWithSpan
                    class="input manager"
                    id="manager2_email"
                    type="text"
                    placeholder="담당자 이메일2"
                    icon="email"
                    :isValid="manager2.email.isValid"
                    v-model.trim="manager2.email.value"
                    @update:modelValue="setInputValue('manager2_email')"
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
              <div v-if="manager3.isAdded" class="divider top"></div>
              <div v-if="manager3.isAdded" class="divider bottom"></div>
              <div
                v-if="manager3.isAdded"
                class="manager-info"
                :class="{ isActive: manager3.isAdded }"
              >
                <div class="manager-inputs">
                  <InputWithSpan
                    class="input manager"
                    id="manager3_name"
                    type="text"
                    placeholder="담당자명3"
                    icon="user"
                    :isValid="manager3.name.isValid"
                    v-model.trim="manager3.name.value"
                    @update:modelValue="setInputValue('manager3_name')"
                  />
                  <InputWithSpan
                    class="input manager"
                    id="manager3_mobile"
                    type="text"
                    placeholder="담당자 핸드폰번호3"
                    icon="phone"
                    :isValid="manager3.mobile.isValid"
                    v-model.trim="manager3.mobile.value"
                    @update:modelValue="setInputValue('manager3_mobile')"
                  />
                  <InputWithSpan
                    class="input manager"
                    id="manager3_email"
                    type="text"
                    placeholder="담당자 이메일3"
                    icon="email"
                    :isValid="manager3.email.isValid"
                    v-model.trim="manager3.email.value"
                    @update:modelValue="setInputValue('manager3_email')"
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
                @update:modelValue="setInputValue('cs_contact')"
              />
            </td>
          </tr>
          <tr>
            <th>고객센터 운영시간 (주중)</th>
            <td>ㅇ</td>
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
                :isValid="long_introduction.isValid"
                v-model.trim="long_introduction.value"
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
                :isValid="long_introduction.isValid"
                v-model.trim="long_introduction.value"
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
      <button class="submit" type="button" @click="requestEdit">수정</button>
      <button class="cancel" type="button" @click="cancelEdit">취소</button>
    </div>
  </div>
</template>
<script>
import PageHeading from '../../components/reusables/PageHeading.vue';
import PageBar from '../../components/reusables/PageBar.vue';
import PageSection from '../../components/reusables/PageSection.vue';
import InputWithSpan from '../../components/reusables/InputWithSpan.vue';

import { Upload } from 'ant-design-vue';
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
    PlusOutlined,
    LoadingOutlined,
    MinusOutlined,
    PageHeading,
    PageBar,
    PageSection,
    InputWithSpan
  },
  data() {
    return {
      seller_id: '',
      account: '',
      seller_name_en: '',
      seller_name_ko: '',
      manager_name: '',
      shop_status: '',
      manager_mobile: '',
      manager_email: '',
      seller_category_id: '',
      seller_type_id: '',
      created_at: '',
      //이미지 업로드 ant design 컴포넌트 data
      profileImgList: [],
      backgroundImgList: [],
      profileLoading: false,
      profileImageUrl: '',
      backgroundLoading: false,
      backgroundImageUrl: '',
      //셀러 소개 data
      short_introduction: {
        value: '',
        isValid: true
      },
      long_introduction: {
        value: '',
        isValid: true
      },
      manager1: {
        name: {
          value: '',
          isValid: true
        },
        mobile: {
          value: '',
          isValid: true
        },
        email: {
          value: '',
          isValid: true
        }
      },
      manager2: {
        isAdded: false,
        name: {
          value: '',
          isValid: true
        },
        mobile: {
          value: '',
          isValid: true
        },
        email: {
          value: '',
          isValid: true
        }
      },
      manager3: {
        isAdded: false,
        name: {
          value: '',
          isValid: true
        },
        mobile: {
          value: '',
          isValid: true
        },
        email: {
          value: '',
          isValid: true
        }
      },
      cs_contact: {
        value: '',
        isValid: true
      }
    };
  },
  methods: {
    loadSeller(sellerId) {
      const { sellerData } = this;
      const selectedSeller = sellerData.find(
        (seller) => seller.seller_id == sellerId
      );
      this.seller_id = selectedSeller.seller_id;
      this.account = selectedSeller.account;
      this.seller_name_en = selectedSeller.seller_name_en;
      this.seller_name_ko = selectedSeller.seller_name_ko;
      this.manager_name = selectedSeller.manager_name;
      this.shop_status = selectedSeller.shop_status;
      this.manager_mobile = selectedSeller.manager_mobile;
      this.manager_email = selectedSeller.manager_email;
      this.seller_category_id = selectedSeller.seller_category_id;
      this.created_at = selectedSeller.created_at;
    },
    // 이미지 업로드 ant design 컴포넌트 methods
    handleChangeProfile(info) {
      console.log(info);
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
      console.log(file);
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
          // console.log(
          this.profileImgList = [];
          this.$refs.aUploadProfile.$el.children[0].children[0].children[0].click();
          // );
          // this.$refs.aUploadProfile.click();
          break;
        case 'background':
          console.log(this.$refs.aUploadBackground);
          // this.$refs.aUploadBackground.click();
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
    setShortIntroduction() {
      console.log(this.shortIntroduction.value);
    },
    setLongIntroduction() {
      console.log(this.longIntroduction.value);
    },
    addManager(managerNum) {
      switch (managerNum) {
        case 2:
          this.manager2.isAdded = true;
          break;
        case 3:
          this.manager3.isAdded = true;
          break;
      }
    },
    hideManager(managerNum) {
      switch (managerNum) {
        case 2:
          this.manager2.isAdded = false;
          break;
        case 3:
          this.manager3.isAdded = false;
          break;
      }
    }
  },
  created() {
    this.loadSeller(this.sellerId);
  },
  watch: {
    sellerId(newSellerId) {
      this.loadSeller(newSellerId);
    }
  }
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
</style>
