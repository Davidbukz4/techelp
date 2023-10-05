$(document).ready(() => {
    $("#submit").click((e) => {
        e.preventDefault();

        let formData = new FormData($("#ticket-form")[0]);

        $.ajax({
            url: "127.0.0.1:8000/api/create",
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log("ticket submitted successfully");
                $("#ticket-form").replaceWith("<p>Ticket submitted successfully!</p>");
                // window.location.href = "/"
            },
            error: function(error) {
                console.log(error);
                console.log(formData)
            }
        })
    })
})