"use strict";

var updateBtns = document.getElementsByClassName('update-cart');

for (i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener('click', function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;
    console.log('productId:', productId, 'Action:', action);
    console.log('USER:', user);

    if (user == 'AnonymousUser') {
      addCookieItem(productId, action);
    } else {
      updateUserOrder(productId, action);
    }
  });
}

function updateUserOrder(productId, action) {
  console.log('User is authenticated, sending data...');
  var url = "/update_item/";
  $.ajax({
    type: 'POST',
    url: url,
    headers: {
      'Content-Type': 'application/json',
      "X-CSRFTOKEN": csrftoken
    },
    data: JSON.stringify({
      'productId': productId,
      'action': action
    }),
    success: function success(data) {
      if (data.action) {
        window.location.href = "/Courses/Cart/?checkout='true'"; //document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
      } else {
        console.log(data.action + " " + "deleted");
        delete cart[data.product_id]; //window.location.reload();
      }
    },
    error: function error(data) {
      swal("NOT Deleted!", "Something blew up.", "error");
    }
  }); // fetch(url, {
  // 	method:'POST',
  // 	headers:{
  // 		'Content-Type':'application/json',
  // 		'X-CSRFToken':csrftoken,
  // 	}, 
  // 	body:JSON.stringify({'productId':productId, 'action':action})
  // })
  // .then((response) => {
  // 	console.log(response)
  //    return response.json();
  // })
  // .then((data) => {
  // 	if (data.action){
  // 		window.location.href="/Courses/Cart/?checkout='true'";
  // 		//document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
  // 	}
  // 	else{
  // 		console.log(data.action+" "+"deleted")
  // 		delete cart[data.product_id];
  // 		//window.location.reload();
  // 	}
  // });
}

function addCookieItem(productId, action) {
  console.log('User is not authenticated');

  if (action == 'add') {
    if (cart[productId] == undefined) {
      cart[productId] = {
        'quantity': 1
      };
    }
  }

  if (action == 'remove') {
    cart[productId]['quantity'] -= 1;
    delete cart[productId];
  }

  console.log('CART:', cart);
  document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
  window.location.href = '/Courses/Cart/';
}