// paypal.Buttons({
//
//     // Set up the transaction
//     createOrder: function (data, actions) {
//         return actions.order.create({
//             purchase_units: [{
//                 amount: {
//                     value: parseFloat(total).toFixed(2)
//                 }
//             }]
//         });
//     },
//
//     // Finalize the transaction
//     onApprove: function (data, actions) {
//         return actions.order.capture().then(function (details) {
//             // Show a success message to the buyer
//             submitFormData()
//             // alert('Transaction completed by ' + details.payer.name.given_name + '!');
//         });
//     }
//
//
// }).render('#paypal-button-container');


var form = document.getElementById('form')
csrftoken = form.getElementsByTagName("input")[0].value
console.log('NewToken:', form.getElementsByTagName("input")[0].value)

form.addEventListener('submit', function (e) {
    e.preventDefault()
    console.log('Form Submitted...')
    document.getElementById('form-button').classList.add("hidden");
    document.getElementById('payment-info').classList.remove("hidden");

})
document.getElementById('make-payment').addEventListener('click', function (e) {
    submitFormData()
})


function submitFormData() {

    var userFormData = {
        'name': form.name.value,
        'number': form.number.value,
        'total': total
    }
    var shippingFormData = {
        'oblast': form.oblast.value,
        'rayon': form.rayon.value,
        'gorod': form.gorod.value,
        'otdeleniye': form.otdeleniye.value

    }


    var url = "/process_order/"
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'applicaiton/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'form': userFormData, 'shipping': shippingFormData}),

    })
        .then((response) => response.json())
        .then((data) => {
            console.log('Success:', data);
            alert('Ваш заказ был оформлен,мы вам позвоним в течении часа');
            cart = {}
            document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
            window.location.href = "/"

        })
}
