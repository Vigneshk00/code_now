// Function to fetch programs from the API
async function fetchMyProgramsFromAPI() {
    try {
        const response = await fetch('/api/myprograms');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching programs:', error);
        return [];
    }
}

// Function to populate programs based on fetched data
async function populateMyPrograms() {
    const data = await fetchMyProgramsFromAPI();
    const container = document.getElementById("explore-content");
    let myProgramsHTML = ''; // Initialize an empty string to store the HTML

    if (data.length === 0) {
        myProgramsHTML = '<p>No courses available.</p>'; // Display message if no courses are found
    } else {
        data.forEach((programData, index) => {

            let buttonHTML = '';
            if (programData[2] === 'pending') {
                buttonHTML = `<button class="pay-btn" data-course-name="${programData[1]}" data-price="${programData[3]}">Make Payment</button>`;
            } else {
                buttonHTML = `<button class="close-btn" data-course-name="${programData[1]}" data-price="${programData[3]}">Go to Course →</button>`;
            }
            const program = `
            <div class="single-explore-item2 vertical-layout">
                <div class="explore-program-img">
                    <img src="${programData[0]}" alt="explore image">
                </div>
                <div class="single-explore-txt bg-theme-1">
                    <h2>${programData[1]}</h2>
                </div> 
                <div class="explore-open-close-part">
                    ${buttonHTML}
                </div>
            </div>`;
        
            myProgramsHTML += program; // Append the HTML to the myProgramsHTML string
        });
    }
    
    container.innerHTML = myProgramsHTML; // Set the innerHTML once after the loop completes

    document.querySelectorAll('.pay-btn').forEach(button => {
        button.addEventListener('click', function() {
            // const url = this.getAttribute('/payment');
            
            window.location.href = '/payment';
        });
    });

    document.querySelectorAll('.close-btn').forEach(button => {
        button.addEventListener('click', function() {
            // const url = this.getAttribute('/course');
            window.location.href = '/course';
        });
    });
}

// Event listener for DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    populateMyPrograms(); // Fetch and populate programs when the DOM content is loaded
});
