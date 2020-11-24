<template>
  <div class="container">
    <form action="/action_page.php">
      <label for="usrname">Username</label>
      <input
        :class="{invalid: }"
        type="text"
        id="usrname"
        name="usrname"
        required
        placeholder="셀러 아이디"
      >
      <p :class="{}">
아이디를 입력해주세요.
</p>

      <label for="psw">Password</label>
      <input
        :class="{}"
        type="password"
        id="psw"
        name="psw"
        pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
        title="Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters"
        required
        placeholder="셀러 비밀번호"
      >
      <p :class="{}">
비밀번호를 입력해주세요.
</p>

      <input type="submit"
value="로그인"
:onsubmit="submit"
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

export default (
methods : {

  submit(){
    fetch:
  }
}

)
</script>
