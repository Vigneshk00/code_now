// Global variable to store all programs data
let allProgramsData = [];

// Function to fetch questions and answers from the API
async function fetchProgramsFromAPI() {
    try {
        const response = await fetch('/api/programs');
        console.log(response)
        const data = await response.json();
        console.log(data)
        return data;
    } catch (error) {
        console.error('Error fetching programs:', error);
        return [];
    }
}

async function populatePrograms() {
    const data = await fetchProgramsFromAPI();
    allProgramsData = data; // Store all programs data globally
    applyFilters(); // Apply filters initially
}

// Function to apply filters and populate programs
function applyFilters() {
    const selectedSubjects = Array.from(document.querySelectorAll('input[name="subject"]:checked')).map(checkbox => checkbox.value);
    const selectedDurations = Array.from(document.querySelectorAll('input[name="duration"]:checked')).map(checkbox => parseInt(checkbox.value));
    const selectedStartDate = document.getElementById('start-date').value;

    // Filter programs based on selected options
    const filteredPrograms = allProgramsData.filter(program => {
        return (
            (selectedSubjects.length === 0 || selectedSubjects.includes(program.subject)) &&
            (selectedDurations.length === 0 || selectedDurations.includes(program.duration)) &&
            (selectedStartDate === 'All' || (program.startDate && program.startDate.includes(selectedStartDate)))
        );
    });

    displayPrograms(filteredPrograms); // Pass the filtered programs to a separate function for displaying
}

// Function to display filtered programs
function displayPrograms(programs) {
    const container = document.getElementById("explore-content");
    let programsHTML = ''; // Initialize an empty string to store the HTML
    
    programs.forEach(programData => {
        const program = `
        <div class="single-explore-item vertical-layout">
            <div class="course-content">
                <div class="single-explore-img">
                    <img src="${programData.image}" alt="explore image">
                </div>
                <div class="single-explore-txt bg-theme-1">
                    <h2><a href="#">${programData.title}</a></h2>
                    <p class="explore-rating-price">
                        <span class="explore-rating">${programData.rating}</span>
                        <a href="#"> ${programData.ratingCount} ratings</a>
                        <span class="explore-price-box">
                            ${programData.price}
                        </span>
                        <a href="#">${programData.duration}</a>
                    </p>
                    <div class="explore-person">
                        <p>
                            ₹ ${programData.price}/-
                        </p>
                    </div>
                    <div class="explore-open-close-part">
                        <button class="close-btn">apply now</button>
                    </div>
                </div>
            </div>
        </div>`;
        
        programsHTML += program; // Append the HTML to the programsHTML string
    });
    
    container.innerHTML = programsHTML; // Set the innerHTML once after the loop completes
}

document.addEventListener('DOMContentLoaded', function() {
    populatePrograms();
    
    // Add event listeners to filter elements
    const filterInputs = document.querySelectorAll('input[name="subject"], input[name="duration"], #start-date');
    filterInputs.forEach(input => {
        input.addEventListener('change', applyFilters);
    });
});
