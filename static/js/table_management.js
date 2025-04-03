document.addEventListener('DOMContentLoaded', function() {

    const deleteBtns = document.querySelectorAll('.delete-table');
    const tableNumberSpan = document.getElementById('tableNumber');
    const deleteForm = document.getElementById('deleteTableForm');
    
    deleteBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tableId = this.dataset.tableId;
            const tableNumber = this.dataset.tableNumber;
            
            tableNumberSpan.textContent = tableNumber;
            deleteForm.action = `/delete-table/${tableId}/`;
            
            const deleteModal = new bootstrap.Modal(document.getElementById('deleteTableModal'));
            deleteModal.show();
        });
    });
});