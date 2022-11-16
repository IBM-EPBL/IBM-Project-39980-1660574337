$(document).on('submit', '#Organisation-Signup-Form', function (e) {
    e.preventDefault();
    $('#Organisation-Signup-Form').validate({
        focusCleanup: true,
        focusInvalid: false,
        ignore: '.ignore',
        debug: true,
        // Rules
        rules: {
            org_contact: {
                required: true,
                digits: true,
            },
            org_pincode: {
                required: true,
                digits: true,
            },
        },
        errorPlacement: function (error, element){
            const ele = $(element).attr("id");
            error.insertAfter('#'+ele+'Validate');
        },
    });

    $('#Organisation-Signup-Form').validate();

    if ($('#Organisation-Signup-Form').valid()) {
        const formdata = new FormData($('#Organisation-Signup-Form')[0]);
        const form = Object.fromEntries(formdata.entries());

        $.ajax({
            type: 'POST',
            url: '/register-as-org',
            data: JSON.stringify(form),
            contentType: 'application/json',
            success: function (response){
                if (response['status'] === 'New-user') {
                    swal.fire({
                        title: 'Thank you',
                        text: 'We\'ll contact you after verifying your response.',
                        icon: 'success',
                        confirmButtonText: 'OK',
                        confirmButtonColor: '#0d6efd',
                    }).then((result) => {
                        if (result) {
                            $('#Organisation-Signup-Form')[0].reset();
                            window.location.href = '/';
                        }
                    });
                }
                else if (response['status'] === 'PENDING') {
                    swal.fire({
                        title: 'You\'ve already submitted a response.',
                        text: 'Verification is pending.',
                        icon: 'info',
                        confirmButtonColor: '#0d6efd',
                    }).then((result) => {
                        if (result) {
                            window.location.href = '/';
                        }
                    });
                }
                else {
                    swal.fire({
                        title: 'You had been registered already.',
                        text: 'Login to continue.',
                        icon: 'warning',
                    });
                }
            },
            error: function () {
                alert('ERROR');
            }
        });
    }
})