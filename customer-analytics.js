
const customers = [
    { id: 'CUST001', name: 'Sharan', email: 'sharan.may29@gmail.com', totalSpent: 1500, lastPurchase: '2025-08-20', joinDate: '2024-07-15' },
    { id: 'CUST002', name: 'Prem', email: 'prem45@gmail.com', totalSpent: 250, lastPurchase: '2025-08-25', joinDate: '2024-08-01' },
    { id: 'CUST003', name: 'Shubham', email:'shubham78@gmail.com', totalSpent: 75, lastPurchase: '2025-07-10', joinDate: '2024-09-01' },
    { id: 'CUST004', name: 'Ishaan', email: 'ishaan05@gmail.com', totalSpent: 500, lastPurchase: '2025-08-15', joinDate: '2024-08-10' },
    { id: 'CUST005', name: 'Amit', email: 'amit24@gmail.com', totalSpent: 900, lastPurchase: '2025-08-28', joinDate: '2024-08-28' },
];

function analyzeCustomerData(data) {
    const today = new Date();
    const thirtyDaysAgo = new Date(today.setDate(today.getDate() - 30));
    
    const totalCustomers = data.length;
    const newCustomers = data.filter(c => new Date(c.joinDate) >= thirtyDaysAgo).length;
    
    const sixtyDaysAgo = new Date(today.setDate(today.getDate() - 30));
    const churnedCustomers = data.filter(c => new Date(c.lastPurchase) < sixtyDaysAgo).length;
    const churnRate = (churnedCustomers / totalCustomers) * 100;

    return { totalCustomers, newCustomers, churnRate };
}

function renderKPIs(kpis) {
    document.getElementById('total-customers-kpi').innerText = kpis.totalCustomers;
    document.getElementById('new-customers-kpi').innerText = kpis.newCustomers;
    document.getElementById('churn-rate-kpi').innerText = kpis.churnRate.toFixed(2) + '%';
}

function renderCustomerTable(data) {
    const tableBody = document.querySelector('#customer-data-table tbody');
    tableBody.innerHTML = '';
    data.forEach(customer => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${customer.id}</td>
            <td>${customer.name}</td>
            <td>${customer.email}</td>
            <td>$${customer.totalSpent.toFixed(2)}</td>
            <td>${customer.lastPurchase}</td>
        `;
        tableBody.appendChild(row);
    });
}

function renderCohortChart(data) {
    const months = ['Jul', 'Aug'];
    const cohortData = [
        { month: 'Jul', newCustomers: 1, retained: [1, 1] },
        { month: 'Aug', newCustomers: 3, retained: [3] }
    ];

    const ctx = document.getElementById('customer-cohort-chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Week 0', 'Week 1'],
            datasets: [
                {
                    label: 'July Growth',
                    data: [1, 1], 
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                },
                {
                    label: 'August Growth',
                    data: [3, 2], 
                    borderColor: 'rgb(255, 99, 132)',
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const analytics = analyzeCustomerData(customers);
    renderKPIs(analytics);
    renderCustomerTable(customers);
    renderCohortChart(customers);
});