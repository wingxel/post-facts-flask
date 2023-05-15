"use strict"

/**
*   https://wingxel.github.io/website
*    -----------------------------------
**/

/**
 * Check if the entered email address follows the convention email
 * format i.e email@dmn.com
 * @param {String} emailAddress 
 * @returns {Boolean}
 */
function isEmailValid(emailAddress) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailAddress)
}

/**
 * Generate a random number between 0 and max
 * @param {Integer} max 
 * @returns {Integer}
 */
function getRandom(max = 3) {
    return Math.floor(Math.random() * 3);
}

/**
 * Check if entered password has white space characters i.e
 * space, tab, newline e.t.c
 * @param {String} txt 
 * @returns {Boolean}
 */
function hasWhitespaceChar(txt) {
    return /\s/.test(txt);
}

/**
 * Check if the entered password has at least one none letter character i.e
 * !, @, #, $ e.t.c
 * @param {String} txt 
 * @returns {Boolean}
 */
function hasNoneChar(txt) {
    return /\W/.test(txt);
}

/**
 * Check if password is valid (Does not contain any white space character, 
 * contains al least one none letter character and has at least eight characters)
 * @param {String} txt 
 * @returns {Boolean}
 */
function isPasswordValid(txt) {
    return (!hasWhitespaceChar(txt) && hasNoneChar(txt) && txt.length >= 8);
}

/**
 * Alert user with the provided string using the provided color
 * @param {String} color
 * @param {String} txt 
 */
function showInfo(color, txt = "Sign-Up") {
    $("#Info").text(txt).css({
        "color": color
    });
}

/**
 * Check if the provided input field contain valid name
 * @param {HTMLElement} element 
 * @param {String} elmName 
 * @returns {Boolean}
 */
function validateName(element, elmName = "") {
    if (element.val().trim().length == 0) {
        showInfo("red", `${elmName} cannot be empty!`);
        element.val("")
        return false;
    } else {
        showInfo("white");
    }
    return true;
}

/**
 * Check if provided input field contains valid email address
 * @param {HTMLElement} element 
 * @returns {Boolean}
 */
function validateEmail(element) {
    if (!isEmailValid(element.val())) {
        showInfo("red", "Email is not valid");
        return false;
    } else {
        showInfo("white")
    }
    return true;
}

/**
 * Check if the provided input field contains valid password
 * @param {HTMLElement} element 
 * @returns {Boolean}
 */
function validatePassword(element) {
    let ok = false;
    if (element.val().length < 8) {
        showInfo("red", "Password should have at least 8 characters");
    } else if (!hasNoneChar(element.val())) {
        showInfo("red", "Password should contain at least on none letter character");
    } else if (hasWhitespaceChar(element.val())) {
        showInfo("red", "Password should not contain whitespace characters");
    } else if (isPasswordValid(element.val())) {
        showInfo("white");
        ok = true;
    }
    return ok;
}

/**
 * Check if the confirmation password matches the entered password
 * @param {HTMLElement} element 
 * @returns {Boolean}
 */
function confirmPasswd(element) {
    if ($("#Password").val() !== element.val()) {
        showInfo("red", "Password does not match");
        return false;
    } else {
        showInfo("white");
    }
    return true;
}

/**
 * Redirect the user accordingly
 * @param {String} resp 
 * @param {String} redirectUrl 
 * @param {String} txt 
 */
function procResp(resp, redirectUrl = "", txt = "Success") {
    if (resp == "success") {
        showInfo("green", txt);
        setTimeout(() => {
            showInfo("white", "");
            location.assign(redirectUrl);
        }, 2000);
    } else {
        showInfo("red", resp);
    }
}

/**
 * Check if the provided image is valid (is not empty, the size is less than 3MB)
 * @param {HTMLElement} element 
 * @returns {Boolean}
 */
function checkImage(element) {
    let imgOk = false;
    let f = element.prop("files")[0];
    if (element.val() === "") {
        showInfo("red", "Please select profile image");
    } else if (f["size"] > (3 * 1024 * 1024)) {
        showInfo("red", "Profile image should be less than 3MB")
    } else {
        imgOk = true;
        showInfo("white")
    }
    return imgOk;
}

/**
 * Wait until the webpage is completely loaded
 */
$(() => {
    // --------------------Temp nav bar stuff--------------------------------------
    // You can delete
    $("#CopyRT").text(`${new Date().getFullYear()}`);
    const u = [
        "https://play.google.com/store/apps/details?id=com.wingxel.python",
        "https://wingxel.github.io/website/index.html",
        "https://github.com/wingxel"
    ];
    $(".mt-z0-wg").on("click", event => {
        o21l(u[getRandom()]);
        event.preventDefault();
    });

    // ---------------------------------------------------------------------------

    // Opens new tab to load to rate the app in Google play store
    const o21l = li => {
        let w = window.open(li, "_blank");
        if (w) {
            w.focus();
        } else {
            alert("Loading failed : Please allow website to open new tabs:)");
        }
    };


    $(".lg-ut-m").on("click", event => {
        // Load confirmation prompt --1--
        let ans = confirm("You want to logout?\n" +
            "Please support the app by rating 5 stars on play store " + String.fromCodePoint(0x1F642));
        if (ans) {
            setTimeout(() => {
                location.assign("/logout");
            }, 1500);
            // open new tab to rate
            o21l(u[0]);
        } else {
            o21l(u[0]);
        }
        // comment/delete from 'Load confirmation prompt --1--' and uncomment the next line
        // location.assign("/logout");
        event.preventDefault();
    });

    // Submit sign-up form data to the backend using ajax
    $("#SignUp").submit(e => {
        if (validateName($("#FirstName")) &&
            validateName($("#LastName")) &&
            validateName($("#Username")) &&
            validateEmail($("#Email")) &&
            validatePassword($("#Password")) &&
            confirmPasswd($("#ConfirmPassword")) &&
            checkImage($("#Profile"))) {

            let data = new FormData()
            data.append("fName", $("#FirstName").val());
            data.append("lName", $("#LastName").val());
            data.append("uName", $("#Username").val().trim());
            data.append("email", $("#Email").val());
            data.append("pwd", $("#Password").val());
            data.append("csrf_token", $("#CSRF").val())
            data.append("profile", $("#Profile").prop("files")[0])

            $.ajax({
                type: "POST",
                url: "/sign-up",
                data: data,
                processData: false,
                contentType: false,
                success: function (response) {
                    procResp(response, "/login-pg?signup")
                }
            });
        }
        e.preventDefault();
    });

    // Submit login form data to the backend for authentication using ajax
    $("#Login").submit(e => {

        let data = new FormData();
        data.append("uName", $("#Username").val().trim())
        data.append("pwd", $("#Password").val())
        data.append("csrf_token", $("#CSRF").val())

        $.ajax({
            type: "POST",
            url: "/login",
            data: data,
            processData: false,
            contentType: false,
            success: function (response) {
                procResp(response, "/");
            }
        });

        e.preventDefault();
    });

    // Submit post fact form data to the backend using ajax
    $("#PostFact").submit(e => {
        if ($("#Fact").val().trim().length > 0) {
            let data = new FormData();
            data.append("fact", $("#Fact").val().trim());
            data.append("csrf_token", $("#CSRF").val());
            $.ajax({
                type: "POST",
                url: "/postFact",
                data: data,
                processData: false,
                contentType: false,
                success: function (response) {
                    procResp(response, "/index");
                }
            });
        } else {
            showInfo("red", "Please enter the required information");
        }
        e.preventDefault();
    });

    // Add click event listeners for all like buttons
    const forms = document.querySelectorAll(".like-form");
    for (let item of Array.from(forms)) {
        item.addEventListener("submit", e => {
            // Submit like form data to the backend using ajax
            let csrf_token = item.elements.csrf_token.value;
            let factId = item.elements.fact_id.value;
            const data = new FormData();
            data.append("csrf_token", csrf_token);
            data.append("factId", factId);
            $.ajax({
                type: "POST",
                url: "/like",
                data: data,
                processData: false,
                contentType: false,
                success: function (response) {
                    if (response === "failed") {
                        // Don't create more than one error alert
                        if ($("#lkFailed").length === 0) {
                            let errItem = $('<div id="lkFailed"><p>Please make sure your are logged in!</p></div>');
                            errItem.css({
                                "background-color": "black",
                                "color": "red",
                                "margin-top": "10px"
                            });
                            $(`#${factId}`).append(errItem);
                            setTimeout(() => $(errItem).remove(), 2000);
                            }
                    } else {
                        $(`#${factId}`).text(response);
                        let current = item.elements.actionBtn.value;
                        if (current == "Like") {
                            item.elements.actionBtn.value = "Undo";
                        } else {
                            item.elements.actionBtn.value = "Like";
                        }
                    }
                }
            });
            e.preventDefault();
        });
    }

    // Close/collapse-back the navigation drop down
    $("#navbarSupportedContent").on("show.bs.collapse", () =>
        $("a.nav-link").click(() => $("#navbarSupportedContent").collapse("hide"))
    );
});