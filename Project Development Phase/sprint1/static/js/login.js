/* Events during redirection behaviour of REQUEST $ DONATE button */
$(document).on('click', '#RequestLink2', function (){
    const loginAs = $(this).attr('data-type');
    $('#login-button').attr('data-userinfo', loginAs);
    $('#RequestLoginForDonorPage').css({display: 'block'});
});
$(document).on('hidden.bs.modal','#loginmodal' ,function (){
    $('#RequestLoginForDonorPage').css({display: 'none'});
    $('#loginform')[0].reset();
    if($('#UserNameValidate').attr('class')) {
        $('#UserNameValidate').text('');
        $('#UserNameValidate').removeClass('error');
    }
    if($('#LoginPasswordValidate').attr('class')) {
        $('#LoginPasswordValidate').text('');
        $('#LoginPasswordValidate').removeClass('error');
    }
});
$(document).on('click', '#DonateLink2', function (){
    const loginAs = $(this).attr('data-type');
    $('#login-button').attr('data-userinfo', loginAs);
    $('#RequestLoginForDonorPage').css({display: 'block'});
});
/* --- Login Form Validation --- */
$(document).on('submit', '#loginform', function (e){
    e.preventDefault();
    $('#loginform').validate({
        focusCleanup: true,
        focusInvalid: false,
        ignore: '.ignore',
        debug: true,
        rules: {
            username: {
                required: true,
            },
            loginpassword: {
                required: true,
            }
        },
        errorPlacement: function (error, element) {
            const ele = $(element).attr('id');
            error.insertAfter('#'+ele+'Validate');
        },
    });
    $('#loginform').validate();
    if($('#loginform').valid()) {
        $('#login-button').hide();
        $('#spinner-button').show();

        const form = new FormData($('#loginform')[0]);
        let loginform = Object.fromEntries(form.entries());
        loginform['title'] = document.title;

        if (document.title !== 'Administrator Login') {
            loginform['loginAs'] = $('#login-button').attr('data-userinfo');
        }
        $.ajax({
            type: 'POST',
            url: '/login',
            data: JSON.stringify(loginform),
            contentType: 'application/json',
            success: function (response) {
                if(response['status'] === 'logged-in') {
                    $('#login-button').show();
                    $('#spinner-button').hide();
                    // Removing error class
                    if($('#UserNameValidate').attr('class')) {
                        $('#UserNameValidate').text('');
                        $('#UserNameValidate').removeClass('error');
                    }
                    if($('#LoginPasswordValidate').attr('class')) {
                        $('#LoginPasswordValidate').text('');
                        $('#LoginPasswordValidate').removeClass('error');
                    }

                    if (response['user'] === 'ADMIN') {
                        window.location.href = '/Administrator';
                    }
                    else if (response['user'] === 'Org') {
                        window.location.href = '/';
                    }
                    else {
                        window.location.href = '/';
                    }
                }
                else if(response['status'] === 'Invalid-User') {
                    $('#login-button').show();
                    $('#spinner-button').hide();

                    $('#UserNameValidate').html('Invalid Username');
                    $('#UserNameValidate').attr('class', 'error');
                }
                else {
                    // Remove error class in UserName
                    if($('#UserNameValidate').attr('class')) {
                       $('#UserNameValidate').removeClass('error');
                       $('#UserNameValidate').html('');
                    }
                    $('#login-button').show();
                    $('#spinner-button').hide();
                    $('#LoginPasswordValidate').html('Invalid Password');
                    $('#LoginPasswordValidate').attr('class', 'error');
                }
            },
            error: function (response) {
                if (response['user'] === 'ADMIN') {
                    $('#login-button').show();
                    $('#spinner-button').hide();
                    alert('ERROR');
                    window.location.href = '/administrator-login';
                }
                else {
                    $('#login-button').show();
                    $('#spinner-button').hide();
                    alert('ERROR');
                    window.location.href = '/';
                }
            },
        });
    }
});

/* --- Show Password --- */
$(document).on('click', '.eye', function () {
    const ID = $(this).prev();
    if(ID.attr('type') === 'password') {
        ID.attr('type', 'text');
        $(this).attr('class', 'input-group-text eye fa-solid fa-eye-slash');
    }
    else {
        ID.attr('type', 'password');
        $(this).attr('class', 'input-group-text eye fa-solid fa-eye');
    }
});

/* --- Request Reset Form --- */
$(document).on('submit', '#reset-form', function (e){
    e.preventDefault();
    $('.alert-warning').css({display: 'none'});

    if($('#reset-form').valid()) {
        $('#reset-button').attr('disabled', true);
        const form_data = new FormData($('#reset-form')[0]);
        const form = Object.fromEntries(form_data.entries());
        $.ajax({
            type: 'POST',
            url: '/request-reset',
            data: JSON.stringify(form),
            contentType: 'application/json',
            success: function (response){
                if(response['status'] === 'Exist') {
                    $('.alert-success').css({display: 'block'});
                }
                else {
                    $('#reset-button').removeAttr('disabled');
                    $('.alert-warning').eq(0).css({display: 'block'});
                }
            },
            error: function () {
                alert('ERROR');
            },
        });
    }
});

/* Hide Warning Message On Focus */
$(document).on('focus', '#e-mail', function (){
    $('.alert-warning').css({display: 'none'});
});
/* --- Password Validation Container --- */
$(document).on('focus', '#Password', function () {
    $('.password-validation-container').css({visibility: 'visible'});
});
$(document).on('focusout', '#Password', function (){
    $('.password-validation-container').css({visibility: 'hidden'});
});
/* ---- Password On-type Validate --- */
$(document).ready(function(){
    $(document).on('paste', '#Password', function (e){
        e.preventDefault();
    });
    $(document).on('paste', '#Confirm', function (e){
        e.preventDefault();
    });
    $(document).on('keyup', '#Password', function (){
        const password = $('#Password').val();
        // Upper-case validate
        if(password.match('(?=.*[A-Z])')) {
            $('.upper').addClass('list-active');
        }
        else {
            $('.upper').removeClass('list-active');
        }
        // Lower-case validate
        if(password.match('(?=.*[a-z])')) {
            $('.lower').addClass('list-active');
        }
        else {
            $('.lower').removeClass('list-active');
        }
        // Numeric value validate
        if(password.match('(?=.*[0-9])')) {
            $('.digit').addClass('list-active');
        }
        else {
            $('.digit').removeClass('list-active');
        }
        // Special character validate
        if(password.match('(?=.*[!@.])')) {
            $('.special').addClass('list-active');
        }
        else {
            $('.special').removeClass('list-active');
        }
        // Length validate
        if(password.length >= 8 && password.length <= 24) {
            $('.length').addClass('list-active');
        }
        else {
            $('.length').removeClass('list-active');
        }
        // Password validate container hide (or) show
        if(password.match('(?=^.{8,}$)(?=.*\\d)(?=.*[!@.]+)(?![.\\n])(?=.*[A-Z])(?=.*[a-z])')) {
            $('.password-validation-container').hide();
        }
        else {
            $('.password-validation-container').show();
        }

        if(password.length === 24) {
            $('#Password').attr('readonly', true);
        }
    });
    // For Stopping if character exceeds more than 24 characters
    $(document).on('click', '#Password', function (){
        if($('#Password').attr('readonly') && $('#Password').val().length === 24) {
            $('#Password').removeAttr('readonly');
        }
        // If password length equal to 24 only backspace works
        $(document).on('keydown', '#Password', function (e){
            if(e.which !== 8 && $('#Password').val().length === 24){
                $('#Password').attr('readonly', true);
            }
        });

    });
});

/* --- Password Reset Form ---*/
$(document).on('submit', '#PasswordResetForm', function (e){
    e.preventDefault();

    $.validator.addMethod('strong',
        function () {
        return /(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])/.test(value)
        }, 'Password must contain mentioned below.')

    $('#PasswordResetForm').validate({
        focusCleanup: true,
        focusInvalid: false,
        ignore: '.ignore',
        debug: true,
        rules: {
            password: {
                required: true,
                strong: true,
                minlength: 8,
            },
            confirm_password: {
                required: true,
                equalTo: '#Password',
            },
        },
        errorPlacement: function (error, element) {
            const ele = $(element).attr('id');
            error.insertAfter('#'+ele+'Validate');
        },
        messages: {
            password: {
                minlength: 'Password must contain at least 8 characters',
            },
            confirm: {
                equalTo: 'Confirm Password doesn\'t match Password',
            },
        },
    });

    $('#PasswordResetForm').validate();
    if($('#PasswordResetForm').valid()){
        $('#Reset-Pwd-Btn').hide();
        $('#spinner-button').show();
        const form_data = new FormData($('#PasswordResetForm')[0]);
        const form = Object.fromEntries(form_data.entries());

        $.ajax({
            type: 'POST',
            url: 'url_for(password_reset)',
            data: JSON.stringify(form),
            contentType: 'application/json',
            success: function (response) {
                $('#Reset-Pwd-Btn').show();
                $('#spinner-button').hide();
                if(response['status'] === 'PasswordUpdated') {
                    $('.Password-reset-container').eq(0).addClass('inactive');
                    $('.Password-reset-container').eq(1).removeClass('inactive');
                }
            },
            error: function () {
                $('#Reset-Pwd-Btn').show();
                $('#spinner-button').hide();
                alert('Something went wrong. Try again later.');
                window.location.href = '/'
            },
        });
    }
});

$(document).on('click', '#Login-As', function () {
    const loginAs = $(this).attr('data-type');
    $('#login-button').attr('data-userinfo', loginAs);
});

$(document).on('click', '#Register-As', function () {
    const regAs = $(this).attr('data-register-as');
    if (regAs === 'Donor') {
        window.location.href = '/register-as-donor';
    }
    else {
        window.location.href = '/register-as-org';
    }
});