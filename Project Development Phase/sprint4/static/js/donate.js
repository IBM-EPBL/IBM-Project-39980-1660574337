$(document).on('change', '.DonoteFilter', function () {
    let data;
    data = {'state': $('#DonorStateFilter').val(), 'city': $('#DonorCityFilter').val(), 'locality': $('#DonorLocalityFilter').val()};

    $.ajax({
        type: 'POST',
        url: '/donate-plasma',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function (response) {
            const table_data = response['filter'];
            $('#TableData').empty();
            for(let i=0; i<table_data.length; i++) {
                $('#TableData').append('<tr>' +
                    '<td style="margin: auto 0">' + (i + 1) + '</td>' +
                    '<td>' + table_data[i]['NAME'] + '</td>' +
                    '<td>' + table_data[i]['LOCALITY'] + '</td>' +
                    '<td>' + table_data[i]['CITY'] + '</td>' +
                    '<td>' + table_data[i]['STATE'] + '</td>' +
                    '<td>' + table_data[i]['PINCODE'] + '</td>' +
                    '<td>' +
                    '<button class="btn btn-primary btn-sm" data-email="{{' + table_data[i]['EMAIl'] + '}}">Donate</button>\n' +
                    '</td>' +
                    '</tr>')
            }
            if(response['filter_city_select'] === 'YES') {
                const city = response['filterCity']
                $('#DonorCityFilter').empty();
                $('#DonorCityFilter').append('<option value="all">All</option>');
                for(let i=0; i<city.length; i++) {
                    if(city[i] === data['city']) {
                        $('#DonorCityFilter').append('<option selected value='+ city[i] +'>'+ city[i] +'</option>');
                    }
                    else {
                        $('#DonorCityFilter').append('<option value='+ city[i] +'>'+ city[i] +'</option>');
                    }
                }
            }
            if(response['filter_locality_select'] === 'YES') {
                const locality = response['filterLocality']
                $('#DonorLocalityFilter').empty();
                $('#DonorLocalityFilter').append('<option value="all">All</option>');
                for(let i=0; i<locality.length; i++) {
                    if(locality[i] === data['locality']) {
                        $('#DonorLocalityFilter').append('<option selected value='+ locality[i] +'>'+ locality[i] +'</option>');
                    }
                    else {
                        $('#DonorLocalityFilter').append('<option value='+ locality[i] +'>'+ locality[i] +'</option>');
                    }
                }
            }
            if(response['filter_state_select'] === 'YES') {
                const state = response['filterState']
                $('#DonorStateFilter').empty();
                $('#DonorStateFilter').append('<option value="all">All</option>');
                for(let i=0; i<state.length; i++) {
                    if(state[i] === data['state']) {
                        $('#DonorStateFilter').append('<option selected value='+ state[i] +'>'+ state[i] +'</option>');
                    }
                    else {
                        $('#DonorStateFilter').append('<option value='+ state[i] +'>'+ state[i] +'</option>');
                    }
                }
            }
        },
        error: function () {
            alert('ERROR');
        },
    })
});

$(document).on('keyup', '#OrgSearch', function () {
    const search = $(this).val().toLowerCase();
    $('#TableData tr').filter(function () {
        $(this).toggle(($(this).text().toLowerCase().indexOf(search) > -1));
    });
})

$(document).on('click', '#DonateButton', function () {
    $('#bg-spin').css('display', 'flex');
    const email = $(this).attr('data-email');
    const name = $(this).attr('data-name');
    $.ajax({
        type: 'POST',
        url: '/donate-plasma',
        data: JSON.stringify({'email': email, 'name': name}),
        contentType: 'application/json',
        success: function (response) {
            $('#bg-spin').hide();
            if (response['donate_req_status'] === 'Success') {
                swal.fire({
                    title: 'Your request has been sent successfully.',
                    text: 'You can view your request status in your profile.',
                    confirmButtonColor: '#0d6efd',
                    icon: 'success',
                });
            }
            else if (response['donate_req_status'] === 'Already') {
                swal.fire({
                    text: 'Your had already made a request to this organisation.',
                    confirmButtonColor: '#0d6efd',
                    icon: 'info',
                });
            }
            else {
                swal.fire({
                    title: 'You have made maximum number of request.',
                    text: 'Try again after 48 hours.',
                    confirmButtonColor: '#0d6efd',
                    icon: 'info',
                });
            }
        },
        error: function () {
            alert('ERROR');
        },
    });
})

$(document).on('click', '#CancelButton', function () {
    $('#bg-spin').css('display', 'flex');
    const orgEmail = $(this).attr('data-org-email');
    $.ajax({
        type: 'POST',
        url: '/donor-profile',
        data: JSON.stringify({'org-email': orgEmail}),
        contentType: 'application/json',
        success: function (response) {
            $('#bg-spin').hide();
            if (response['CancelStatus'] === 'True') {
                swal.fire({
                    text: 'Your request has be cancelled.',
                    icon: 'info',
                    confirmButtonColor: '#0d6efd',
                }).then((result) => {
                    if (result) {
                        location.reload();
                    }
                });
            }
        },
        error: function () {
            alert('ERROR');
        },
    })
})