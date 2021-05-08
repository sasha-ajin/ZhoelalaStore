var updateBtns = document.getElementsByClassName('update-cart')
for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
            var productId = this.dataset.product
            var action = this.dataset.action
            console.log(productId, action)
            console.log('User:', user)
            if (user === 'AnonymousUser') {
                addCoockieItem(productId, action)
            } else {
                updateUserOrder(productId, action)
            }
        }
    )
}

function addCoockieItem(productId, action) {
    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity': 1}

        } else {
            cart[productId]['quantity'] += 1
        }
    }

    if (action == 'remove') {
        cart[productId]['quantity'] -= 1

        if (cart[productId]['quantity'] <= 0) {
            console.log('Item should be deleted')
            delete cart[productId];
        }
    }
    console.log('CART:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

function updateUserOrder(productdId, action) {
    console.log('User is logged in')
    var url = '/update_item/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productdId, 'action': action})
    })

        .then((response) => {
            return response.json()

        })
        .then((data) => {
            console.log('data:', data)
            location.reload()
        })
}
