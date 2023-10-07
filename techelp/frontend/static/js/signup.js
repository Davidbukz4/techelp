$(document).ready(() => {

    $(".submit").click((e) => {
        e.preventDefault();

        let username = $("#username").val();
        let email = $("#email").val();
        let password = $("#password").val();
        let role;
        if ($("#enduser-role").is(":checked")) {
            role = "enduser";
        } else {
            role = "itsupport"
        }

        let signupData = {
            email: email,
            password: password,
            username: username,
            role: role
        };

        $.ajax({
            url: "http://127.0.0.1:8000/api/signup",
            type: "POST",
            data: signupData,
            dataType: "json",
            success: function (response) {
                if (response.token) {
                    console.log("Signup successful");
                } else {
                    console.log("Signup failed");
                }
            },
            error: function (error) {
                console.log("Error: " + error.statusText);
            }
        })
    })
})