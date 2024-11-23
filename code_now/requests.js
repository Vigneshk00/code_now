async function fetchRequestsFromAPI() {
    try {
        const response = await fetch('/api/requests');
        const data = await response.json();
        console.log(data)
        return data;
    } catch (error) {
        console.error('Error fetching programs:', error);
        return [];
    }
}

async function populateRequests() {
    const data = await fetchRequestsFromAPI();
    const container = document.getElementById("main");
    console.log(data)
    
    let requestsHTML = ''; // Initialize an empty string to store the HTML
    
    data.forEach((requestData, index) => {
        const uniqueId = `request-${index}`;
        const request = `
        <div class="r-container" id="${uniqueId}">
            <div class="info"><span>Course:</span> ${requestData[0]}</div>
            <div class="info"><span>Student Name:</span> ${requestData[1]}</div>
            <div class="info"><span>Education Background:</span> ${requestData[5]}</div>
            <div class="info"><span>Employment Status:</span> ${requestData[6]}</div>
            <div class="info"><span>Purpose:</span> ${requestData[7]}</div>
            <div class="buttons">
            <button class="accept" id="accept-${uniqueId}">Accept</button>
            <button class="reject" id="reject-${uniqueId}">Reject</button>
            </div>
        </div>`;
        
        requestsHTML += request; // Append the HTML to the programsHTML string
    });
    
    container.innerHTML = requestsHTML; // Set the innerHTML once after the loop completes

    data.forEach((requestData, index) => {
        const uniqueId = `request-${index}`; // Define uniqueId here to make it accessible within the event listener
        const acceptButton = document.getElementById(`accept-${uniqueId}`);
        const rejectButton = document.getElementById(`reject-${uniqueId}`);

        acceptButton.addEventListener('click', () => {
            console.log(`Accept button clicked for email: ${requestData[2]} and course: ${requestData[0]}`);
            var email = `${requestData[2]}`
            var course = `${requestData[0]}`
            var name = `${requestData[1]}`

            sendEmail(email, course, name, 'accept');
            enrolled(course, name);
            removeContainer(uniqueId);
        });

        rejectButton.addEventListener('click', () => {
            console.log(`Reject button clicked for email: ${requestData[2]} and course: ${requestData[0]}`);
            var email = `${requestData[2]}`
            var course = `${requestData[0]}`
            var name = `${requestData[1]}`

            sendEmail(email, course, name, 'reject');
            removeContainer(uniqueId);
        });
    });
};


async function sendEmail(email, course, name, action) {
    try {
        const response = await fetch('/send-email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, course, name, action })
        });
        const data = await response.json();
        console.log(data); // Assuming the server sends back a response, you can handle it here
    } catch (error) {
        console.error('Error sending email:', error);
    }
}

async function enrolled(course, student) {
    try {
        const response = await fetch('/enrolled', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({course, student})
        });
        const data = await response.json();
        console.log(data);
        console.log("sucess")
    } catch (error) {
        console.error('Error sending email:', error);
    }
}    

function removeContainer(id) {
    const container = document.getElementById(id);
    if (container) {
        container.style.animation = 'fadeOut 1s forwards';
        setTimeout(() => {
            container.remove();
        }, 1000);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    populateRequests();
});
