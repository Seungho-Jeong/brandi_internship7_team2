<template>
  <div class="container">
    <h2>브랜디 어드민 로그인</h2>
    <form @submit.prevent="login">
      <input
        :class="{ isEmpty: idInvalid && loginClicked }"
        v-model="idValue"
        type="text"
        id="id"
        name="id"
        placeholder="셀러 아이디"
        @input="checkIdPw"
      />
      <p :class="{ isEmpty: idInvalid && loginClicked }">
        아이디를 입력해주세요.
      </p>
      <input
        :class="{ isEmpty: pwInvalid && loginClicked }"
        v-model="pwValue"
        type="password"
        id="pw"
        name="psw"
        title="Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters"
        placeholder="셀러 비밀번호"
        @input="checkIdPw"
      />
      <p :class="{ isEmpty: pwInvalid && loginClicked }">
        비밀번호를 입력해주세요.
      </p>

      <input type="submit" value="로그인" />
    </form>
    <p class="checkSignup">
      아직 셀러가 아니신가요?
      <router-link class="signup" to="signup">회원가입하기</router-link>
    </p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Login',
  data() {
    return {
      idValue: '',
      pwValue: '',
      idInvalid: this.idValue === 0 ? true : false,
      pwInvalid: false,
      loginClicked: false,
      token: ''
    };
  },
  methods: {
    checkIdPw() {
      this.idValue.length === 0
        ? (this.idInvalid = true)
        : (this.idInvalid = false);
      this.pwValue.length === 0
        ? (this.pwInvalid = true)
        : (this.pwInvalid = false);
    },
    getValue(e) {
      this.idValue = e.target.value;
    },
    login() {
      const auth = { account: this.idValue, password: this.pwValue };
      console.log(this.idValue);
      // // Correct username is 'foo' and password is 'bar'
      const url = 'http://10.251.1.120:5000/user/signin';
      axios
        .post(url, auth)
        .then((res) => res.data)
        .then((resp) => {
          this.token = resp.access_token;
          console.log(this.token);
          this.$router.push('/account');
        })
        .catch((error) => {
          console.error(error);
          this.$router.push('/signup');
        });
    }
  }
};
</script>

<style lang="scss" scoped>
body {
  background-color: #fafafa;

  .container {
    background-color: white;
    padding: 20px;
    width: 380px;
    height: 518px;
    box-shadow: 0 4px 31px 0 rgba(0, 0, 0, 0.1);

    form {
      input {
        width: 100%;
        padding: 12px;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-sizing: border-box;
        margin-top: 6px;
        margin-bottom: 16px;
      }
      input.isEmpty {
        width: 100%;
        padding: 12px;
        border: 1px solid red;
        border-radius: 4px;
        box-sizing: border-box;
        margin-top: 6px;
        margin-bottom: 16px;
      }

      p {
        display: none;
      }
      p.isEmpty {
        display: block;
      }

      input[type='submit'] {
        background-color: black;
        color: white;
      }
    }

    p.checkSignup {
      color: #929292;

      .signup {
        color: #3c72ff;
      }
    }
  }
}
</style>
