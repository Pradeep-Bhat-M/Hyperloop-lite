// function validate(e) {

//     //Email varification
//     var emailID = document.registerForm.email.value;
//     atpos = emailID.indexOf("@");
//     dotpos = emailID.lastIndexOf(".");

//     if (atpos < 1 || (dotpos - atpos < 2)) {
//         document.getElementById("errorText").innerHTML = "Please enter correct email ID !";
//         document.registerForm.email.focus();
//         return false;
//     }

//     //username varification
//     var username = document.registerForm.username.value;
//     var patt1 = /\W/g;
//     var result = username.search(patt1);
//     if (result != -1) {
//         document.getElementById("error_text").innerHTML = "Username sholud not contain any special character except '_' !";
//         document.registerForm.username.focus();
//         return false;
//     }

//     //password strength checking
//     var password1 = document.registerForm.password.value;
//     if (password1.length < 8) {
//         document.getElementById("errorText").innerHTML = "Password sholud contain atleast 8 letter!";
//         document.registerForm.password.focus();
//         return false;
//     }

//     var pat = /[0-9]/g
//     if (!password1.match(pat)) {
//         document.getElementById("errorText").innerHTML = "Password sholud contain atleast a Digit!";
//         document.registerForm.password.focus();
//         return false;
//     }

//     var pat2 = /[a-z]/g
//     if (!password1.match(pat2)) {
//         document.getElementById("errorText").innerHTML = "Password sholud contain atleast One Lower case letter!";
//         document.registerForm.password.focus();
//         return false;
//     }

//     var pat3 = /[A-Z]/g
//     if (!password1.match(pat3)) {
//         document.getElementById("errorText").innerHTML = "Password sholud contain atleast One Uppercase character letter!";
//         document.registerForm.password.focus();
//         return false;
//     }

//     var pat4 = /\W/g;
//     var pat5 = /_/g;
//     if (!(password1.match(pat4) || password1.match(pat5))) {
//         document.getElementById("errorText").innerHTML = "Password sholud contain atleast One special character!";
//         document.registerForm.password.focus();
//         return false;
//     }

//     var password2 = document.registerForm.c_password.value;
//     if (password1 != password2) {
//         document.getElementById("errorText").innerHTML = "Password did not match !";
//         document.registerForm.c_password.focus();
//         return false;
//     }
// }

    function cardFinder() {

        var owner = $('#owner');
        var cardNumber = $('#cardNumber');
        var cardNumberField = $('#card-number-field');
        var CVV = $("#cvv");
        var mastercard = $("#mastercard");
        var confirmButton = $('#confirm-purchase');
        var visa = $("#visa");
        var amex = $("#amex");
    
        // Use the payform library to format and validate
        // the payment fields.
    
        cardNumber.payform('formatCardNumber');
        CVV.payform('formatCardCVC');
    
    
        cardNumber.keyup(function() {
    
            amex.removeClass('transparent');
            visa.removeClass('transparent');
            mastercard.removeClass('transparent');
    
            if ($.payform.validateCardNumber(cardNumber.val()) == false) {
                cardNumberField.addClass('has-error');
            } else {
                cardNumberField.removeClass('has-error');
                cardNumberField.addClass('has-success');
            }
    
            if ($.payform.parseCardType(cardNumber.val()) == 'visa') {
                mastercard.addClass('transparent');
                amex.addClass('transparent');
            } else if ($.payform.parseCardType(cardNumber.val()) == 'amex') {
                mastercard.addClass('transparent');
                visa.addClass('transparent');
            } else if ($.payform.parseCardType(cardNumber.val()) == 'mastercard') {
                amex.addClass('transparent');
                visa.addClass('transparent');
            }
        });
    
        confirmButton.click(function(e) {
    
            e.preventDefault();
    
            var isCardValid = $.payform.validateCardNumber(cardNumber.val());
            var isCvvValid = $.payform.validateCardCVC(CVV.val());
    
            if(owner.val().length < 5){
                alert("Wrong owner name");
            } else if (!isCardValid) {
                alert("Wrong card number");
            } else if (!isCvvValid) {
                alert("Wrong CVV");
            } else {
                // Everything is correct. Add your form submission code here.
                alert("Everything is correct");
            }
        });
    }