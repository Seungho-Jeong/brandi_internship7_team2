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
            v-for="input in signupInfoInputList"
            :input="input"
            :key="input.id"
            v-model.trim="input[`${input.id}Value`]"
            @update:modelValue="validateInput(input.id)"
          />
        </div>
        <div class="signup-subdiv manager-mobile">
          <h3>담당자 정보<span> (*실제 샾을 운영하시는 분)</span></h3>
          <InputWithSpan
            v-for="input in managerMobileInput"
            :input="input"
            :key="input.id"
            v-model.trim="input[`${input.id}Value`]"
            @update:modelValue="validateInput(input.id)"
          />
        </div>
        <div class="signup-subdiv seller-info">
          <h3>셀러 정보</h3>
          <div class="seller-categories">
            <RadioInputs
              v-for="category in sellerCategories.list"
              :radio-object="sellerCategories"
              :category="category"
              :key="category"
              v-model="sellerCategories.selectedSellerCategory"
            />
          </div>
          <InputWithSpan
            v-for="input in sellerInfoInputList"
            :input="input"
            :key="input.id"
            v-model.trim="input[`${input.id}Value`]"
            @update:modelValue="validateInput(input.id)"
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
import InputWithSpan from '../components/InputWithSpan.vue';
import RadioInputs from '../components/RadioInputs.vue';

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
      signupInfoInputList: [
        {
          id: 'account',
          type: 'text',
          placeholder: '아이디',
          accountValue: '',
          accountIsValid: true,
          iconClass: 'fas fa-user',
          spanText: {
            1: '이미 사용중인 아이디 입니다.',
            2: '아이디의 최소 길이는 5글자 입니다.',
            3: '아이디는 5-~20글자의 영문, 숫자, 언더바, 하이픈만 사용 가능하며 시작 문자는 영문 또는 숫자입니다.'
          },
          spanTextOption: 1
        },
        {
          id: 'password',
          type: 'password',
          placeholder: '비밀번호',
          passwordValue: '',
          passwordIsValid: true,
          iconClass: 'fas fa-lock',
          spanText: {
            1: '비밀번호는 8~20글자의 영문대소문자, 숫자, 특수문자를 조합해야 합니다.'
          },
          spanTextOption: 1
        },
        {
          id: 'passwordCheck',
          type: 'password',
          placeholder: '비밀번호 재입력',
          passwordCheckValue: '',
          passwordCheckIsValid: true,
          iconClass: 'fas fa-check',
          spanText: { 1: '비밀번호가 일치하지 않습니다.' },
          spanTextOption: 1
        }
      ],
      managerMobileInput: [
        {
          id: 'managerMobile',
          type: 'text',
          placeholder: '핸드폰번호',
          managerMobileValue: '',
          managerMobileIsValid: true,
          iconClass: 'fas fa-phone',
          spanText: {
            1: '올바른 정보를 입력해주세요.'
          },
          spanTextOption: 1,
          explanation:
            '입점 신청 후 브랜디 담당자가 연락을 드릴 수 있으니 정확한 정보를 기입해주세요.'
        }
      ],
      sellerCategories: {
        name: 'sellerCategory',
        selectedCateory: null,
        list: [
          '쇼핑몰',
          '마켓',
          '로드샵',
          '디자이너브랜드',
          '제너럴브랜드',
          '내셔널브랜드',
          '뷰티'
        ]
      },
      sellerInfoInputList: [
        {
          id: 'sellerNameKo',
          type: 'text',
          placeholder: '셀러명 (상호)',
          sellerNameKoValue: '',
          sellerNameKoIsValid: true,
          iconClass: 'fas fa-font',
          spanText: {
            1: '한글,영문,숫자만 입력해주세요.'
          },
          spanTextOption: 1
        },
        {
          id: 'sellerNameEng',
          type: 'text',
          placeholder: '영문 셀러명 (영문상호)',
          sellerNameEngValue: '',
          sellerNameEngIsValid: true,
          iconClass: 'fas fa-font',
          spanText: {
            1: '셀러 영문명은 소문자만 입력가능합니다.'
          },
          spanTextOption: 1
        },
        {
          id: 'csContact',
          type: 'text',
          placeholder: '고객센터 전화번호',
          csContactValue: '',
          csContactIsValid: true,
          iconClass: 'fas fa-phone',
          spanText: {
            1: '고객센터 전화번호는 숫자와 하이픈만 입력가능합니다.'
          },
          spanTextOption: 1
        }
      ]
    };
  },
  methods: {
    isAccountValid() {
      const inputId = this.signupInfoInputList[0];
      const inputIdValue = 'accountValue';
      const inputIdIsValid = 'accountIsValid';

      if (inputId[inputIdValue].length === 0) {
        inputId[inputIdIsValid] = true;
      } else {
        const isInputEntered = inputId[inputIdValue].length > 0;
        const isAccountAvailable = !this.existingAccounts.includes(
          inputId[inputIdValue]
        );
        const isAccountLengthValid = inputId[inputIdValue].length >= 5;
        const accountIdValidation = /^([A-Za-z0-9])([A-Za-z0-9_-]){4,19}$/;
        const isAccountIdValid = accountIdValidation.test(
          inputId[inputIdValue]
        );
        const isValid =
          isInputEntered &&
          isAccountAvailable &&
          isAccountLengthValid &&
          isAccountIdValid;

        isValid
          ? (inputId[inputIdIsValid] = true)
          : (inputId[inputIdIsValid] = false);

        if (!isValid) {
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
      const inputId = this.signupInfoInputList[1];
      const inputIdValue = 'passwordValue';
      const inputIdIsValid = 'passwordIsValid';

      if (inputId[inputIdValue].length === 0) {
        inputId[inputIdIsValid] = true;
      } else {
        const pwValidation = /^(?=.*[A-Za-z])(?=.*[0-9])(?=.*[~!@#$%^&*()\-_=+,.<>/?;:'"[{}\]\\|]).{8,20}$/;
        const isValid = pwValidation.test(inputId[inputIdValue]);

        isValid
          ? (inputId[inputIdIsValid] = true)
          : (inputId[inputIdIsValid] = false);

        this.isPwCheckValid();
      }
    },
    isPwCheckValid() {
      const inputId = this.signupInfoInputList[2];
      const inputIdValue = 'passwordCheckValue';
      const inputIdIsValid = 'passwordCheckIsValid';

      if (inputId[inputIdValue].length === 0) {
        inputId[inputIdIsValid] = true;
      } else {
        const isValid =
          this.isPwValid &&
          this.signupInfoInputList[1].passwordValue === inputId[inputIdValue];

        isValid
          ? (inputId[inputIdIsValid] = true)
          : (inputId[inputIdIsValid] = false);
      }
    },
    isManagerMobileValid() {
      const inputId = this.managerMobileInput[0];
      const inputIdValue = 'managerMobileValue';
      const inputIdIsValid = 'managerMobileIsValid';

      if (inputId[inputIdValue].length === 0) {
        inputId[inputIdIsValid] = true;
      } else {
        const managerMobileValidation = /^(\d{11})$/;
        const isValid = managerMobileValidation.test(inputId[inputIdValue]);

        isValid
          ? (inputId[inputIdIsValid] = true)
          : (inputId[inputIdIsValid] = false);
      }
    },
    isSellerNameKoValid() {
      const inputId = this.sellerInfoInputList[0];
      const inputIdValue = 'sellerNameKoValue';
      const inputIdIsValid = 'sellerNameKoIsValid';

      if (inputId[inputIdValue].length === 0) {
        inputId[inputIdIsValid] = true;
      } else {
        const sellerNameKoValidation = /^([A-Za-z0-9\uac00-\ud7af])+$/;
        const isValid = sellerNameKoValidation.test(inputId[inputIdValue]);
        isValid
          ? (inputId[inputIdIsValid] = true)
          : (inputId[inputIdIsValid] = false);
      }
    },
    isSellerNameEngValid() {
      const inputId = this.sellerInfoInputList[1];
      const inputIdValue = 'sellerNameEngValue';
      const inputIdIsValid = 'sellerNameEngIsValid';

      if (inputId[inputIdValue].length === 0) {
        inputId[inputIdIsValid] = true;
      } else {
        const sellerNameEngValidation = /^([a-z])+$/;
        const isValid = sellerNameEngValidation.test(inputId[inputIdValue]);

        isValid
          ? (inputId[inputIdIsValid] = true)
          : (inputId[inputIdIsValid] = false);
      }
    },
    isCsContactValid() {
      const inputId = this.sellerInfoInputList[2];
      const inputIdValue = 'csContactValue';
      const inputIdIsValid = 'csContactIsValid';

      if (inputId[inputIdValue].length === 0) {
        inputId[inputIdIsValid] = true;
      } else {
        const managerMobileValidation = /^([\d-]+)$/;
        const isValid = managerMobileValidation.test(inputId[inputIdValue]);

        isValid
          ? (inputId[inputIdIsValid] = true)
          : (inputId[inputIdIsValid] = false);
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
        this.signupInfoInputList[0].accountIsValid,
        this.signupInfoInputList[1].passwordIsValid,
        this.signupInfoInputList[2].passwordCheckIsValid,
        this.managerMobileInput[0].managerMobileIsValid,
        this.sellerInfoInputList[0].sellerNameKoIsValid,
        this.sellerInfoInputList[1].sellerNameEngIsValid,
        this.sellerInfoInputList[2].csContactIsValid
      ];
      const isAllValid = validationItemsList.every((item) => item == true);

      isAllValid ? (this.isFormValid = true) : (this.isFormValid = false);
    },
    requestSignup() {
      this.validateForm();

      if (this.isFormValid) {
        const action = confirm('입력하신 정보로 셀러신청을 하시겠습니까?');
        if (action) {
          alert(
            '신청이 완료되었습니다.\n검토 후 연락 드리겠습니다. 감사합니다.'
          );
        }
      } else {
        alert('입력하신 정보를 확인해주세요.');
      }
    },
    cancelSignup() {
      const action = confirm('브랜디 가입을 취소하시겠습니까?');
      if (action) {
        alert('회원가입이 취소되었습니다');
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
