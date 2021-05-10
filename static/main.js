// to mark the active page on navbar
$(document).ready(function() {
    $(".navbar-nav .nav-link .active-link").removeClass("active");
    $(".navbar-nav .nav-link").each(function() {
        if (this.href === window.location.href) {
            $(this).addClass("active-link");
        }
    });
});


// auto collapse navbar when user clicks outside it
$(document).ready(function () {
    $(".main-content").click(function () {
        var is_expanded = $(".navbar-collapse").hasClass("show");
        if (is_expanded && !$(".navbar-toggler").hasClass("collapsed")) {
            $(".navbar-collapse").removeClass("show");
        }
    });
});


// to show password 
function toggleView() {
    let toggleInput = document.getElementById('pass');
    let toggleButton = document.getElementById('toggle');

    if (toggleInput.type === "password" && toggleButton.checked) {
        toggleInput.type = "text";
    } else {
        toggleInput.type = "password";
    }
}


// validate password when user starts to type inside the password field
function validatePassword() {
    var confirm = document.getElementById("confirm");
    var pass = document.getElementById("pass");
    var letter = document.getElementById("letter");
    var number = document.getElementById("number");
    var special = document.getElementById("special");
    var length = document.getElementById("length");
    var match = document.getElementById("match");

    // check if password has letters
    var upper = /[A-Z]/g;
    var lower = /[a-z]/g;
    if (pass.value.match(upper) && pass.value.match(lower)) {
        changeClass(letter, "invalid", "valid");
    } else {
        changeClass(letter, "valid", "invalid");
    }

    // check if password has numbers
    var numbers = /[0-9]/g;
    if (pass.value.match(numbers)) {
        changeClass(number, "invalid", "valid");
    } else {
        changeClass(number, "valid", "invalid");
    }

    // check password length
    if (pass.value.length >= 8) {
        changeClass(length, "invalid", "valid");
    } else {
        changeClass(length, "valid", "invalid");
    }

    // check if password has special characters
    var specialChars = /[!@#$%^&*()-+/]/g;
    if (pass.value.match(specialChars)) {
        changeClass(special, "invalid", "valid");
    } else {
        changeClass(special, "valid", "invalid");
    }

    // check if passwords match 
    if (pass.value != "" && pass.value === confirm.value) {
        changeClass(match, "invalid", "valid");
    } else {
        changeClass(match, "valid", "invalid");
    }


    // if password satisfies all the requirements, enable the submit button
    if (passwordPassedAllChecks(letter, number, special, length, match)) {
        document.getElementById("create_pass").disabled = false;
    } else {
        document.getElementById("create_pass").disabled = true;
    }
}


// function to change classname of an element
function changeClass(element, oldClassName, newClassName) {
    element.classList.remove(oldClassName);
    element.classList.add(newClassName);
}


// check if entered password passes all checks
function passwordPassedAllChecks(...testCases) {
    var passedChecks = 0;
    testCases.forEach(function(test) {
        if (test.classList.contains("valid")) {
            passedChecks++;
        }
    });
    
    if (passedChecks === testCases.length) {
        return true;
    } else {
        return false;
    }
}


// to display price according to plan type
function displayPrice(input) {
    var planName = input.value;
    var planPrice = document.getElementById("plan-price"); 

    if (planName === "STARTER") {
        planPrice.innerHTML = "&nbsp;&nbsp;$15";
    } else if (planName === "PROFESSIONAL") {
        planPrice.innerHTML = "&nbsp;&nbsp;$25";
    } else if (planName === "ENTERPRISE") {
        planPrice.innerHTML = "&nbsp;&nbsp;$50";
    }
}


// Ajax form submission
function sendAjaxRequestToServer(formId, formAction) {
    $(formId).on('submit', function(event) { 
        event.preventDefault();
        var offset = new Date().getTimezoneOffset();

        $.ajax({
            url: formAction,
            type: "POST", 
            data: $(formId).serialize() + "&offset=" + offset,
        
            success : function(json) {
                if (json.status == 1) {
                    // Show the alert right after the input
                    $(json.alertInputId).after(
                        "<div class='info custom-alert'>" + json.msg + "</div>"
                    );
                   
                    // Auto hide the alert
                    setTimeout(function() {
                        $('.custom-alert').fadeOut('slow', function() {
                            $(this).remove(); 
                        });
                    }, 3000);
                } else {
                    window.location.assign(json.redirectUrl);
                }
            }
        });
    });
}


// AJAX request to server
$(document).ready(function() {    
    sendAjaxRequestToServer("#feedback-form", "/contact/");
    sendAjaxRequestToServer("#login-form", "/login/");

    // User registration
    sendAjaxRequestToServer("#enter-mail", "/register/");
    sendAjaxRequestToServer("#validate-mail", "/account/validate_mail/");
    sendAjaxRequestToServer("#open-account", "/account/open_account/");
    sendAjaxRequestToServer("#create-pass", "/account/create_password/");
    sendAjaxRequestToServer("#select-plan", "/account/select_plan/");

    // Change password
    sendAjaxRequestToServer("#confirm-mail", "/account/confirm_mail/");
    sendAjaxRequestToServer("#change-pass", "/account/change_password/");

    // Stock quote, buy and sell
    sendAjaxRequestToServer("#stock-quote", "/user/stocks/quote/");
    sendAjaxRequestToServer("#stock-buy", "/user/stocks/buy/");
    sendAjaxRequestToServer("#stock-sell", "/user/stocks/sell/");
});


// Alert auto close
window.setTimeout(function() {
    $(".alert-auto-close").fadeTo(500, 0).slideUp(500, function(){
        $(this).remove(); 
    });
}, 3000);


// To show bio when user clicks on dropdown
$(document).ready(function() {
    var elements = document.getElementsByClassName("show-bio");

    for (var i = 0; i < elements.length; i++) {
        elements[i].querySelector("a").onclick = function () {
            if (this.parentNode.parentNode.querySelector(".bio-desc").style.display == "block") {
                this.innerHTML = "Bio<i class='fas fa-angle-down'></i>";
                this.parentNode.parentNode.querySelector(".bio-desc").style.display = "none";
            } else {
                this.innerHTML = "Bio<i class='fas fa-angle-up'></i>";
                this.parentNode.parentNode.querySelector(".bio-desc").style.display = "block";
            }
            return false;
        };
    }
});


// Filter stock table
$(document).ready(function(){
    $("#filter-stocks").on('change', function() {
        var filter = $(this).val().toLowerCase();

        if (filter === "cs") {
            filter = "Common stock";
        } else if (filter === "ps") {
            filter = "Preferred stock";
        } else if (filter === "adr") {
            filter = "ADR";
        } 

        $("#stocks-table td:nth-child(4)").each(function() {
            if (filter === "all") {
                $(this).parent().show();
            } else if ($(this).text() === filter) {
                $(this).parent().show();
            } else {
                $(this).parent().hide();
            }
        });
    });
});


// Resize pagination for small screen
function resizePagination() {
    if ($(window).width() < 580) {
        $(".pagination").addClass("pagination-sm");
    } else {
        $(".pagination").removeClass("pagination-sm");
    }
}


// Add event listener for the function
$(document).ready(resizePagination);
$(window).resize(resizePagination);