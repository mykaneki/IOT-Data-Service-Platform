// var app = new Vue({
//     el: '#app',
//     data: {
//     spots: [
//         { id: 'A1', status: 'empty' },
//         { id: 'A2', status: 'occupied' },
//         { id: 'A3', status: 'empty' },
//         { id: 'A4', status: 'empty' },
//         { id: 'A5', status: 'occupied' },
//         { id: 'A6', status: 'empty' },
//         { id: 'B1', status: 'occupied' },
//         { id: 'B2', status: 'empty' },
//         { id: 'B3', status: 'empty' },
//         { id: 'B4', status: 'occupied' },
//         { id: 'B5', status: 'empty' },
//         { id: 'B6', status: 'occupied' },
//         { id: 'C1', status: 'empty' },
//         { id: 'C2', status: 'occupied' },
//         { id: 'C3', status: 'occupied' },
//         { id: 'C4', status: 'empty' },
//         { id: 'C5', status: 'empty' },
//         { id: 'C6', status: 'occupied' },
//         { id: 'D1', status: 'occupied' },
//         { id: 'D2', status: 'empty' },
//         { id: 'D3', status: 'empty' },
//         { id: 'D4', status: 'occupied' },
//         { id: 'D5', status: 'empty' },
//         { id: 'D6', status: 'occupied' },
//     ]
//     }
// })

var app = new Vue({
    el: '#app',
    data: {
    spots: [
    ]
    }
})

$.ajax({
    url: 'http://127.0.0.1:5000/get_spots_status',
    type: 'GET',
    success: function(data) {
        app.spots = data.spots;
        console.log(data)
    },
    error: function() {
        alert('获取停车位状态失败');
    }
});