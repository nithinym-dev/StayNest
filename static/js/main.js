// Main JavaScript functions for HostelBook

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            if (alert.classList.contains('alert-success') || alert.classList.contains('alert-info')) {
                alert.style.opacity = '0';
                setTimeout(function() {
                    alert.remove();
                }, 300);
            }
        });
    }, 5000);

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Form validation enhancements
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<span class="spinner"></span> Processing...';
                submitBtn.disabled = true;
            }
        });
    });

    // Image preview for file uploads
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    // Create or update preview image
                    let preview = document.getElementById('image-preview');
                    if (!preview) {
                        preview = document.createElement('img');
                        preview.id = 'image-preview';
                        preview.style.maxWidth = '200px';
                        preview.style.maxHeight = '200px';
                        preview.style.marginTop = '10px';
                        preview.className = 'img-thumbnail';
                        input.parentNode.appendChild(preview);
                    }
                    preview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    });
});

// Search functionality
function searchProperties() {
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.submit();
    }
}

// Location detection
function getUserLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                
                // You can use this to auto-fill location fields or search nearby properties
                console.log('User location:', lat, lng);
            },
            function(error) {
                console.log('Location access denied');
            }
        );
    }
}

// Price calculation for booking
function calculateBookingPrice(dailyRate, monthlyRate, securityDeposit) {
    const bookingType = document.getElementById('id_booking_type');
    const checkIn = document.getElementById('id_check_in_date');
    const checkOut = document.getElementById('id_check_out_date');
    const totalElement = document.getElementById('total-amount');
    
    function updateTotal() {
        if (checkIn.value && checkOut.value) {
            const startDate = new Date(checkIn.value);
            const endDate = new Date(checkOut.value);
            const timeDiff = endDate.getTime() - startDate.getTime();
            const daysDiff = Math.ceil(timeDiff / (1000 * 3600 * 24));
            
            if (daysDiff > 0) {
                let total = 0;
                if (bookingType.value === 'daily') {
                    total = daysDiff * dailyRate;
                } else if (bookingType.value === 'monthly') {
                    const months = daysDiff / 30;
                    total = months * monthlyRate;
                }
                total += securityDeposit;
                
                if (totalElement) {
                    totalElement.textContent = '₹' + total.toFixed(2);
                }
            }
        }
    }
    
    if (bookingType && checkIn && checkOut) {
        bookingType.addEventListener('change', updateTotal);
        checkIn.addEventListener('change', updateTotal);
        checkOut.addEventListener('change', updateTotal);
    }
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

function showLoadingSpinner(element) {
    element.innerHTML = '<span class="spinner"></span> Loading...';
    element.disabled = true;
}

function hideLoadingSpinner(element, originalText) {
    element.innerHTML = originalText;
    element.disabled = false;
}
