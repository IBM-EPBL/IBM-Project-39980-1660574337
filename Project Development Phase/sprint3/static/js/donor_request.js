/* Filter by Blood Group */
$(document).on('change', 'input[type=checkbox]', function () {
    const element_id = $(this).attr('id');
    if(element_id === 'BloodGroupCheckBox') {
        let data = {'state': $('#Filter_State').val(), 'city': $('#Filter_City').val(), 'blood_group': get_checked_BloodGroup_values()};
        changeTableContent(data);
    }
    else if(element_id === 'TableData') {
        if($('input:checkbox[id=TableSelectAll]').is(':checked')) {
            $('input:checkbox[id=TableSelectAll]').prop('checked', false);
        }
    }
    else if(element_id === 'TableSelectAll') {
        if($('input:checkbox[id=TableSelectAll]').is(':checked')) {
            $('input:checkbox[id=TableData]').prop('checked', true);
        }
        else {
            $('input:checkbox[id=TableData]').prop('checked', false);
        }
    }
})
/* function to filter donors by blood-group */
function get_checked_BloodGroup_values() {
    let arr = [];
    $('input:checkbox[id=BloodGroupCheckBox]:checked').each(function () {
        arr.push($(this).val());
    });
    if(arr.length > 0) {
        return (arr);
    }
    else {
        return ('all');
    }
}
/* Function to get selected user's emails */
function CheckBoxData() {
    let arr = [];
    $('input:checkbox[id=TableData]:checked').each(function () {
        arr.push($(this).val());
    });
    return (arr)
}
/* Send Mail Button */
$(document).on('click', '#SendRequestButton', function () {
    let user_email;
    user_email = CheckBoxData();
    if(user_email.length > 0) {
        const mails = {'emails': user_email};
        $.ajax({
            type: 'POST',
            url: '/donor-request',
            data: JSON.stringify(mails),
            contentType: 'application/json',
            success: function (response) {
                if(response['mail_sent'] === 'Sent'){
                    swal.fire({
                        text: "Request has been sent.",
                        icon: "success",
                        confirmButtonColor: '#0d6efd',
                    });
                }
            },
            error: function () {
                alert('Something went wrong. Try again later.');
                window.location.href = '/'
            },
        });
    }
    else {
        swal.fire({
            text: "Please select the donor before sending request.",
            icon: "info",
            confirmButtonColor: '#0d6efd',
        })
    }
})
/* Filter by STATE & CITY */
$(document).on('change', '.FILTER', function (){
    const element_id = $(this).attr('id'); let data;
    if(element_id === 'Filter_State' || element_id === 'Filter_City') {
        data = {'state': $('#Filter_State').val(), 'city': $('#Filter_City').val(), 'blood_group': get_checked_BloodGroup_values()};
        changeTableContent(data);
    }
})
/* Function to send filter-data through ajax */
function changeTableContent(data) {
    $.ajax({
        type: 'POST',
        url: '/donor-request',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function (response){
            const table_data = response['filters'];
            $('#TableContent').empty();
            // For Filtered table content
            for(let i=0; i<table_data.length; i++) {
                $('#TableContent').append('<tr>' +
                    '<th> <div class="form-check"> <input class="form-check-input" type="checkbox" value="' + table_data[i]['EMAIL'] + '" aria-label="TableData"> </div> </th>' +
                    '<th scope="row">' + (i + 1) +'</th>' +
                    '<td>'+ table_data[i]['FIRSTNAME'] + table_data[i]['LASTNAME']+'</td>' +
                    '<td>'+ table_data[i]['BLOODGROUP'] +'</td>' +
                    '<td>' + table_data[i]['EMAIL'] + '</td>' +
                    '<td>' + table_data[i]['PHONENUMBER'] + '</td>' +
                    '<td>'+ table_data[i]['CITY'] +'</td>' +
                    '<td>'+ table_data[i]['STATE']+ '</td>' +
                '</tr>');
            }
            // show entries
            const showEntries = parseInt($('#show-entries').val());
            ShowEntries(showEntries);

            if($('input:checkbox[id=TableSelectAll]').is(':checked')) {
                $('input:checkbox[id=TableSelectAll]').prop('checked', false);
            }
            // For City Filter Tab
            if(response['filter_by'] === 'State') {
                const city = response['filter1_city']
                $('#Filter_City').empty();
                $('#Filter_City').append('<option value="all">All</option>');
                for(let i=0; i<city.length; i++) {
                    if(city[i] === data['city']) {
                        $('#Filter_City').append('<option selected value='+ city[i] +'>'+ city[i] +'</option>');
                    }
                    else {
                        $('#Filter_City').append('<option value='+ city[i] +'>'+ city[i] +'</option>');
                    }
                }
            }
        },
        error: function () {
            alert('Something went wrong. Try again later.');
            window.location.href = '/'
        },
    });
}

/* Search Bar */
$(document).on('keyup', '#Search', function () {
    const search = $(this).val().toLowerCase();
    const showEntries = parseInt($('#show-entries').val());
    let trNum = 0;
    $('#TableContent tr').each(function () {
        if($(this).text().toLowerCase().indexOf(search) > -1) {
            trNum++;
            if (trNum <= showEntries) {
                $(this).show();
            }
            else {
                $(this).hide();
            }
        }
        else {
            $(this).hide();
        }
    });
    // Button hide & show
    if (trNum <= showEntries) {
        $('#NextPage').addClass('inactive');
        $('#PrevPage').addClass('inactive');
    }
    else {
        if ($('#NextPage').hasClass('inactive')) {
            $('#NextPage').removeClass('inactive');
        }
        if ($('#PrevPage').hasClass('inactive')) {
            $('#PrevPage').removeClass('inactive');
        }
    }
})
/* On Ready Show Entries */
$(document).ready(function (){
    let trNum = 0;
    const showEntries = parseInt($('#show-entries').val());
    $('table tbody tr').each(function () {
        trNum++;
        if(trNum > showEntries) {
            $(this).hide();
        }
        else {
            $(this).show();
        }
    });
    $('#Showing-entries').html('Showing ' + showEntries + ' of ' + $('table tbody tr').length);
})
/* Show Entries */
$('#show-entries').on('change', function () {
    const showEntries = parseInt($(this).val());
    ShowEntries(showEntries);
})
/* Show Entries Function */
function ShowEntries(showEntries) {
    let trNum = 0, end = 0;
    const totalRows = $('table tbody tr').length;
    const pageIndex = parseInt($('#PrevPage').attr('data-page'));
    if (pageIndex !== 1) {
        $('#NextPage').attr('data-page', '1');
        $('#PrevPage').attr('data-page', '1');
        if ($('#PrevPage').hasClass('active')) {
            $('#PrevPage').removeClass('active');
        }
    }
    const search = $('#Search').val().toLowerCase();
    if(search) {
        $('table tbody tr').each(function () {
            if ($(this).text().toLowerCase().indexOf(search) > -1) {
                trNum++;
                if(trNum > showEntries) {
                    $(this).hide();
                }
                else {
                    if (end < trNum) {
                        end = trNum;
                    }
                    $(this).show();
                }
            }
        });
    }
    else {
        $('table tbody tr').each(function () {
            trNum++;
            if(trNum > showEntries) {
                $(this).hide();
            }
            else {
                if (end < trNum) {
                    end = trNum;
                }
                $(this).show();
            }
        });
    }
    let pageNum;
    if(totalRows > showEntries) {
        pageNum = Math.ceil(totalRows/showEntries);
    }
    else {
        pageNum = null;
    }
    if(pageNum === null) {
        $('#NextPage').addClass('inactive');
        $('#PrevPage').addClass('inactive');

        $('#NextPage').removeClass('active');
        $('#PrevPage').removeClass('active');
    }
    else {
        $('#NextPage').removeClass('inactive');
        $('#PrevPage').removeClass('inactive');

        $('#NextPage').addClass('active');
    }
    $('#Showing-entries').html('Showing ' + end + ' of ' + $('table tbody tr').length);
}

/* Pagination */
$('.pageIndex').on('click', function (){
    let pageIndex, pageNum, totalRows;
    const search = $('#Search').val().toLowerCase();
    const showEntries = parseInt($('#show-entries').val());
    // Total Rows
    if (search) {
        totalRows = 0;
        $('table tbody tr').each(function () {
            if ($(this).text().toLowerCase().indexOf(search) > -1) {
                totalRows++;
            }
        });
    }
    else {
        totalRows = $('table tbody tr').length;
    }
    // Page number
    if(totalRows > showEntries) {
        pageNum = Math.ceil(totalRows/showEntries);
    }

    if($(this).attr('id') === 'NextPage') {
        pageIndex = parseInt($('#NextPage').attr('data-page'))+1;
        if (pageIndex <= pageNum) {
            display_rows(pageIndex, showEntries, totalRows, search);
            $('#NextPage').attr('data-page', pageIndex);
            $('#PrevPage').attr('data-page', pageIndex);
        }
    }
    else {
        pageIndex = parseInt($('#PrevPage').attr('data-page'))-1;
        if(pageIndex >= 1) {
            display_rows(pageIndex, showEntries, totalRows, search);
            $('#NextPage').attr('data-page', pageIndex);
            $('#PrevPage').attr('data-page', pageIndex);
        }
    }
    // Previous Page Button
    if(pageIndex <= 1) {
        $('#PrevPage').removeClass('active');
    }
    else {
        $('#PrevPage').addClass('active');
    }
    // Next Page Button
    if(pageIndex >= pageNum) {
        $('#NextPage').removeClass('active');
    }
    else {
        $('#NextPage').addClass('active');
    }
})
/* Function To Display Rows */
function display_rows(pageIndex, showEntries, totalRows, search) {
    let trNum = 0, end;
    if (search) {
        $('table tbody tr').each(function () {
            if ($(this).text().toLowerCase().indexOf(search) > -1) {
                trNum++;
                if (trNum > (pageIndex * showEntries) || trNum <= ((pageIndex * showEntries) - showEntries)) {
                    $(this).hide();
                }
                else {
                    if (trNum === (pageIndex * showEntries) || trNum === totalRows) {
                        end = trNum;
                    }
                    $(this).show();
                }
            }
        });
    }
    else {
        $('table tbody tr').each(function () {
            trNum++;
            if (trNum > (pageIndex * showEntries) || trNum <= ((pageIndex * showEntries) - showEntries)) {
                $(this).hide();
            }
            else {
                if (trNum === (pageIndex * showEntries) || trNum === totalRows) {
                    end = trNum;
                }
                $(this).show();
            }
        });
        $('#Showing-entries').html('Showing ' + end + ' from ' + $('table tbody tr').length);
    }
}