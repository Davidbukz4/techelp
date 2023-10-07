$(document).ready(() => {
    $("#loginForm").submit((e) => {
        e.preventDefault();

        let email = $("#email").val();
        let password = $("#password").val();

        let loginData = {
            email: email,
            password: password
        };

        $.ajax({
            url: "http://127.0.0.1:8000/api/login",
            type: "POST",
            data: loginData,
            dataType: "json",
            success: function (response) {
                if (response.token) {
                    console.log("Login successful", response);
                } else {
                    console.log("Login failed");
                }
            },
            error: function (error) {
                console.log("Error: " + error.statusText);
            }
        })
    })
})