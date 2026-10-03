const defaultSalesData = [
    { id: 1, date: '2025-07-05', product: 'iTab', amount: 450, status: 'Completed', quantity: 3 },
    { id: 2, date: '2025-07-08', product: 'Webcam', amount: 75, status: 'Completed', quantity: 5 },
    { id: 3, date: '2025-07-10', product: 'iPhone', amount: 999, status: 'Completed', quantity: 2 },
    { id: 4, date: '2025-07-12', product: 'Laptop Pro', amount: 1200, status: 'Completed', quantity: 1 },
    { id: 5, date: '2025-07-15', product: 'Television', amount: 1500, status: 'Completed', quantity: 1 },
    { id: 6, date: '2025-07-18', product: 'iTab', amount: 900, status: 'Completed', quantity: 2 },
    { id: 7, date: '2025-07-20', product: 'Webcam', amount: 150, status: 'Completed', quantity: 2 },
    { id: 8, date: '2025-07-22', product: 'iPhone', amount: 1998, status: 'Completed', quantity: 2 },
    { id: 9, date: '2025-07-25', product: 'Laptop Pro', amount: 2400, status: 'Completed', quantity: 2 },
    { id: 10, date: '2025-07-28', product: 'Television', amount: 3000, status: 'Completed', quantity: 2 },
];
let salesData = JSON.parse(localStorage.getItem('salesData'));
if (!salesData || salesData.length === 0) {
    salesData = defaultSalesData;
    localStorage.setItem('salesData', JSON.stringify(salesData));
}

let filteredData = [...salesData]; 
let salesLineChart, productBarChart; 

function calculateKPIs(data) {
    const completedSales = data.filter(s => s.status === 'Completed');
    const totalRevenue = completedSales.reduce((sum, s) => sum + s.amount, 0);
    const totalOrders = completedSales.length;
    const avgOrderValue = totalOrders > 0 ? (totalRevenue / totalOrders) : 0;
    const newCustomers = new Set(completedSales.map(s => s.product)).size;
    
    return {
        totalRevenue: totalRevenue.toFixed(2),
        totalOrders,
        avgOrderValue: avgOrderValue.toFixed(2),
        newCustomers
    };
}

function updateKPIs(kpis) {
    document.getElementById('total-revenue').textContent = `$${kpis.totalRevenue}`;
    document.getElementById('total-orders').textContent = kpis.totalOrders;
    document.getElementById('avg-order-value').textContent = `$${kpis.avgOrderValue}`;
    document.getElementById('new-customers').textContent = kpis.newCustomers;
}

function updateDataTable(data) {
    const tableBody = document.querySelector('#sales-data-table tbody');
    tableBody.innerHTML = ''; 
    data.forEach(sale => {
        const row = tableBody.insertRow();
        row.insertCell(0).textContent = sale.id;
        row.insertCell(1).textContent = sale.product;
        row.insertCell(2).textContent = new Date(sale.date).toLocaleDateString();
        row.insertCell(3).textContent = `$${sale.amount.toFixed(2)}`;
        row.insertCell(4).textContent = sale.status;
    });
}

function renderCharts(data) {
    const lineCtx = document.getElementById('sales-line-chart').getContext('d');
    const barCtx = document.getElementById('product-bar-chart').getContext('2d');
    
    if (salesLineChart) salesLineChart.destroy();
    if (productBarChart) productBarChart.destroy();

    const monthlySales = data.reduce((acc, sale) => {
        const month = new Date(sale.date).toLocaleString('default', { month: 'short', year: 'numeric' });
        acc[month] = (acc[month] || 0) + sale.amount;
        return acc;
    }, {});

    salesLineChart = new Chart(lineCtx, {
        type: 'line',
        data: {
            labels: Object.keys(monthlySales),
            datasets: [{
                label: 'Total Sales ($)',
                data: Object.values(monthlySales),
                borderColor: '#007bff',
                fill: true,
                tension: 0.4
            }]
        }
    });

    const productSales = data.reduce((acc, sale) => {
        acc[sale.product] = (acc[sale.product] || 0) + sale.quantity;
        return acc;
    }, {});
    const sortedProducts = Object.entries(productSales).sort(([, a], [, b]) => b - a).slice(0, 5);

    productBarChart = new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: sortedProducts.map(item => item[0]),
            datasets: [{
                label: 'Units Sold',
                data: sortedProducts.map(item => item[1]),
                backgroundColor: ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1'],
            }]
        }
    });
}

function refreshDashboard(data) {
    updateDataTable(data);
    renderCharts(data);
}

document.addEventListener('DOMContentLoaded', () => {
    refreshDashboard(filteredData);
    const initialKpis = calculateKPIs(filteredData);
    updateKPIs(initialKpis);


    document.getElementById('date-range').addEventListener('change', (event) => {
        const selectedRange = event.target.value;
        const now = new Date();
        let startDate;

        if (selectedRange === 'all-time') {
            filteredData = [...salesData];
        } else {
            if (selectedRange === 'last-7-days') {
                startDate = new Date(new Date().setDate(now.getDate() - 7));
            } else if (selectedRange === 'last-30-days') {
                startDate = new Date(new Date().setDate(now.getDate() - 30));
            }
            filteredData = salesData.filter(sale => new Date(sale.date) >= startDate);
        }
        
        refreshDashboard(filteredData);
    });
});

