document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('orgChartForm');
    const companyNameInput = document.getElementById('companyName');
    const departmentNameInput = document.getElementById('departmentName');
    const orgStructureInput = document.getElementById('orgStructure');
    const reportingLineSelect = document.getElementById('reportingLine');
    const exampleButton = document.getElementById('btnExample');

    // Load enterprise example data from the database
    exampleButton.addEventListener('click', async function(e) {
        e.preventDefault();
        
        // Show loading indicator
        exampleButton.disabled = true;
        exampleButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-loader"><line x1="12" y1="2" x2="12" y2="6"></line><line x1="12" y1="18" x2="12" y2="22"></line><line x1="4.93" y1="4.93" x2="7.76" y2="7.76"></line><line x1="16.24" y1="16.24" x2="19.07" y2="19.07"></line><line x1="2" y1="12" x2="6" y2="12"></line><line x1="18" y1="12" x2="22" y2="12"></line><line x1="4.93" y1="19.07" x2="7.76" y2="16.24"></line><line x1="16.24" y1="7.76" x2="19.07" y2="4.93"></line></svg> Loading...';
        
        try {
            // Fetch enterprise example data from our API
            const response = await fetch('/api/get-enterprise-example');
            
            if (!response.ok) {
                throw new Error('Failed to fetch enterprise example data');
            }
            
            const exampleData = await response.json();
            
            // Populate the form with the fetched data
            companyNameInput.value = exampleData.companyName;
            departmentNameInput.value = exampleData.departmentName;
            orgStructureInput.value = exampleData.orgStructure;
            
            // Select the value in the dropdown
            Array.from(reportingLineSelect.options).forEach(option => {
                if (option.value === exampleData.reportingLine) {
                    option.selected = true;
                }
            });
            
            // Highlight the organization structure with a brief animation
            orgStructureInput.style.transition = 'background-color 0.5s';
            orgStructureInput.style.backgroundColor = '#f0f8ff';
            setTimeout(() => {
                orgStructureInput.style.backgroundColor = '';
            }, 1000);
        } catch (error) {
            console.error('Error fetching enterprise example data:', error);
            alert('Failed to load enterprise example data. Please try again.');
        } finally {
            // Restore the button
            exampleButton.disabled = false;
            exampleButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-play"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg> Try an example';
        }
    });

    // Form validation and submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        let isValid = true;
        
        // Basic validation
        if (!companyNameInput.value.trim()) {
            showError(companyNameInput, 'Company name is required');
            isValid = false;
        } else {
            hideError(companyNameInput);
        }
        
        if (!orgStructureInput.value.trim()) {
            showError(orgStructureInput, 'Organization structure is required');
            isValid = false;
        } else {
            hideError(orgStructureInput);
        }
        
        if (isValid) {
            // Build the URL with query parameters
            const params = new URLSearchParams({
                company_name: companyNameInput.value,
                department_name: departmentNameInput.value || '',
                org_structure: orgStructureInput.value,
                reporting_line: reportingLineSelect.value || ''
            });
            
            // Navigate to the org chart page
            window.location.href = `/org-chart?${params.toString()}`;
        }
    });

    // Helper functions for form validation
    function showError(input, message) {
        // Remove any existing error
        hideError(input);
        
        // Create and add error message
        const errorSpan = document.createElement('span');
        errorSpan.className = 'error-message';
        errorSpan.style.color = 'red';
        errorSpan.style.fontSize = '0.8rem';
        errorSpan.style.display = 'block';
        errorSpan.style.marginTop = '5px';
        errorSpan.textContent = message;
        
        // Find the appropriate parent for appending the error message
        const parent = input.parentNode.classList.contains('input-group') ? 
            input.parentNode.parentNode : input.parentNode;
            
        parent.appendChild(errorSpan);
        input.style.borderColor = 'red';
    }

    function hideError(input) {
        // Find the appropriate parent that might contain the error message
        const parent = input.parentNode.classList.contains('input-group') ? 
            input.parentNode.parentNode : input.parentNode;
            
        const errorSpan = parent.querySelector('.error-message');
        if (errorSpan) {
            parent.removeChild(errorSpan);
        }
        input.style.borderColor = '';
    }
});
