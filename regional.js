const salesData = [
    { orderId: 'ORD001', product: 'Peace Headbuds', date:   '2025-08-24', amount: 42.00, status: 'Completed', state: 'Mumbai' },
    { orderId: 'ORD003', product: 'iTab', date:    '2025-08-25', amount: 50, status: 'Completed', state: 'Mumbai' },
    { orderId: 'ORD002', product: 'iPhone', date: '2025-08-27', amount: 75, status: 'Shipped', state: 'Delhi' },
    { orderId: 'ORD004', product: 'iTab', date:  '2025-08-22', amount: 30, status: 'Pending', state: 'Bengaluru' },
    { orderId: 'ORD005', product: 'MaxView Television', date:   '2025-08-23', amount: 120, status: 'Completed', state: 'Delhi' },
    { orderId: 'ORD006', product: 'Realme x7', date:    '2025-08-29', amount: 50, status: 'Pending', state: 'Mumbai' },
    { orderId: 'ORD007', product: 'iTab', date:    '2025-08-27', amount: 50, status: 'Completed', state: 'Bengaluru' },
    { orderId: 'ORD008', product: 'MaxView Television', date:   '2025-08-23', amount: 120, status: 'Shipped', state: 'Mumbai' },
    { orderId: 'ORD009', product: 'Peace Headbuds', date: '2025-08-26', amount: 75, status: 'Completed', state: 'Bengaluru' },
    { orderId: 'ORD010', product: 'iTab', date:  '2025-08-20', amount: 30, status: 'Completed', state: 'Delhi' }
];
function analyzeRegionalSales(data) {
    const regionalData = {};

    data.forEach(sale => {
        const { state, product, amount } = sale;
        if (!regionalData[state]) {
            regionalData[state] = {
                totalRevenue: 0,
                orders: 0,
                products: {}
            };
        }
        regionalData[state].totalRevenue += amount;
        regionalData[state].orders += 1;
        
        if (!regionalData[state].products[product]) {
            regionalData[state].products[product] = 0;
        }
        regionalData[state].products[product] += amount;
    });

    return regionalData;
}
function getTopProduct(products) {
    let topProduct = null;
    let maxSales = 0;
    for (const product in products) {
        if (products[product] > maxSales) {
            maxSales = products[product];
            topProduct = product;
        }
    }
    return topProduct;
}
function renderRegionalTable(regionalData) {
    const tableBody = document.querySelector('#regional-sales-table tbody');
    tableBody.innerHTML = '';
    
    for (const state in regionalData) {
        const row = document.createElement('tr');
        const topProduct = getTopProduct(regionalData[state].products);

        row.innerHTML = `
            <td>${state}</td>
            <td>$${regionalData[state].totalRevenue.toFixed(2)}</td>
            <td>${topProduct || 'N/A'}</td>
            <td>${regionalData[state].orders}</td>
        `;
        tableBody.appendChild(row);
    }
}
function renderRegionalChart(regionalData) {
    const states = Object.keys(regionalData);
    if (states.length === 0) return;
        const stateToDisplay = states[0]; 
    const productsData = regionalData[stateToDisplay].products;

    const chartLabels = Object.keys(productsData);
    const chartData = Object.values(productsData);

    const ctx = document.getElementById('regional-product-chart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chartLabels,
            datasets: [{
                label: `Sales in ${stateToDisplay} ($)`,
                data: chartData,
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
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
    const regionalData = analyzeRegionalSales(salesData);
    renderRegionalTable(regionalData);
    renderRegionalChart(regionalData);
});