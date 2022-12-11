/* jshint esversion: 8 */
/* jshint node: true */
/* jshint browser: true */
"use strict";

// const SERVER_URL = "http://kevin00co.pythonanywhere.com";
const SERVER_URL = "http://127.0.0.1:5000";

async function SignUp() {
  let username = document.getElementById("username").value;
  let studentid = document.getElementById("student-id").value;
  let email = document.getElementById("email").value;
  let phonenumber = document.getElementById("phone-number").value;
  let password = document.getElementById("password").value;
  let confirmPassword = document.getElementById("password-cf").value;
  let warn_msg = document.getElementById("message");
  // while (password != confirmPassword) {
  //   let warn_msg = document.createElement("div");
  //   warn_msg.innerHTML = "<p>The two passwords don't match</p>";
  //   warn_msg.setAttribute("class", "");
  //   filebody = document;
  //   password;
  // }

  // console.log(
  //   SERVER_URL +
  //     `/api/signup?username=${username}&student_id=${studentid}&email=${email}&phone_number=${phonenumber}&password=${password}&confirmPassword=${confirmPassword}`
  // );
  let request = await fetch(
    SERVER_URL +
      `/api/signup/${username}/${studentid}/${email}/${phonenumber}/${password}/${confirmPassword}`
  )
    .then((response) => response.json())
    .then((response) => {
      if (response.hasOwnProperty("error")) {
        warn_msg.innerText = response["error"].toString();
        warn_msg.setAttribute("class", "alert alert-danger");
      } else {
        if (response.status == "Successful") {
          let userName = response["currentUserName"];
          window.location.href = "base.html";
          let IdContainer = document.getElementById("username");
          IdContainer.innerText = userName.toString();
          IdContainer.innerText = userName.toString();
        }
      }
    });
}

async function SignIn() {
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;
  console.log(SERVER_URL + `/api/signin/${username}/${password}`);
  let SendObj = {};
  let request = await fetch(SERVER_URL + `/api/signin/${username}/${password}`)
    .then((response) => response.json())
    .then((response) => {
      // if (response.hasOwnProperty("error")) {
      //   warn_msg.innerText = response["error"].toString();
      //   warn_msg.setAttribute("class", "alert alert-danger");
      // } else {
      //   if (response.status == "Successful") {
      //     console.log(response.status);
      //     let userName = response["currentUserName"];
      //     window.location.href = "base.html";
      //     let IdContainer = document.getElementById("username");
      //     IdContainer.innerText = userName.toString();
      //     IdContainer.innerText = userName.toString();
      //   }
      // }
      console.log(response);
    });
}

async function CreateRequest() {
  let items = document.getElementById("item_list");
  const SendObj = {
    method: "POST",
  };
  SendObj["body"] = {};
  if (items.children.length == 0) return;
  for (const child of items.children) {
    if (items.children.length == 0) return;
    for (const child of items.children) {
      let child_string = child.innerText;
      child_string = child_string.toString();
      const child_array = child_string.split(",");
      console.log(child_array);
      SendObj["body"][child_array[0]] = child_array[1];
    }
    console.log(SendObj);
    let tprice = parseInt(document.getElementById("total-price").innerText);
    console.log(tprice);
    let userid = document.getElementById("username").innerText;
    console.log(userid);
    const d = new Date();
    let year = d.getFullYear();
    let date = d.getDate();
    let month = d.getMonth();
    let time = "";
    if (date < 10) {
      time = time + month + "0" + date + year;
    } else {
      time = time + month + date + year;
    }
    console.log(`/api/request/add/${userid}/${time}/${tprice}`);
    let request = await fetch(
      SERVER_URL + `/api/request/add/${userid}/${time}/${tprice}`,
      SendObj
    )
      .then((response) => response.json())
      .then((response) => {});
  }
}

async function SeeAllRequests() {
  let request = await fetch(
    // SERVER_URL + `/api/request/all`
    "json-test/all_request_sample.JSON"
  )
    .then((response) => response.json())
    .then((response) => {
      console.log(response);
      let tablebody = document.querySelector("#table > tbody");
      tablebody.innerHTML = "";
      console.log(tablebody.innerHTML);
      if (response.fectch_reqstatus == "Successful") {
        for (const data of response.data) {
          let row = document.createElement("tr");
          let user = document.createElement("td");
          user.innerText = data.user_id;
          row.appendChild(user);
          let reqstat = document.createElement("td");
          reqstat.innerText = data.request_status;
          row.appendChild(reqstat);
          let price = document.createElement("td");
          price.innerText = data.price;
          row.appendChild(price);
          let acceptbutton = document.createElement("td");
          acceptbutton.innerHTML = `<button class="btn" onclick="AcceptRequest(${data.request_id})">Accept It</button>`;
          row.appendChild(acceptbutton);
          let deletebutton = document.createElement("td");
          deletebutton.innerHTML = `<button class="btn" onclick="RemoveRequest(${data.request_id})">Accept It</button>`;
          row.appendChild(deletebutton);
          tablebody.appendChild(row);
        }
      }
    });
}

async function RemoveRequest(request_id) {
  JsonObj = {
    method: "POST",
    body: JSON.stringify(request_id),
  };
  let request = await fetch(
    SERVER_URL + `/api/request/remove/${request_id}`,
    JsonObj
  )
    .then((response) => response.json())
    .then((response) => {});
}

async function AcceptRequest(request_id) {
  let year = d.getFullYear();
  let date = d.getDate();
  let month = d.getMonth();
  let time = "";
  if (date < 10) {
    time = time + month + "0" + date + year;
  } else {
    time = time + month + date + year;
  }
  let userid = parseInt(document.getElementById("username"));
  let request = await fetch(
    SERVER_URL + `/api/request/accept/${request_id}/${userid}/${time}`
  )
    .then((response) => response.json())
    .then((response) => {});
}

function AddItem() {
  let item = document.getElementById("item").value;
  if (item == "") return;
  let quantity = document.getElementById("quantity").value;
  if (quantity == "") return;
  let price = document.getElementById("price").value;
  if (price == "") return;
  price = parseInt(price);
  let listingtop = document.getElementById("item_list");
  let listing = document.createElement("li");
  listing.innerText = `${item},${quantity}`;
  listingtop.appendChild(listing);
  let totalprice = parseInt(document.getElementById("total-price").innerText);
  totalprice = totalprice + price;
  document.getElementById("total-price").innerText = `${totalprice}`;
}
