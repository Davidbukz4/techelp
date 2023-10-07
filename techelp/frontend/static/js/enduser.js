$(document).ready(() => {
    function renderTickets() {
        $.ajax({
            url: "http://127.0.0.1:8000/api/tickets",
            type: "GET",
            dataType: "json",
            success: function (response) {
                $("#user-id").data("user-id", response.user_id);
                $("#user-id").text(response.user_id);
                console.log(response)
                // response.tickets.forEach(function(ticket) {
                //     let rowHtml = `<tr>
                //     <td class="nowrap">ticket one title</td>
                //     <td>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Magnam, alias repudiandae sit sint recusandae maxime quas dolores iure repellendus assumenda. Dignissimos maxime vero quae, dolorem ad similique amet voluptatum commodi!</td>
                //     <td class="centered-text">High</td>
                //     <td class="nowrap centered-text">In progress</td>
                //     <td class="centered-text">Software</td>
                //     <td class="centered-text">User1</td>
                //     <td class="nowrap centered-text">20-sept-2022</td>
                //     <td class="centered-text">view</td>
                //     <td class="nowrap centered-text">20-sept-2022</td>
                // </tr>`;
                // $("#ticket-list").append(rowHtml);
                // })
            },
            error: function(error) {
                console.log("Error: " + error.statusText);
            }
        })
    }

    renderTickets();

    $("#tickets").click(function (e) {
        e.preventDefault();
        renderTickets();
    })

    $("#create").click(function (e) {
        e.preventDefault();
        //
    })

    $("#signout").click(function (e) {
        e.preventDefault();
        //
    })

})