/* jshint esversion: 8 */
/* jshint node: true */
/* jshint browser: true */
"use strict";

const SERVER_URL = "http://kevin00co.pythonanywhere.com";
// const SERVER_URL = "http://127.0.0.1:5000";
var USERNAME = "";
var USERID = "";

async function SignUp() {
  let username = document.getElementById("username").value;
  let studentid = document.getElementById("student-id").value;
  let email = document.getElementById("email").value;
  let phonenumber = document.getElementById("phone-number").value;
  let password = document.getElementById("password").value;
  let confirmPassword = document.getElementById("password-cf").value;
  let warn_msg = document.getElementById("message");
  console.log(
    SERVER_URL +
      `/api/signup/${username}/${studentid}/${email}/${phonenumber}/${password}/${confirmPassword}`
  );
  let request = await fetch(
    SERVER_URL +
      `/api/signup/${username}/${studentid}/${email}/${phonenumber}/${password}/${confirmPassword}`
  )
    .then((response) => response.json())
    .then((response) => {
      console.log(response);
      if (response.hasOwnProperty("error")) {
        warn_msg.innerText = response["error"].toString();
        warn_msg.setAttribute(
          "class",
          "container d-flex justify-content-center"
        );
        warn_msg.classList.add("alert");
        warn_msg.classList.add("alert-danger");
        setTimeout(() => {
          warn_msg.classList.remove("alert");
          warn_msg.classList.remove("alert-danger");
          warn_msg.innerText = "";
        }, 2000);
      } else {
        if (response.status == "Successful") {
          USERNAME = response["currentUserName"];
          USERID = response["currentUserID"];
          location = "./base.html";
        } else {
          warn_msg.innerText = response.toString();
          warn_msg.setAttribute(
            "class",
            "container d-flex justify-content-center"
          );
          warn_msg.classList.add("alert");
          warn_msg.classList.add("alert-danger");
          setTimeout(() => {
            warn_msg.classList.remove("alert");
            warn_msg.classList.remove("alert-danger");
            warn_msg.innerText = "";
          }, 2000);
        }
      }
    })
    .then((error) => {
      console.log(error);
    });
}

async function SignIn() {
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;
  let warn_msg = document.getElementById("message");
  console.log(SERVER_URL + `/api/signin/${username}/${password}`);
  let request = await fetch(SERVER_URL + `/api/signin/${username}/${password}`)
    .then((response) => response.json())
    .then((response) => {
      if (response.hasOwnProperty("error")) {
        warn_msg.innerText = response["error"].toString();
        warn_msg.setAttribute(
          "class",
          "container d-flex justify-content-center"
        );
        warn_msg.classList.add("alert");
        warn_msg.classList.add("alert-danger");
        setTimeout(() => {
          warn_msg.classList.remove("alert");
          warn_msg.classList.remove("alert-danger");
          warn_msg.innerText = "";
        }, 2000);
      }
      if (response["status"] == "Successful") {
        localStorage.setItem("UserName", response["currentUserName"]);
        localStorage.setItem("UserID", response["currentUserID"]);
        location = "./base.html";
      } else {
        warn_msg.innerText = response.toString();
        warn_msg.setAttribute(
          "class",
          "container d-flex justify-content-center"
        );
        warn_msg.classList.add("alert");
        warn_msg.classList.add("alert-danger");
        setTimeout(() => {
          warn_msg.classList.remove("alert");
          warn_msg.classList.remove("alert-danger");
          warn_msg.innerText = "";
        }, 2000);
      }
    });
}

async function CreateRequest() {
  let item = document.getElementById("item");
  item.value = "";
  let quantity = document.getElementById("quantity");
  quantity.value = "";
  let price = document.getElementById("price");
  price.value = "";
  let items = document.getElementById("item_list");
  const SendObj = {
    method: "POST",
  };
  SendObj["body"] = {};
  if (items.children.length == 0) return;
  if (items.children.length == 0) return;
  for (const child of items.children) {
    let child_string = child.innerText;
    child_string = child_string.toString();
    const child_array = child_string.split(",");
    SendObj["body"][child_array[0]] = child_array[1];
  }
  let tprice = parseInt(document.getElementById("total-price").innerText);
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
  items.innerHTML = "Item list (if any)";
  let totalprice = document.getElementById("total-price");
  totalprice.innerHTML = "0";
  // console.log(
  //   SERVER_URL +
  //     `/api/request/add/${localStorage.getItem("UserID")}/${time}/${tprice}`
  // );
  console.log(SendObj);
  let request = await fetch(
    SERVER_URL +
      `/api/request/add/${localStorage.getItem("UserID")}/${time}/${tprice}`,
    SendObj
  )
    .then((response) => response.json())
    .then((response) => {
      let msg = document.querySelector("#message");
      if (response["status"] == "Successful") {
        msg.innerText = "Request (seems to have been) Created. Thank you";
        msg.classList.add("alert");
        msg.classList.add("alert-success");
        setTimeout(() => {
          msg.classList.remove("alert");
          msg.classList.remove("alert-success");
          msg.innerText = "";
        }, 2000);
      } else {
        console.log(response);
        msg.innerText =
          "Something unexpected happened. Sorry for this Inconvenience";
        msg.setAttribute("class", "container d-flex justify-content-center");
        msg.classList.add("alert");
        msg.classList.add("alert-danger");
        setTimeout(() => {
          msg.classList.remove("alert");
          msg.classList.remove("alert-danger");
          msg.innerText = "";
        }, 2000);
      }
    })
    .then((error) => {
      console.log(error);
    });
}

async function SeeAllRequests() {
  let request = await fetch(
    SERVER_URL + `/api/request/all`
    // "json-test/all_request_sample.JSON"
  )
    .then((response) => response.json())
    .then((response) => {
      let table = document.querySelector("#table");
      table.innerHTML = "";
      let tablehead = document.createElement("thead");
      let headrow = document.createElement("tr");

      let userhead = document.createElement("th");
      userhead.innerText = "Request ID";
      headrow.appendChild(userhead);

      let statushead = document.createElement("th");
      statushead.innerText = "Request Status";
      headrow.appendChild(statushead);

      let pricehead = document.createElement("th");
      pricehead.innerText = "Price";
      headrow.appendChild(pricehead);

      let accepthead = document.createElement("th");
      accepthead.innerText = "Accept";
      headrow.appendChild(accepthead);

      let removehead = document.createElement("th");
      removehead.innerText = "Remove";
      headrow.appendChild(removehead);

      tablehead.appendChild(headrow);
      table.appendChild(tablehead);

      let tablebody = document.createElement("tbody");
      table.appendChild(tablebody);
      tablebody.innerHTML = "";
      for (const data of response) {
        let row = document.createElement("tr");
        let user = document.createElement("td");
        user.innerText = data[0].id;
        row.appendChild(user);
        let reqstat = document.createElement("td");
        reqstat.innerText = data[0].request_status;
        row.appendChild(reqstat);
        let price = document.createElement("td");
        price.innerText = data[0].price;
        row.appendChild(price);
        let acceptbutton = document.createElement("td");
        acceptbutton.innerHTML = `<button class="btn btn-outline-primary" onclick="AcceptRequest(${data[0].id})">Accept It</button>`;
        row.appendChild(acceptbutton);
        let deletebutton = document.createElement("td");
        deletebutton.innerHTML = `<button class="btn btn-outline-primary" onclick="RemoveRequest(${data[0].id})">Remove It</button>`;
        row.appendChild(deletebutton);
        tablebody.appendChild(row);
      }
    });
}

async function RemoveRequest(request_id) {
  const JsonObj = {
    method: "POST",
    body: JSON.stringify(request_id),
  };
  let request = await fetch(
    SERVER_URL + `/api/request/remove/${request_id.toString()}`,
    JsonObj
  ).then((response) => {
    if (response.status == "200") {
      let msg = document.querySelector("#message");
      msg.innerText = "Request (seems to be) Removed. Thank you";
      msg.classList.add("alert");
      msg.classList.add("alert-success");
      setTimeout(() => {
        msg.classList.remove("alert");
        msg.classList.remove("alert-success");
        msg.innerText = "";
      }, 2000);
    }
  });
}

async function AcceptRequest(request_id) {
  let d = new Date();
  let year = d.getFullYear();
  let date = d.getDate();
  let month = d.getMonth();
  let time = "";
  if (date < 10) {
    time = time + month + "0" + date + year;
  } else {
    time = time + month + date + year;
  }
  let request = await fetch(
    SERVER_URL +
      `/api/request/accept/${request_id}/${localStorage.getItem(
        "UserID"
      )}/${time}`
  ).then((response) => {
    if (response.status == "200") {
      let msg = document.querySelector("#message");
      msg.innerText = "Request (seems to be) accepted. Thank you";
      msg.classList.add("alert");
      msg.classList.add("alert-success");
      setTimeout(() => {
        msg.classList.remove("alert");
        msg.classList.remove("alert-success");
        msg.innerText = "";
      }, 2000);
    }
  });
}

function AddItem() {
  let item = document.getElementById("item");
  if (item == "") return;
  let quantity = document.getElementById("quantity");
  if (quantity == "") return;
  let price = document.getElementById("price");
  if (price == "") return;
  price = parseInt(price.value);
  let listingtop = document.getElementById("item_list");
  let listing = document.createElement("li");
  listing.innerText = `${item.value},${quantity.value}`;
  listingtop.appendChild(listing);
  let totalprice = parseInt(document.getElementById("total-price").innerText);
  totalprice = totalprice + price;
  document.getElementById("total-price").innerText = `${totalprice}`;
}

async function SignOut() {
  let request = await fetch(SERVER_URL + `/api/logout`).then((response) => {
    localStorage.clear();
    location = "./index.html";
  });
}

function showUserName() {
  let showdiv = document.querySelector("#username");
  showdiv.innerText = localStorage.getItem("UserName");
}
