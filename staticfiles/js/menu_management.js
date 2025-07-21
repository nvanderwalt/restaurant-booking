document.addEventListener('DOMContentLoaded', function() {
    const deleteBtns = document.querySelectorAll('.delete-menu-item');
    const menuItemNameSpan = document.getElementById('menuItemName');
    const deleteForm = document.getElementById('deleteMenuItemForm');
    
    deleteBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            const itemName = this.dataset.itemName;
            
            menuItemNameSpan.textContent = itemName;
            deleteForm.action = `/delete-menu-item/${itemId}/`;
            
            const deleteModal = new bootstrap.Modal(document.getElementById('deleteMenuItemModal'));
            deleteModal.show();
        });
    });
});