/* eslint-disable vue/valid-v-for */ /* eslint-disable vue/no-unused-vars */ /*
eslint-disable vue/require-v-for-key */

<template>
  <section class="signup-page">
    <section class="signup-container">
      <img
        class="logo"
        src="../assets/images/logo_seller_admin_1.png"
        alt="Brandi admin logo"
      />
      <h2>셀러회원 가입</h2>
      <img
        class="seller-join-top-img"
        src="../assets/images/seller_join_top_2.png"
        alt="seller join top"
      />
      <form>
        <div class="signup-subdiv account-and-pw">
          <h3>가입 정보</h3>
          <InputWithSpan
            :input="account"
            v-model.trim="account.value"
            @update:modelValue="validateInput(account.id)"
          />
          <InputWithSpan
            :input="password"
            v-model.trim="password.value"
            @update:modelValue="validateInput(password.id)"
          />
          <InputWithSpan
            :input="passwordCheck"
            v-model.trim="passwordCheck.value"
            @update:modelValue="validateInput(passwordCheck.id)"
          />
        </div>
        <div class="signup-subdiv manager-mobile">
          <h3>담당자 정보<span> (*실제 샾을 운영하시는 분)</span></h3>
          <InputWithSpan
            :input="managerMobile"
            v-model.trim="managerMobile.value"
            @update:modelValue="validateInput(managerMobile.id)"
          />
        </div>
        <div class="signup-subdiv seller-info">
          <h3>셀러 정보</h3>
          <div class="seller-categories">
            <RadioInputs
              v-for="category in sellerCategories.list"
              :radio-object="sellerCategories"
              :category="category"
              :key="category.categoryId"
              :value="category.categoryId"
              v-model="sellerCategories.selectedSellerCategory"
              @update:modelValue="setSelectedCategory()"
            />
          </div>
          <InputWithSpan
            :input="sellerNameKo"
            v-model.trim="sellerNameKo.value"
            @update:modelValue="validateInput(sellerNameKo.id)"
          />
          <InputWithSpan
            :input="sellerNameEng"
            v-model.trim="sellerNameEng.value"
            @update:modelValue="validateInput(sellerNameEng.id)"
          />
          <InputWithSpan
            :input="csContact"
            v-model.trim="csContact.value"
            @update:modelValue="validateInput(csContact.id)"
          />
        </div>
        <div class="buttons">
          <button class="left" type="submit" @click="requestSignup">
            신청
          </button>
          <button class="right" type="submit" @click="cancelSignup">
            취소
          </button>
        </div>
      </form>
    </section>
  </section>
</template>

<script>
import InputWithSpan from '../components/reusables/InputWithSpan.vue';
import RadioInputs from '../components/reusables/RadioInputs.vue';

export default {
  name: 'Signup',
  components: {
    InputWithSpan,
    RadioInputs
  },
  data() {
    return {
      existingAccounts: ['d', 'dd'],
      isFormValid: false,
      account: {
        id: 'account',
        type: 'text',
        placeholder: '아이디',
        value: '',
        isValid: true,
        iconClass: 'fas fa-user',
        spanText: {
          1: '이미 사용중인 아이디 입니다.',
          2: '아이디의 최소 길이는 5글자 입니다.',
          3: '아이디는 5-~20글자의 영문, 숫자, 언더바, 하이픈만 사용 가능하며 시작 문자는 영문 또는 숫자입니다.'
        },
        spanTextOption: 1
      },
      password: {
        id: 'password',
        type: 'password',
        placeholder: '비밀번호',
        value: '',
        isValid: true,
        iconClass: 'fas fa-lock',
        spanText: {
          1: '비밀번호는 8~20글자의 영문대소문자, 숫자, 특수문자를 조합해야 합니다.'
        },
        spanTextOption: 1
      },
      passwordCheck: {
        id: 'passwordCheck',
        type: 'password',
        placeholder: '비밀번호 재입력',
        value: '',
        isValid: true,
        iconClass: 'fas fa-check',
        spanText: { 1: '비밀번호가 일치하지 않습니다.' },
        spanTextOption: 1
      },
      managerMobile: {
        id: 'managerMobile',
        type: 'text',
        placeholder: '핸드폰번호',
        value: '',
        isValid: true,
        iconClass: 'fas fa-phone',
        spanText: {
          1: '올바른 정보를 입력해주세요.'
        },
        spanTextOption: 1,
        explanation:
          '입점 신청 후 브랜디 담당자가 연락을 드릴 수 있으니 정확한 정보를 기입해주세요.'
      },
      sellerCategories: {
        name: 'sellerCategory',
        selectedSellerCategory: null,
        list: [
          { categoryId: 1, label: '쇼핑몰' },
          { categoryId: 2, label: '마켓' },
          { categoryId: 3, label: '로드샵' },
          { categoryId: 4, label: '디자이너브랜드' },
          { categoryId: 5, label: '제너럴브랜드' },
          { categoryId: 6, label: '내셔널브랜드' },
          { categoryId: 7, label: '뷰티' }
        ]
      },
      selectedSellerCategory: null,
      sellerNameKo: {
        id: 'sellerNameKo',
        type: 'text',
        placeholder: '셀러명 (상호)',
        value: '',
        isValid: true,
        iconClass: 'fas fa-font',
        spanText: {
          1: '한글,영문,숫자만 입력해주세요.'
        },
        spanTextOption: 1
      },
      sellerNameEng: {
        id: 'sellerNameEng',
        type: 'text',
        placeholder: '영문 셀러명 (영문상호)',
        value: '',
        isValid: true,
        iconClass: 'fas fa-font',
        spanText: {
          1: '셀러 영문명은 소문자만 입력가능합니다.'
        },
        spanTextOption: 1
      },
      csContact: {
        id: 'csContact',
        type: 'text',
        placeholder: '고객센터 전화번호',
        value: '',
        isValid: true,
        iconClass: 'fas fa-phone',
        spanText: {
          1: '고객센터 전화번호는 숫자와 하이픈만 입력가능합니다.'
        },
        spanTextOption: 1
      }
    };
  },
  methods: {
    setSelectedCategory() {
      console.log(this.sellerCategories.selectedSellerCategory);
    },
    isAccountValid() {
      // console.log(this.selectedSellerCategory);
      const inputId = this.account;

      if (inputId.value.length === 0) {
        inputId.isValid = true;
      } else {
        const isInputEntered = inputId.value.length > 0;
        const isAccountAvailable = !this.existingAccounts.includes(
          inputId.value
        );
        const isAccountLengthValid = inputId.value.length >= 5;
        const accountIdValidation = /^([A-Za-z0-9])([A-Za-z0-9_-]){4,19}$/;
        const isAccountIdValid = accountIdValidation.test(inputId.value);
        const isInputValid =
          isInputEntered &&
          isAccountAvailable &&
          isAccountLengthValid &&
          isAccountIdValid;

        isInputValid ? (inputId.isValid = true) : (inputId.isValid = false);

        if (!isInputValid) {
          !isAccountAvailable || (!isAccountAvailable && !isAccountLengthValid)
            ? (inputId.spanTextOption = 1)
            : !isAccountLengthValid
            ? (inputId.spanTextOption = 2)
            : !isAccountIdValid
            ? (inputId.spanTextOption = 3)
            : null;
        }
      }
    },
    isPwValid() {
      const inputId = this.password;

      if (inputId.value.length === 0) {
        inputId.isValid = true;
      } else {
        const pwValidation = /^(?=.*[A-Za-z])(?=.*[0-9])(?=.*[~!@#$%^&*()\-_=+,.<>/?;:'"[{}\]\\|]).{8,20}$/;
        const isInputValid = pwValidation.test(inputId.value);

        isInputValid ? (inputId.isValid = true) : (inputId.isValid = false);

        this.isPwCheckValid();
      }
    },
    isPwCheckValid() {
      const inputId = this.passwordCheck;

      if (inputId.value.length === 0) {
        inputId.isValid = true;
      } else {
        const isInputValid =
          this.isPwValid && this.password.value === inputId.value;

        isInputValid ? (inputId.isValid = true) : (inputId.isValid = false);
      }
    },
    isManagerMobileValid() {
      const inputId = this.managerMobile;

      if (inputId.value.length === 0) {
        inputId.isValid = true;
      } else {
        const managerMobileValidation = /^(\d{11})$/;
        const isInputValid = managerMobileValidation.test(inputId.value);

        isInputValid ? (inputId.isValid = true) : (inputId.isValid = false);
      }
    },
    isSellerNameKoValid() {
      const inputId = this.sellerNameKo;

      if (inputId.value.length === 0) {
        inputId.isValid = true;
      } else {
        const sellerNameKoValidation = /^([A-Za-z0-9\uac00-\ud7af])+$/;
        const isInputValid = sellerNameKoValidation.test(inputId.value);
        isInputValid ? (inputId.isValid = true) : (inputId.isValid = false);
      }
    },
    isSellerNameEngValid() {
      const inputId = this.sellerNameEng;

      if (inputId.value.length === 0) {
        inputId.isValid = true;
      } else {
        const sellerNameEngValidation = /^([a-z])+$/;
        const isInputValid = sellerNameEngValidation.test(inputId.value);

        isInputValid ? (inputId.isValid = true) : (inputId.isValid = false);
      }
    },
    isCsContactValid() {
      const inputId = this.csContact;

      if (inputId.value.length === 0) {
        inputId.isValid = true;
      } else {
        const managerMobileValidation = /^([\d-]+)$/;
        const isInputValid = managerMobileValidation.test(inputId.value);

        isInputValid ? (inputId.isValid = true) : (inputId.isValid = false);
      }
    },
    validateInput(inputId) {
      switch (inputId) {
        case 'account':
          this.isAccountValid();
          break;
        case 'password':
          this.isPwValid();
          break;
        case 'passwordCheck':
          this.isPwCheckValid();
          break;
        case 'managerMobile':
          this.isManagerMobileValid();
          break;
        case 'sellerNameKo':
          this.isSellerNameKoValid();
          break;
        case 'sellerNameEng':
          this.isSellerNameEngValid();
          break;
        case 'csContact':
          this.isCsContactValid();
          break;
        default:
          console.log('Input validation error');
      }
    },
    validateForm() {
      const validationItemsList = [
        this.account.isValid,
        this.password.isValid,
        this.passwordCheck.isValid,
        this.managerMobile.isValid,
        this.sellerNameKo.isValid,
        this.sellerNameEng.isValid,
        this.csContact.isValid
      ];
      const isAllValid = validationItemsList.every((item) => item == true);

      isAllValid ? (this.isFormValid = true) : (this.isFormValid = false);
    },
    async requestSignup() {
      this.validateForm();

      if (this.isFormValid) {
        const API = 'http://localhost:5000/user/signup';
        try {
          const res = await fetch(API, {
            method: 'POST',
            body: JSON.stringify({
              seller_category_id: this.sellerCategories.selectedCateory,
              account: this.account.value,
              password: this.password.value,
              seller_name_ko: this.sellerNameKo.value,
              seller_name_en: this.sellerNameEng.value,
              cs_contact: this.csContact.value,
              is_master: false
            })
          });
          const data = await res.json();
          if (data.message === 'success') {
            const action = confirm('입력하신 정보로 셀러신청을 하시겠습니까?');
            if (action) {
              alert(
                '신청이 완료되었습니다.\n검토 후 연락 드리겠습니다. 감사합니다.'
              );
              this.$router.push('/');
            }
          }
        } catch (err) {
          alert('POST error: post request to server failed');
        }
      } else {
        alert('입력하신 정보를 확인해주세요.');
      }
    },
    cancelSignup() {
      const action = confirm('브랜디 가입을 취소하시겠습니까?');
      if (action) {
        this.$router.push('/');
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.signup-page {
  width: 100vw;
  height: 100vh;
  overflow: auto;
  background: #fafafa;

  .signup-container {
    width: 500px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    background: white;

    .logo {
      width: 28%;
      margin-top: 20px;
      margin-bottom: 30px;
    }

    h2 {
      width: 85%;
      font-size: 24px;
      font-weight: 400;
      margin-bottom: 20px;
      text-align: center;
      position: relative;

      &::after {
        position: absolute;
        bottom: -20px;
        left: 0;
        content: '';
        height: 1px;
        width: 100%;
        background-color: #e0dfdf;
      }
    }

    .seller-join-top-img {
      width: 80%;
      height: auto;
      margin-top: 20px;
    }

    form {
      width: 80%;
      display: flex;
      flex-direction: column;
      align-items: center;

      .signup-subdiv {
        width: 100%;
        margin-top: 35px;

        &.manager-mobile span {
          font-size: 85%;
          font-weight: 200;
          color: #349afe;
        }

        h3 {
          font-size: 18px;
          font-weight: 400;
          margin-bottom: 10px;
        }

        .seller-categories {
          display: flex;
          flex-wrap: wrap;
        }
      }

      .buttons {
        display: flex;
        margin: 40px 0 30px 0;

        button {
          width: 60px;
          height: 35px;
          color: white;
          cursor: pointer;

          &.left {
            background-color: #5bc0de;
            border-top-left-radius: 5px;
            border-bottom-left-radius: 5px;
          }

          &.right {
            background-color: #d8534f;
            border-top-right-radius: 5px;
            border-bottom-right-radius: 5px;
          }
        }
      }
    }
  }
}
</style>
