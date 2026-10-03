document.addEventListener('DOMContentLoaded', () => {
    const salesData = JSON.parse(localStorage.getItem('salesData')) || [];
    if (salesData.length === 0) {
        document.querySelector('.performance-content').innerHTML = 
            '<h1>No sales data found.</h1><p>Please add sales from the main dashboard to see performance metrics.</p>';
        return;
    }
    const productPerformance = salesData.reduce((acc, sale) => {
        if (sale.status === 'Completed') {
            if (!acc[sale.product]) {
                acc[sale.product] = { unitsSold: 0, totalRevenue: 0 };
            }
            acc[sale.product].unitsSold += sale.quantity;
            acc[sale.product].totalRevenue += sale.amount;
        }
        return acc;
    }, {});
    const performanceArray = Object.entries(productPerformance).map(([productName, data]) => ({
        product: productName,
        unitsSold: data.unitsSold,
        totalRevenue: data.totalRevenue,
        avgPrice: data.unitsSold > 0 ? (data.totalRevenue / data.unitsSold) : 0,
    })).sort((a, b) => b.unitsSold - a.unitsSold);
    const barCtx = document.getElementById('performance-bar-chart').getContext('2d');
    new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: performanceArray.map(item => item.product),
            datasets: [{
                label: 'Total Units Sold',
                data: performanceArray.map(item => item.unitsSold),
                backgroundColor: '#007bff',
            }]
        },
        options: {
            scales: { y: { beginAtZero: true } },
            responsive: true,
            maintainAspectRatio: false,
        }
    });
    const tableBody = document.querySelector('#performance-table tbody');
    tableBody.innerHTML = ''; 
    performanceArray.forEach(item => {
        const row = tableBody.insertRow();
        row.insertCell(0).textContent = item.product;
        row.insertCell(1).textContent = item.unitsSold;
        row.insertCell(2).textContent = `$${item.totalRevenue.toFixed(2)}`;
        row.insertCell(3).textContent = `$${item.avgPrice.toFixed(2)}`;
    });
});

