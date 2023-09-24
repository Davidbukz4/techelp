$(document).ready(() => {
    $("#submit").click((e) => {
        e.preventDefault();

        let formData = new FormData($("#ticket-form"));

        $.ajax({
            url: "enter url",
            type: "POST",
            data: formData,
            success: function(response) {
                console.log("ticket submitted successfully");
                $("#ticket-form").replaceWith("<p>Ticket submitted successfully!</p>");
                window.location.href = "/"
            },
            error: function(error) {
                console.log(error);
            }
        })
    })
})