<template>
  <div class="container">
    <h2>브랜디 어드민 로그인</h2>
    <form>
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
        pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
        title="Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters"
        placeholder="셀러 비밀번호"
        @input="checkIdPw"
      />
      <p :class="{ isEmpty: pwInvalid && loginClicked }">
        비밀번호를 입력해주세요.
      </p>

      <input
        type="submit"
        value="로그인"
        @click.prevent="loginClicked = true"
      />
    </form>
    <p class="checkSignup">
      아직 셀러가 아니신가요?
      <router-link class="signup" to="signup">회원가입하기</router-link>
    </p>
  </div>
</template>

<script lang="js">

export default{
    data() {
    return {
      idValue: '',
      pwValue: '',
      idInvalid: this.idValue===0? true : false,
      pwInvalid: false,
      loginClicked: false

    }
  },
  methods: {
    checkIdPw(){
      console.log('hahahaha')
      console.log(this.idValue)
      console.log(this.pwValue)
        this.idValue.length === 0 ? this.idInvalid = true : this.idInvalid = false;
        this.pwValue.length === 0 ? this.pwInvalid = true : this.pwInvalid = false;
    },
    getValue(e){
      console.log("hahaha");
      this.idValue = e.target.value;
      console.log(e.target.value)
    },
//     signin(){
//       var axios = require('axios';
//       const https = require('https');
//       require('https').globalAgent.options.ca = require('ssl-rrot-cas/latest').create();

//       var instance = axios.create({
// validateStatus: fucntion (status){
//   return status;
// }

//       });

//       var apiHelper = function(status){

//         this.generateAccessToken aswync function(hostUrl, username, password, client_secret){
//           try {
//             var post_date = {
//               'grant_tyep': 'client_credentials',
//               "username" : username,
//               "password":password,
//               "client_id": client_id
//             }

//             const agent + new https.Agent({

//               rejectUnauthorized: false
//             });

//             const responese = await axios({
//               method:'post',
//               url: hostURl + '443/auth/blabla ending point',
//               httpsAgent : agent, data : Objec.keys(posjt_data).map(function key) {

//                 return encodURIcoimpoent(key) + '=' + encodURIcomponent,
//               }
//                   headers: {
//                     'Contnet_)tyep': " application/x-www-form blablabla",
//                   }
//             });
//             console.log('access_token = ', response.data.access_token)
//             return response.data.access_toekn;
//           } catch (error){
//             console.log('token error is coming');
//             console.log('token error: ', )
//           }
//         }
//       }
//     }

  }
  }
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
