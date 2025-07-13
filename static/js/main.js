// Yemen Fashion Store - Main JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Logo click counter for admin access
    let logoClickCount = 0;
    let logoClickTimer = null;
    const logoLink = document.getElementById('logo-link');
    
    if (logoLink) {
        logoLink.addEventListener('click', function(e) {
            logoClickCount++;
            
            // Reset counter after 3 seconds of inactivity
            if (logoClickTimer) {
                clearTimeout(logoClickTimer);
            }
            
            logoClickTimer = setTimeout(function() {
                logoClickCount = 0;
            }, 3000);
            
            // Show admin login after 3 clicks
            if (logoClickCount === 3) {
                e.preventDefault();
                logoClickCount = 0;
                window.location.href = '/admin/login';
            }
        });
    }
    
    // Form validation for order form
    const orderForm = document.querySelector('.order-form');
    if (orderForm) {
        orderForm.addEventListener('submit', function(e) {
            // Validate phone number (Yemen format)
            const phoneInput = orderForm.querySelector('input[name="phone"]');
            if (phoneInput) {
                const phoneValue = phoneInput.value.trim();
                const yemenPhoneRegex = /^(77|73|70|71|78)\d{7}$/;
                
                if (!yemenPhoneRegex.test(phoneValue)) {
                    e.preventDefault();
                    showAlert('يرجى إدخال رقم هاتف صحيح (مثال: 771234567)', 'danger');
                    phoneInput.focus();
                    return;
                }
            }
            
            // Show loading state
            const submitBtn = orderForm.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> جاري الإرسال...';
                submitBtn.disabled = true;
                
                // Re-enable after 5 seconds in case of issues
                setTimeout(function() {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 5000);
            }
        });
    }
    
    // Star rating interactive behavior
    const starRatingInputs = document.querySelectorAll('.star-rating input[type="radio"]');
    starRatingInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            const rating = parseInt(this.value);
            const starContainer = this.closest('.star-rating');
            const labels = starContainer.querySelectorAll('label');
            
            labels.forEach(function(label, index) {
                if (index < rating) {
                    label.classList.add('active');
                } else {
                    label.classList.remove('active');
                }
            });
        });
    });
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            if (alert.parentNode) {
                alert.style.opacity = '0';
                setTimeout(function() {
                    alert.remove();
                }, 300);
            }
        }, 5000);
    });
    
    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
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
    
    // Product image zoom on hover
    const productImages = document.querySelectorAll('.product-image img');
    productImages.forEach(function(img) {
        img.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
            this.style.transition = 'transform 0.3s ease';
        });
        
        img.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
    
    // Category filter functionality
    const categoryFilter = document.querySelector('.category-filter');
    if (categoryFilter) {
        categoryFilter.addEventListener('change', function() {
            const selectedCategory = this.value;
            const productCards = document.querySelectorAll('.product-card');
            
            productCards.forEach(function(card) {
                const categoryId = card.getAttribute('data-category-id');
                if (selectedCategory === '' || categoryId === selectedCategory) {
                    card.style.display = 'block';
                    card.style.animation = 'fadeIn 0.5s ease-out';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
    
    // Form field auto-formatting
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            // Remove non-numeric characters
            let value = this.value.replace(/\D/g, '');
            
            // Format Yemen phone numbers
            if (value.length > 0) {
                if (value.length <= 3) {
                    value = value;
                } else if (value.length <= 6) {
                    value = value.substring(0, 3) + ' ' + value.substring(3);
                } else if (value.length <= 9) {
                    value = value.substring(0, 3) + ' ' + value.substring(3, 6) + ' ' + value.substring(6);
                } else {
                    value = value.substring(0, 3) + ' ' + value.substring(3, 6) + ' ' + value.substring(6, 9);
                }
            }
            
            this.value = value;
        });
    });
    
    // Price formatting
    const priceElements = document.querySelectorAll('.product-price, .product-price-large');
    priceElements.forEach(function(element) {
        const price = parseFloat(element.textContent.replace(/[^\d.]/g, ''));
        if (!isNaN(price)) {
            element.textContent = new Intl.NumberFormat('ar-YE', {
                style: 'currency',
                currency: 'YER',
                minimumFractionDigits: 0
            }).format(price);
        }
    });
    
    // Lazy loading for images
    const images = document.querySelectorAll('img[data-src]');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(function(img) {
            imageObserver.observe(img);
        });
    }
    
    // Back to top button
    const backToTopBtn = document.createElement('button');
    backToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTopBtn.className = 'btn btn-glass back-to-top';
    backToTopBtn.style.cssText = `
        position: fixed;
        bottom: 20px;
        left: 20px;
        z-index: 1000;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: none;
        opacity: 0;
        transition: all 0.3s ease;
    `;
    
    document.body.appendChild(backToTopBtn);
    
    // Show/hide back to top button
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.style.display = 'block';
            setTimeout(function() {
                backToTopBtn.style.opacity = '1';
            }, 10);
        } else {
            backToTopBtn.style.opacity = '0';
            setTimeout(function() {
                backToTopBtn.style.display = 'none';
            }, 300);
        }
    });
    
    // Back to top functionality
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
});

// Utility functions
function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container');
    if (!alertContainer) return;
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} glass-alert alert-dismissible fade show`;
    alert.setAttribute('role', 'alert');
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    alertContainer.insertBefore(alert, alertContainer.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(function() {
        if (alert.parentNode) {
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 300);
        }
    }, 5000);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('ar-YE', {
        style: 'currency',
        currency: 'YER',
        minimumFractionDigits: 0
    }).format(amount);
}

function validateYemenPhone(phone) {
    const cleanPhone = phone.replace(/\D/g, '');
    const yemenPhoneRegex = /^(77|73|70|71|78)\d{7}$/;
    return yemenPhoneRegex.test(cleanPhone);
}

// Admin panel specific functions
if (window.location.pathname.startsWith('/admin')) {
    document.addEventListener('DOMContentLoaded', function() {
        // Auto-refresh statistics every 30 seconds
        const statsCards = document.querySelectorAll('.stats-card');
        if (statsCards.length > 0) {
            setInterval(function() {
                // This would typically make an AJAX call to refresh stats
                // For now, we'll just add a subtle animation to indicate activity
                statsCards.forEach(function(card) {
                    card.style.transform = 'scale(1.02)';
                    setTimeout(function() {
                        card.style.transform = 'scale(1)';
                    }, 200);
                });
            }, 30000);
        }
        
        // Confirm delete actions
        const deleteButtons = document.querySelectorAll('a[href*="/delete/"]');
        deleteButtons.forEach(function(button) {
            button.addEventListener('click', function(e) {
                if (!confirm('هل أنت متأكد من هذا الإجراء؟ لا يمكن التراجع عنه.')) {
                    e.preventDefault();
                }
            });
        });
        
        // Auto-save form data
        const forms = document.querySelectorAll('form');
        forms.forEach(function(form) {
            const inputs = form.querySelectorAll('input, textarea, select');
            inputs.forEach(function(input) {
                input.addEventListener('input', function() {
                    const formData = new FormData(form);
                    const data = {};
                    for (let [key, value] of formData.entries()) {
                        data[key] = value;
                    }
                    localStorage.setItem('form_' + form.id, JSON.stringify(data));
                });
            });
        });
        
        // Restore form data on page load
        forms.forEach(function(form) {
            const savedData = localStorage.getItem('form_' + form.id);
            if (savedData) {
                const data = JSON.parse(savedData);
                Object.keys(data).forEach(function(key) {
                    const input = form.querySelector(`[name="${key}"]`);
                    if (input) {
                        input.value = data[key];
                    }
                });
            }
        });
    });
}
