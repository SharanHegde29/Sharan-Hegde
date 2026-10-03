
document.getElementById('add-sale-form').addEventListener('submit', function(event) {
    event.preventDefault(); 
    try {
        let salesData = JSON.parse(localStorage.getItem('salesData')) || [];
        const newSale = {
            id: Date.now(), 
            date: new Date().toISOString().split('T')[0], 
            product: document.getElementById('product-name').value,
            amount: parseFloat(document.getElementById('sale-amount').value),
            status: 'Completed',
            quantity: parseInt(document.getElementById('sale-quantity').value)
        };
        salesData.push(newSale);
        localStorage.setItem('salesData', JSON.stringify(salesData));
        window.location.href = 'index.html';

    } catch (error) {
        console.error("Failed to add sale:", error);
        alert("An error occurred while trying to save the sale. Please check the console for details.");
    }
});