document.addEventListener('DOMContentLoaded', function() {
    const checkAvailabilityBtn = document.getElementById('check-availability');
    const submitBookingBtn = document.getElementById('submit-booking');
    const availableTablesDiv = document.getElementById('available-tables');
    const tableOptionsDiv = document.getElementById('table-options');
    const bookingForm = document.getElementById('booking-form');
    
    checkAvailabilityBtn.addEventListener('click', function() {
        
        const formData = new FormData(bookingForm);
        const date = formData.get('booking_date');
        const time = formData.get('booking_time');
        const partySize = formData.get('party_size');
        
        
        if (!date || !time || !partySize) {
            alert('Please fill out all required fields');
            return;
        }
        
        
        fetch('/check-availability/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'booking_date': date,
                'booking_time': time,
                'party_size': partySize,
            })
        })
        .then(response => response.json())
        .then(data => {
            
            tableOptionsDiv.innerHTML = '';
            
            if (data.available_tables && data.available_tables.length > 0) {
                
                data.available_tables.forEach(table => {
                    const tableCol = document.createElement('div');
                    tableCol.className = 'col-md-4 mb-3';
                    tableCol.innerHTML = `
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Table ${table.table_number}</h5>
                                <p class="card-text">Capacity: ${table.capacity}</p>
                                <p class="card-text">Location: ${table.location}</p>
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" name="table_id" value="${table.id}" id="table_${table.id}">
                                    <label class="form-check-label" for="table_${table.id}">
                                        Select this table
                                    </label>
                                </div>
                            </div>
                        </div>
                    `;
                    tableOptionsDiv.appendChild(tableCol);
                });
                
                // Show available tables and submit button
                availableTablesDiv.style.display = 'block';
                submitBookingBtn.style.display = 'inline-block';
            } else {
                // No tables available
                tableOptionsDiv.innerHTML = '<div class="col-12"><div class="alert alert-warning">No tables available for the selected date, time, and party size.</div></div>';
                availableTablesDiv.style.display = 'block';
                submitBookingBtn.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while checking availability');
        });
    });
});