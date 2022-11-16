/* --- UserValidateHide OnClick--- */
$(document).on('focus', '#E-mail', function () {
    if($('#UserExistValidate').attr('class')){
        $('#UserExistValidate').removeClass('error');
        $('#UserExistValidate').hide();
    }
});
/* --- Next Page --- */
// Form - 1
$(document).on('submit', '#form-1', function (e){
    e.preventDefault();
    //  Custom Validators
    $.validator.addMethod('uppercase',
        function(value) {
            return /(?=.*[A-Z])/.test(value)
        },
        'Password must contain one UpperCase character');
    $.validator.addMethod('lowercase',
        function (value) {
            return /(?=.*[a-z])/.test(value)
        },
        'Password must contain one LowerCase character');
    $.validator.addMethod('digit',
        function (value) {
            return /(?=.*[0-9])/.test(value)
        },
        'Password must contain one numeric value');
    $.validator.addMethod('special_char',
        function (value) {
            return /(?=.*[!.@])/.test(value)
        },
        'Password must contain one special character');
    // Form-1 Validate Rules
    $('#form-1').validate({
        focusCleanup: true,
        focusInvalid: false,
        ignore: '.ignore',
        debug: true,
        // Rules
        rules: {
            email: {
                required: true,
                email: true
            },
            password: {
                required: true,
                uppercase: true,
                lowercase: true,
                digit: true,
                special_char: true,
                minlength: 8,
            },
            confirm: {
                required: true,
                minlength: 8,
                equalTo: '#Password',
            },
        },
        errorPlacement: function (error, element){
            const ele = $(element).attr("id");
            error.insertAfter('#'+ele+'Validate');
        },
        // Error Message
        messages: {
            email: {
                email: 'Enter a valid email address',
            },
            password: {
                minlength: 'Your password must contain at least 8 characters',
            },
            confirm: {
                equalTo: 'Confirm Password doesn\'t match Password',
            },
        },
    });
    // Validate Call
    $('#form-1').validate();
    // Submit Form if form is valid and move to Next Form
    if($('#form-1').valid()){
        $('#SignUpButton').hide();
        $('#spinner-button1').show();
        // Current Div Class
        const f1_curr_page = $(this).parent();
        const f1_next_page = $(this).parent().next();
        // index of current and next page
        const curr_index = $('.form').index(f1_curr_page);
        const next_index = $('.form').index(f1_next_page);
        // Form Data
        const form1 = new FormData($('#form-1')[0]);
        const form = Object.fromEntries(form1.entries());
        $.ajax({
            type: 'POST',
            url: '/user-exist',
            data: JSON.stringify(form),
            contentType: 'application/json',
            success: function (response) {
                if (response['status'] === 'Exist') {
                    $('#SignUpButton').show();
                    $('#spinner-button1').hide();

                    $('#UserExistValidate').html('User Already Exist');
                    $('#UserExistValidate').attr('class', 'error');
                }
                else {
                    $('#SignUpButton').show();
                    $('#spinner-button1').hide();
                    // Form Change
                    f1_curr_page.removeClass('form-active');
                    f1_next_page.addClass('form-active');

                    // Progress Bar
                    $(".progress_bar").eq(curr_index).removeClass('inactive');
                    $(".progress_bar").eq(next_index).addClass('active');

                    // Check display
                    $(".check").eq(curr_index).addClass('active');
                    $(".initial").eq(curr_index).addClass('inactive');
                }
            }
        });
    }
});
// Phone Number Validation
$(document).ready(function (){
    $(document).on('paste', '#PhoneNumber', function (e){
        e.preventDefault();
    });
    $(document).on('keyup', '#PhoneNumber', function (){
        if($.isNumeric($('#PhoneNumber').val()) === true || $('#PhoneNumber').val() === ''){
            $('#PhoneNumberValidate').removeAttr('class');
            $('#PhoneNumberValidate').html('');
        }
        else {
            $('#PhoneNumberValidate').attr('class', 'error');
            $('#PhoneNumberValidate').html('Please enter a valid number');
        }
        if($('#PhoneNumber').val().length === 10) {
            $('#PhoneNumber').attr('readonly', true);
            $('#PhoneNumber').blur();
        }
    });
    $(document).on('click', '#PhoneNumber', function (){
         if($('#PhoneNumber').attr('readonly') && $('#PhoneNumber').val().length === 10){
             $('#PhoneNumber').removeAttr('readonly');
             $('#PhoneNumber').focus();
         }
         $(document).on('keydown', '#PhoneNumber', function (e){
             if(e.which !== 8 && $('#PhoneNumber').val().length === 10){
                 $('#PhoneNumber').attr('readonly', true);
             }
         });
    });
});
// Form-2 Submission
$(document).on('submit', '#form-2', function (e){
    e.preventDefault();
    // Form - 2 Validate
    $('#form-2').validate({
        focusCleanup: true,
        focusInvalid: false,
        ignore: '.ignore',
        debug: true,

        rules: {
            fname: {
                required: true,
            },
            lname: 'required',
            dateofbirth: 'required',
            age: 'required',
            phonenumber: {
                required: true,
                digits: true,
                minlength: 10,
            },
            bloodgroup: 'required',
            address: 'required',
            city: 'required',
            state: 'required',
            pincode: {
                required: true,
                digits: true,
            },
        },
        errorPlacement: function (error, element){
            const ele = $(element).attr("id");
            error.insertAfter('#'+ele+'Validate');
        },
    });
    // Form-2 Validation Call
    $('#form-2').validate();
    if($('#form-2').valid()){
        $('#SubmitButton').hide();
        $('#spinner-button2').show();
        // Current Div Class
        const f2_curr_page = $(this).parent();
        const f2_next_page = $(this).parent().next();
        // index of current and next page
        const curr_index = $('.form').index(f2_curr_page);
        const next_index = $('.form').index(f2_next_page);
        // Combining Two Forms into single form-data
        const form1 = new FormData($('#form-1')[0]);
        const form2 = new FormData($('#form-2')[0]);
        for(const [key, value] of form1.entries()){
            form2.append(key, value);
        }
        const form = Object.fromEntries(form2.entries());
        $.ajax({
            type: 'POST',
            url: '/form-submission',
            data: JSON.stringify(form),
            contentType: 'application/json',
            success: function (response){
                if(response['status'] === 'success'){
                    $('#SubmitButton').show();
                    $('#spinner-button2').hide();
                    // Form Change
                    f2_curr_page.removeClass('form-active');
                    f2_next_page.addClass('form-active');
                    // Progress Bar
                    $(".progress_bar").eq(curr_index).removeClass('inactive');
                    $(".progress_bar").eq(next_index).addClass('active');
                    // Check display
                    $(".check").eq(curr_index).addClass('active');
                    $(".initial").eq(curr_index).addClass('inactive');
                }
            },
            error: function () {
                $('#SubmitButton').show();
                $('#spinner-button2').hide();
            }
        });
    }
});
/* --- Previous Page --- */
$(document).on('click', '#previous', function (){
    const curr_page = $('#form-2').parent();
    const pre_page = $('#form-2').parent().prev();
    // Form Display
    curr_page.removeClass('form-active');
    pre_page.addClass('form-active');
    // Index of current and previous page
    const curr_index = $('.form').index(curr_page);
    const pre_index = $('.form').index(pre_page);
    // Progress bar reverse
    $(".progress_bar").eq(curr_index).removeClass('active');
    $(".progress_bar").eq(curr_index).addClass('inactive');

    $(".check").eq(pre_index).removeClass('active');
    $(".initial").eq(pre_index).removeClass('inactive');

});
