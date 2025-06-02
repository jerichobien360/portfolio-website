// Wait for the page to load
$(document).ready(function() {
    
    // Test
    console.log("jQuery is working!");
    console.log("JavaScript file loaded successfully!");

    // Smooth scrolling for navigation links
    $('nav a[href^="#"]').on('click', function(e) {
        e.preventDefault();
        
        var target = this.hash;
        var targetElement = $(target);
        
        if (targetElement.length) {
            $('html, body').animate({
                scrollTop: targetElement.offset().top - 100
            }, 800);
        }
    });
    
    console.log("jQuery is working!");
});


// Contact form handling
$('#contactForm').on('submit', function(e) {
    e.preventDefault();
    
    var formData = $(this).serialize();
    
    $.ajax({
        url: '/contact',
        method: 'POST',
        data: formData,
        success: function(response) {
            if (response.success) {
                showMessage(response.message, 'success');
                $('#contactForm')[0].reset();
            } else {
                showMessage(response.message, 'error');
            }
        },
        error: function() {
            showMessage('Sorry, there was an error sending your message.', 'error');
        }
    });
});

// Helper functions
function isValidEmail(email) {
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showMessage(message, type) {
    var messageDiv = $('#formMessage');
    messageDiv.removeClass('success error');
    messageDiv.addClass(type);
    messageDiv.text(message);
    messageDiv.fadeIn();
    
    setTimeout(function() {
        messageDiv.fadeOut();
    }, 5000);
}
