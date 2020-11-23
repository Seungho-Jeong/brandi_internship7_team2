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
            v-model.trim="input[`${input.id}Value`]"
            :key="input.id"
            @blur="clearValidation"
          />
        </div>
        <div class="signup-subdiv manager-mobile">
          <h3>담당자 정보<span> (*실제 샾을 운영하시는 분)</span></h3>
          <InputWithSpan
            v-for="input in manangerMobileInput"
            v-model.trim="input[`${input.id}Value`]"
            :input="input"
            :key="input.id"
          />
        </div>
        <div class="signup-subdiv seller-info">
          <h3>셀러 정보</h3>
          <div class="seller-categories">
            <div
              v-for="category in sellerCategories"
              class="radio-selection"
              :key="category"
            >
              <input
                type="radio"
                name="sellerCategory"
                :value="category"
                :id="category"
              />
              <label :for="category">{{ category }}</label>
            </div>
          </div>
          <InputWithSpan
            v-for="input in sellerInfoInputList"
            v-model.trim="input[`${input.id}Value`]"
            :input="input"
            :key="input.id"
          />
        </div>
        <div class="buttons">
          <button class="left" @click="requestSignup">신청</button>
          <button class="right" @click="requestSignup">신청</button>
        </div>
      </form>
    </section>
  </section>
</template>

<script>
import InputWithSpan from '../components/InputWithSpan.vue';

export default {
  name: 'Signup',
  components: {
    InputWithSpan
  },
  data() {
    return {
      existingAccounts: [],
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
            2: '아이디의 최소 길이는 5글자 입니다.'
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
      manangerMobileInput: [
        {
          id: 'managerMobile',
          type: 'text',
          placeholder: '핸드폰번호',
          managerMobileValue: '',
          managerMobileIsValid: null,
          iconClass: 'fas fa-phone',
          spanText: {
            1: '입점 신청 후 브랜디 담당자가 연락을 드릴 수 있으니 정확한 정보를 기입해주세요.'
          },
          spanTextOption: 1
        }
      ],
      sellerCategories: [
        '쇼핑몰',
        '마켓',
        '로드샵',
        '디자이너브랜드',
        '제너럴브랜드',
        '내셔널브랜드',
        '뷰티'
      ],
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
            1: ''
          },
          spanTextOption: 1
        }
      ]
    };
  },
  // watch: {
  //   signupInfoInputList() {
  //     this.isAccountValid();
  //   }
  // },
  updated() {
    this.isAccountValid();
  },
  methods: {
    isAccountValid() {
      const isAccountAvailable =
        this.signupInfoInputList[0].accountValue.length !== 0 &&
        this.existingAccounts.includes(
          this.signupInfoInputList[0].accountValue
        );
      isAccountAvailable ? console.log('true') : console.log('false');
      const isAccountLengthValid =
        this.signupInfoInputList[0].accountValue.length >= 5;
      const isValid = isAccountAvailable && isAccountLengthValid;
      isValid
        ? (this.signupInfoInputList[0].accountIsValid = true)
        : (this.signupInfoInputList[0].accountIsValid = false);
      if (!isValid) {
        !isAccountAvailable || (!isAccountAvailable && !isAccountLengthValid)
          ? (this.signupInfoInputList[0].spanTextOption = 1)
          : !isAccountLengthValid
          ? (this.signupInfoInputList[0].spanTextOption = 2)
          : null;
      }
    },
    isPwValid() {
      const pwValidation = /^(?=.{8,20})(?=.*([A-Za-z]))(?=.*[0-9])(?=.*[~!@#$%^&*()-_=+,.<>/?;:'"[{}\]\\|]).*$/;
      const isValid = pwValidation.test(
        this.signupInfoInputList[1].passwordValue
      );

      isValid
        ? (this.signupInfoInputList[1].passwordIsValid = true)
        : (this.signupInfoInputList[1].passwordIsValid = false);
    },
    isPwCheckValid() {
      const isValid =
        this.isPwValid &&
        this.signupInfoInputList[1].passwordValue ===
          this.signupInfoInputList[2].passwordCheckValue;

      isValid
        ? (this.signupInfoInputList[2].passwordCheckIsValid = true)
        : (this.signupInfoInputList[2].passwordCheckIsValid = false);
    },
    isSellerNameKoValid(e) {
      const sellerNameKoValidation = /^(?=.*[A-Za-z0-9]).*$/;
      return (
        e.target.value.length > 0 && sellerNameKoValidation.test(e.target.value)
      );
    },
    clearValidation() {
      this.signupInfoInputList[0].accountIsValid = true;
      this.signupInfoInputList[1].passwordIsValid = true;
      this.signupInfoInputList[2].passwordCheckIsValid = true;
    }
  },
  validateInput() {
    return true;
    // if (e.target.id === 'account') {
    //   console.log(this.$refs.spanType.id);
    //   return this.isAccountValid;
    // }
    // if (e.target.id === 'password') {
    //   return this.isPwValid;
    // }
    // if (e.target.id === 'passwordCheck') {
    //   return this.isPwCheckValid;
    // }
    // this.$set(this.signupInfoInputList, 'isValid', this.isAccountValid);
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

          .radio-selection {
            margin-right: 15px;
            cursor: pointer;

            input {
              cursor: pointer;
            }

            label {
              font-size: 14px;
              cursor: pointer;
            }
          }
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
