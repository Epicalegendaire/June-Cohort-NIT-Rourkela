// main.js (optional placeholder logic)
document.addEventListener('DOMContentLoaded', function() {
    // Add click event to patient list items
    const patientItems = document.querySelectorAll('.patient-list li');
    patientItems.forEach(item => {
        item.addEventListener('click', function() {
            // Remove active class from all items
            patientItems.forEach(i => i.classList.remove('active'));
            // Add active class to clicked item
            this.classList.add('active');
            
            // Here you would typically load patient data
            console.log('Patient selected:', this.textContent);
        });
    });

    // Add click event to + buttons
    const addButtons = document.querySelectorAll('.add-btn');
    addButtons.forEach(button => {
        button.addEventListener('click', function() {
            console.log('Add button clicked in section:', this.parentElement.querySelector('h3').textContent);
            // Here you would typically show a form to add content
        });
    });
});
