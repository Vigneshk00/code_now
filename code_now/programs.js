// // Function to fetch questions and answers from the API
// async function fetchProgramsFromAPI() {
//     try {
//         const response = await fetch('/api/programs');
//         const data = await response.json();
//         console.log(data)
//         return data;
//     } catch (error) {
//         console.error('Error fetching programs:', error);
//         return [];
//     }
// }

// async function populatePrograms() {
//     const data = await fetchProgramsFromAPI();
//     const container = document.getElementById("explore-content");
//     console.log(data)
    
//     let programsHTML = ''; // Initialize an empty string to store the HTML
    
//     data.forEach((programData, index) => {
//         const program = `
//         <div class="single-explore-item vertical-layout">
//             <div class="course-content">
//                 <div class="single-explore-img">
//                     <img src="${programData[6]}" alt="explore image">
//                 </div>
//                 <div class="single-explore-txt bg-theme-1">
//                     <h2><a href="#">${programData[0]}</a></h2>
//                     <p class="explore-rating-price">
//                         <span class="explore-rating">${programData[1]}</span>
//                         <a href="#"> ${programData[2]} ratings</a>
//                         <span class="explore-price-box">
//                             ${programData[3]}
//                         </span>
//                         <a href="#">${programData[4]}</a>
//                     </p>
//                     <div class="explore-person">
//                         <p>
//                             ₹ ${programData[5]}/-
//                         </p>
//                     </div>
//                     <div class="explore-open-close-part">
//                         <button class="close-btn" data-program-id="${programData[0]}">apply now</button>
//                     </div>
//                 </div>
//             </div>
//         </div>`;
        
//         programsHTML += program; // Append the HTML to the programsHTML string
//     });
    
//     container.innerHTML = programsHTML; // Set the innerHTML once after the loop completes

//     const applyButtons = document.querySelectorAll('.close-btn');
//     applyButtons.forEach(button => {
//         button.addEventListener('click', redirectToRegistrationPage);
//     });
// }

// function redirectToRegistrationPage(event) {
//     const programId = event.target.getAttribute('data-program-id');
//     // Assuming the registration page URL includes the program ID as a query parameter
//     window.location.href = `/registration?programId=${programId}`;
// }

// document.addEventListener('DOMContentLoaded', function() {
//     populatePrograms();
// });


// Function to fetch programs from the API
async function fetchMyProgramsFromAPI() {
    try {
        const response = await fetch('http://127.0.0.1:8928/api/programs');
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
    console.log(data);
    const container = document.getElementById("explore-content");
    let programsHTML = ''; // Initialize an empty string to store the HTML

    data.forEach((programData, index) => {
        const program = `
        <div class="single-explore-item vertical-layout" data-subject="${programData[0]}" data-duration="${programData[4]}" data-start-date="${programData[3]}">
            <div class="course-content">
                <div class="single-explore-img">
                    <img src="${programData[6]}" alt="explore image">
                </div>
                <div class="single-explore-txt bg-theme-1">
                    <h2><a href="#">${programData[0]}</a></h2>
                    <p class="explore-rating-price">
                        <span class="explore-rating">${programData[1]}</span>
                        <a href="#"> ${programData[2]} ratings</a>
                        <span class="explore-price-box">
                            ${programData[3]}
                        </span>
                        <a href="#">${programData[4]}</a>
                    </p>
                    <div class="explore-person">
                        <p>
                            ₹ ${programData[5]}/-
                        </p>
                    </div>
                    <div class="explore-open-close-part">
                        <button class="close-btn" data-program-id="${programData[0]}">apply now</button>
                    </div>
                </div>
            </div>
        </div>`;
        
        programsHTML += program; // Append the HTML to the programsHTML string
    });
    
    container.innerHTML = programsHTML; // Set the innerHTML once after the loop completes

    const applyButtons = document.querySelectorAll('.close-btn');
    applyButtons.forEach(button => {
        button.addEventListener('click', redirectToRegistrationPage);
    });

    // Filter programs when the DOM content is loaded
    // filterPrograms();
}

// Function to filter programs based on selected criteria
function filterPrograms() {
    // const selectedSubjects = Array.from(document.querySelectorAll('input[name="subject"]:checked')).map(checkbox => checkbox.value);
    const selectedDurations = Array.from(document.querySelectorAll('input[name="duration"]:checked')).map(checkbox => parseInt(checkbox.value)); // Convert duration values to integers
    const selectedStartDate = document.getElementById('start-date').value;

    const programItems = document.querySelectorAll('.single-explore-item');

    // Loop through each program item and check if it matches the selected criteria
    programItems.forEach(function(item) {
        // const subject = item.getAttribute('data-subject').toLowerCase();
        const duration = parseInt(item.getAttribute('data-duration')); // Convert duration attribute value to integer
        const startDate = item.getAttribute('data-start-date').toLowerCase();

        // const matchesSubject = selectedSubjects.length === 0 || selectedSubjects.includes(subject);
        const matchesDuration = selectedDurations.length === 0 || selectedDurations.includes(duration);
        const matchesStartDate = selectedStartDate === 'all' || startDate.includes(selectedStartDate.toLowerCase());

        // Show or hide the program item based on the criteria
        if (matchesDuration && matchesStartDate) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
}

// Function to redirect to registration page
function redirectToRegistrationPage(event) {
    const programId = event.target.getAttribute('data-program-id');
    // Assuming the registration page URL includes the program ID as a query parameter
    window.location.href = `/registration?programId=${programId}`;
}

// Add event listener for DOMContentLoaded event

document.addEventListener('DOMContentLoaded', function() {
    populateMyPrograms(); // Fetch and populate programs when the DOM content is loaded

    // Add event listener for changes in filter elements
    const filterCheckboxes = document.querySelectorAll('.filter input[type="checkbox"], .filter select');
    filterCheckboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', filterPrograms);
    });
});
