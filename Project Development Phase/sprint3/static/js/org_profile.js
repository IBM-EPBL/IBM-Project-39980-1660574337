$(document).on('click', '.LeftPane',function (){
    const ele_id = $(this).attr('id');

    if (ele_id === 'LP1') {
        $('#OrgTableFilter').val('all');
        // Tabs
        if(!$('#LP1').hasClass('active')) {
            $('#LP1').addClass('active');
        }
        if($('#LP2').hasClass('active')) {
            $('#LP2').removeClass('active');
        }
        if($('#LP3').hasClass('active')) {
            $('#LP3').removeClass('active');
        }
        // containers
        if(!$('#Tab1').hasClass('active')) {
            $('#Tab1').addClass('active');
        }
        if($('#Tab2').hasClass('active')) {
            $('#Tab2').removeClass('active');
        }
        // tables
        if (!$('.Table1').hasClass('active')) {
            $('.Table1').addClass('active');
        }
        if ($('.Table2').hasClass('active')) {
            $('.Table2').removeClass('active');
        }
    }
    else if (ele_id === 'LP2') {
        $('#OrgTableFilter').val('all');
        if($('#LP1').hasClass('active')) {
            $('#LP1').removeClass('active');
        }
        if(!$('#LP2').hasClass('active')) {
            $('#LP2').addClass('active');
        }
        if($('#LP3').hasClass('active')) {
            $('#LP3').removeClass('active');
        }
        if(!$('#Tab1').hasClass('active')) {
            $('#Tab1').addClass('active');
        }
        if($('#Tab2').hasClass('active')) {
            $('#Tab2').removeClass('active');
        }
        if ($('.Table1').hasClass('active')) {
            $('.Table1').removeClass('active');
        }
        if (!$('.Table2').hasClass('active')) {
            $('.Table2').addClass('active');
        }
    }
    else {
        if($('#LP1').hasClass('active')) {
            $('#LP1').removeClass('active');
        }
        if($('#LP2').hasClass('active')) {
            $('#LP2').removeClass('active');
        }
        if(!$('#LP3').hasClass('active')) {
            $('#LP3').addClass('active');
        }
        if($('#Tab1').hasClass('active')) {
            $('#Tab1').removeClass('active');
        }
        if(!$('#Tab2').hasClass('active')) {
            $('#Tab2').addClass('active');
        }
    }
})

$(document).on('submit', '#OrgDonorRegisterForm', function (e) {
    e.preventDefault();
    $('#OrgDonorRegisterForm').validate({
        focusCleanup: true,
        focusInvalid: false,
        ignore: '.ignore',
        debug: true,
        rules: {
            contact: {
                required: true,
                digits: true,
            },
        },
    });
    $('#OrgDonorRegisterForm').validate();
    if ($('#OrgDonorRegisterForm').valid()) {
        const form = new FormData($('#OrgDonorRegisterForm')[0]);
        const data = Object.fromEntries(form.entries());

        $.ajax({
            type: 'POST',
            url: '/org-profile',
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function (response) {
                if (response['status'] === 'Done') {
                    swal.fire({
                        title: 'Donor added successfully.',
                        icon: 'success',
                        confirmButtonColor: '#0d6efd',
                    }).then((result)=>{
                        if (result) {
                            $('#OrgDonorRegisterForm')[0].reset();
                        }
                    });
                }
                else {
                    swal.fire({
                        title: 'Donor already added.',
                        icon: 'info',
                        confirmButtonColor: '#0d6efd',
                    }).then((result)=>{
                        if (result) {
                            $('#OrgDonorRegisterForm')[0].reset();
                        }
                    });
                }
            },
            error: function (){
                alert('ERROR');
            }
        })
    }
})

$(document).on('change', '#OrgTableFilter', function () {
    if($('.Table1').css('display') !== 'none') {
        const data = $(this).val();
        if (data === 'all') {
            $('#Table1 tr').each(function (){
                $(this).show();
            });
        }
        else {
            $('#Table1 tr').filter(function (){
                $(this).toggle($(this).text().indexOf(data) > -1)
            });
        }
    }
    if($('.Table2').css('display') !== 'none') {
        const data = $(this).val();
        if (data === 'all') {
            $('#Table2 tr').each(function (){
                $(this).show();
            });
        }
        else {
            $('#Table2 tr').filter(function (){
                $(this).toggle($(this).text().indexOf(data) > -1);
            });
        }
    }
})

$(document).on('keyup', '#OrgReqSearch', function () {
    const data = $(this).val().toLowerCase();
    if($('.Table1').css('display') !== 'none') {
        $('#Table1 tr').filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(data) > -1);
        })
    }
    if($('.Table2').css('display') !== 'none') {
        $('#Table2 tr').filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(data) > -1);
        })
    }
})

$(document).on('click', '.actionBtn', function (){
    const data = {'BtnType': $(this).attr('id'), 'Email': $(this).attr('data-donor-email')};

    $.ajax({
        type: 'POST',
        url: '/org-profile',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function (response) {
            alert('success');
        },
        error: function () {
            alert('Something went wrong. Try again later.');
            window.location.href = '/'
        },
    })
})