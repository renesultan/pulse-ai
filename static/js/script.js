document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('orgChartForm');
    const companyNameInput = document.getElementById('companyName');
    const departmentNameInput = document.getElementById('departmentName');
    const orgStructureInput = document.getElementById('orgStructure');
    const reportingLineSelect = document.getElementById('reportingLine');
    const exampleButton = document.getElementById('btnExample');

    // Sample data for "Try an example" button
    const exampleData = {
        companyName: 'Hoolie',
        departmentName: 'Engineering',
        orgStructure: 'Richard Hendricks, CEO\n' +
                     'Bertram Gilfoyle, CTO, Richard Hendricks\n' +
                     'Dinesh Chugtai, Lead Engineer, Bertram Gilfoyle\n' +
                     'Jared Dunn, COO, Richard Hendricks\n' +
                     'Monica Hall, CFO, Richard Hendricks\n' +
                     'Nelson Bighetti, Programmer, Dinesh Chugtai',
        reportingLine: 'hierarchical'
    };

    // Load example data
    exampleButton.addEventListener('click', function(e) {
        e.preventDefault();
        companyNameInput.value = exampleData.companyName;
        departmentNameInput.value = exampleData.departmentName;
        orgStructureInput.value = exampleData.orgStructure;
        
        // Select the value in the dropdown
        Array.from(reportingLineSelect.options).forEach(option => {
            if (option.value === exampleData.reportingLine) {
                option.selected = true;
            }
        });
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
