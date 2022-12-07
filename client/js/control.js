/* jshint esversion: 8 */
/* jshint node: true */
/* jshint browser: true */
"use strict";

const SERVER_URL = "";

async function SignUp() {
  let username = document.getElementById("username").value;
  let studentid = document.getElementById("student-id").value;
  let email = document.getElementById("email").value;
  let phonenumber = document.getElementById("phone-number").value;
  let password = document.getElementById("password").value;
  let confirmPassword = document.getElementById("password-cf").value;
  console.log(
    SERVER_URL +
      `/api/signup?username=${username}&student_id=${studentid}&email=${email}&phone_number=${phonenumber}&password=${password}&confirmPassword=${confirmPassword}`
  );
  //   let request = await fetch(SERVER_URL + `/api/signup/?username=${username}&student_id=${studentid}&email=${email}&phone_number=${phonenumber}&password=${password}&confirmPassword=${confirmPassword}`)
  //     .then((response) => response.json())
  //     .then((response) => {

  //     })
}
