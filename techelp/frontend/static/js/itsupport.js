$(document).ready(() => {
    

    $(".saveBtn").click(() => {
        let now = new Date();
        let resolvedDate = now.toLocaleTimeString() + " " + now.toLocaleDateString();

        if ($("#checkbox").is(":checked") || $(".status").val() !== "") {
            $.ajax({
                url: "enter url",
                type: "PUT",
                data: {
                    resolved_at: resolvedDate,
                    status: $(".status").val()
                },
                success: function(response) {
                    console.log("Ticket updated!");
                },
                error: function(error) {
                    console.log("Error updating ticket:", error);
                }
            })
        }
    })

    $(".deleteBtn").click(() => {
        // get the ticket ID
        let ticketId = $(this).closet("li").attr("id")

        $.ajax({
            url: "enter url",
            type: "DELETE",
            success: (response) => {
                $(this).closest("li").remove();
            },
            error: (error) => {
                console.log(error);
            }
        })
    })

    $(".searchBtn").click((e) => {
        let filter = $("#filter").val()
        let searchTerm = $("#search").val();

        let url = "enter url"
        if (filter !== "none") {
            url += "?filter=" + filter;
        }
        if (searchTerm !== "") {
            url += "&search=" + searchTerm;
        }

        $.ajax({
            url: url,
            type: "GET",
            success: (response) => {
                renderSearch(response);
            },
            error: (error) => {
                console.log(error);
            }
        })
    })

    function renderSearch(data) {
        // clear the ticket list
        $("#ticket-list").empty();

        // Add each ticket to the list
        for (let i = 0; i < data.length; i++) {
            let ticket = data[i];

            // Create a new list item element
            var listItem = $("<li>");

            // status dropdown
            let dropdown = '<select name="status">' +
                    '<option value="" disabled>Select Status</option>' +
                    '<option value="open"' + checkStatus("Open") + '>Open</option>' +
                    '<option value="in_progress"' + checkStatus("In Progress") + '>In Progress</option>' +
                    '<option value="completed"' + checkStatus("Completed") + '>Completed</option> </select>'

            function checkStatus(status) {
                if (status === ticket.status) {
                    return "selected";
                } else {
                    return "";
                }
            }

            // Add the ticket details to the list item element
            listItem.append("<h3>Title: " + ticket.title + "</h3>");
            listItem.append("<p>Description: " + ticket.description + "</p>");
            listItem.append("<p>Priority: " + ticket.priority + "</p>");
            listItem.append("<p>Status: " + dropdown + "</p>");
            listItem.append("<p>Category: " + ticket.category + "</p>");
            listItem.append("<p>Owner: " + ticket.owner + "</p>");
            listItem.append("<p>Created date: " + ticket.created_date + "</p>");
            listItem.append("<p>Resolved date: " + ticket.resolved_date + "</p>");
            listItem.append("<input type='checkbox' >")
            listItem.append("<button class='viewBtn'>View Attachment</button>");
            listItem.append("<button class='saveBtn'>Save Changes</button>");
            listItem.append("<button class='deleteBtn'>Delete</button>");

            // Add the list item element to the ticket list
            $("#ticket-list").append(listItem);
        }
    }

    
})