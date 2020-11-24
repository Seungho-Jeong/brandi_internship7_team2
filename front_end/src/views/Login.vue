<template>
  <div class="container">
    <form>
      <label for="usrname">Username</label>
      <input
        :class="{ isEmpty: idInvalid }"
        type="text"
        id="id"
        name="usrname"
        required
        placeholder="셀러 아이디"
        @input="getValue"
      >
      <p :class="{ isEmpty: idInvalid }">
아이디를 입력해주세요.
</p>

      <label for="psw">Password</label>
      <input
        :class="{ isEmpty: pwInvalid }"
        type="password"
        id="pw"
        name="psw"
        pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
        title="Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters"
        required
        placeholder="셀러 비밀번호"
        @onChange="getValue()"
      />
      <p :class="{ isEmpty: pwInvalid }">
비밀번호를 입력해주세요.
</p>

      <input type="submit"
value="로그인" @onclick="checkIdPw()"
/>
    </form>
  </div>

  <div id="message">
    <h3>Password must contain the following:</h3>
    <p
id="letter" class="invalid">A <b>lowercase</b> letter</p>
    <p
id="capital" class="invalid">A <b>capital (uppercase)</b> letter</p>
    <p id="number"
class="invalid"
>
A <b>number</b>
</p>
    <p
id="length" class="invalid">Minimum <b>8 characters</b></p>
  </div>
</template>

<script lang="js">

export default
  {data() {
    return {
      idValue: '',
      pwValue: '',
      idInvalid: false,
      pwInvalid: false,

    }
  },
  methods: {
    checkIdPw(){
      this.idValue.length === 0 ? this.idInvalid = true : this.idInvalid = false;
      this.pwValue.length === 0 ? this.pwInvalid = true : this.pwInvalid = false;
    },
    getValue(event){
      console.log(hahaha);
      event.target.id==='id' ? this.idValue = event.target.innerHTML: this.pwValue = event.target.innerHTML;
      console.log(event.target.innerHTML)
    }

  }}
</script>
