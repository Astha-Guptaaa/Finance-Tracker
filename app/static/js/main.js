/**
 * Main JavaScript for Personal Finance Tracker
 * Author: Senior Software Engineering Mentor
 */

document.addEventListener('DOMContentLoaded', function() {
    // 1. Initialize Bootstrap Tooltips if any
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // 2. Form Validation Feedback
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // 3. Delete Confirmation
    const deleteButtons = document.querySelectorAll('.delete-confirm');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // 4. Auto-hide Alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-important)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // 5. Dynamic Category Suggestions (Simple Example)
    const typeSelect = document.getElementById('transaction_type');
    const categorySelect = document.getElementById('category');
    
    if (typeSelect && categorySelect) {
        const categories = {
            'Income': ['Salary', 'Freelance', 'Investment', 'Gift', 'Other'],
            'Expense': ['Food', 'Rent', 'Utilities', 'Transport', 'Shopping', 'Health', 'Entertainment', 'Other'],
            'Received': ['Loan Repayment', 'Debt', 'Gift', 'Other'],
            'Sent': ['Loan', 'Debt Payment', 'Transfer', 'Other']
        };

        typeSelect.addEventListener('change', function() {
            const selectedType = this.value;
            const options = categories[selectedType] || [];
            
            // Clear current options
            categorySelect.innerHTML = '<option value="" selected disabled>Choose Category...</option>';
            
            // Add new options
            options.forEach(cat => {
                const opt = document.createElement('option');
                opt.value = cat;
                opt.textContent = cat;
                categorySelect.appendChild(opt);
            });
        });
    }
});

/**
 * Helper to initialize Charts (to be called from template specific blocks)
 */
function initAnalyticsCharts(trendLabels, incomeData, expenseData, catLabels, catValues) {
    // Trend Chart (Line)
    const trendCtx = document.getElementById('trendChart');
    if (trendCtx) {
        new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: trendLabels,
                datasets: [{
                    label: 'Income',
                    data: incomeData,
                    borderColor: '#1cc88a',
                    backgroundColor: 'rgba(28, 200, 138, 0.05)',
                    fill: true,
                    tension: 0.3
                }, {
                    label: 'Expense',
                    data: expenseData,
                    borderColor: '#e74a3b',
                    backgroundColor: 'rgba(231, 74, 59, 0.05)',
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'top' }
                },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }

    // Category Chart (Doughnut)
    const catCtx = document.getElementById('categoryChart');
    if (catCtx) {
        new Chart(catCtx, {
            type: 'doughnut',
            data: {
                labels: catLabels,
                datasets: [{
                    data: catValues,
                    backgroundColor: [
                        '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b', 
                        '#858796', '#5a5c69', '#2e59d9', '#17a673', '#2c9faf'
                    ],
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }
}
