$(document).on('click', '.Action', function () {
    $('.action').attr('disabled', true);
    const buttonID = $(this).attr('id');
    const dataEmail = $(this).attr('data-email');
    const dataIndex = parseInt($(this).attr('data-index'));

    let data;
    if (buttonID === 'ApproveButton') {
        data = {'email': dataEmail, 'action': 'approve'};
    }
    else {
        data = {'email': dataEmail, 'action': 'decline'};
    }
    $.ajax({
        type: 'POST',
        url: '/Administrator',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function (response){
            if(response['action'] === 'Approved') {
                swal.fire({
                    title: 'You\'ve approved this organisation.',
                    icon: 'success',
                    confirmButtonColor: '#0d6efd',
                }).then((result) => {
                    if(result) {
                        $('tr[id=ID'+ dataIndex +'] td:gt(1)').html('<span>' + response['action'] + '</span>');
                    }
                });
            }
            else {
                swal.fire({
                    title: 'You\'ve declined this organisation.',
                    icon: 'info',
                    confirmButtonColor: '#0d6efd',
                }).then((result) => {
                    if(result) {
                        $('tr[id=ID'+ dataIndex +'] td:gt(1)').html('<span>' + response['action'] + '</span>');
                    }
                });
            }
        },
        error: function () {
            alert('Something went wrong. Try again later.');
            window.location.href = '/administrator-login'
        },
    })
});

$(document).on('click', '.LeftPane',function (){
    const ele_id = $(this).attr('id');

    if (ele_id === 'LP1') {
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
        // tables
        if (!$('.Table1').hasClass('active')) {
            $('.Table1').addClass('active');
        }
        if ($('.Table2').hasClass('active')) {
            $('.Table2').removeClass('active');
        }
        if ($('.Table3').hasClass('active')) {
            $('.Table3').removeClass('active');
        }
    }
    else if (ele_id === 'LP2') {
        if($('#LP1').hasClass('active')) {
            $('#LP1').removeClass('active');
        }
        if(!$('#LP2').hasClass('active')) {
            $('#LP2').addClass('active');
        }
        if($('#LP3').hasClass('active')) {
            $('#LP3').removeClass('active');
        }
        if ($('.Table1').hasClass('active')) {
            $('.Table1').removeClass('active');
        }
        if (!$('.Table2').hasClass('active')) {
            $('.Table2').addClass('active');
        }
        if ($('.Table3').hasClass('active')) {
            $('.Table3').removeClass('active');
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
        if($('.Table1').hasClass('active')) {
            $('.Table1').removeClass('active');
        }
        if($('.Table2').hasClass('active')) {
            $('.Table2').removeClass('active');
        }
        if(!$('.Table3').hasClass('active')) {
            $('.Table3').addClass('active');
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
    if($('.Table3').css('display') !== 'none') {
        $('#Table3 tr').filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(data) > -1);
        })
    }
})