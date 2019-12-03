// function getCookie(c_name)
// {
//     if (document.cookie.length > 0)
//     {
//         c_start = document.cookie.indexOf(c_name + "=");
//         if (c_start != -1)
//         {
//             c_start = c_start + c_name.length + 1;
//             c_end = document.cookie.indexOf(";", c_start);
//             if (c_end == -1) c_end = document.cookie.length;
//             return unescape(document.cookie.substring(c_start,c_end));
//         }
//     }
//     return "";
//  }

function playbackresponse(resp){
    //  console.log(resp);
     var count = 0;
    //  console.log(resp[0]['vehicle_id']);
$('#vehicle_id_field').empty();
    // .find('option')
    // .remove()
    // .end();
    $("#vehicle_id_field").append('<option value=' + -1 + '>' + "None" + '</option>');
    // $("#vehicle_id_field").val($("#vehicle_id_field option:first").val());
    $("#vehicle_id_field option:first").attr('selected','selected');

  for (var i=0; i < resp.length;++i){
    //   console.log(resp[i]['vehicle_id'])
      count++;
    $("#vehicle_id_field").append('<option value=' + resp[i]['vehicle_id'] + '>' + resp[i]['vehicle_id'] + '</option>');
    // addOption(document.getElementById("vehicle_id_field"), resp[i]['vehicle_id'], resp[i]['vehicle_id']);
  }
  console.log(count);

   }
$(document).ready(function() {

   

    $("#starttime").blur( function(event) {
        // alert("You changed the button using JQuery!" + $(this).val());
        urll = "/updatestart/";
        //urll = "{% url 'playback:update-end' %}"
        $.ajax({
            url:urll,
            type: 'get',
            data:  {start_time:$(this).val()},
             success: function(resp){
                 playbackresponse(resp);    
               }
    
        });
    });
    $("#endtime").blur( function(event) {
        // alert("You changed the button using JQuery!" + $(this).val());
        urll = "/updateend/";
        $.ajax({
            url:urll,
            type: 'get',
            data:  {end_time:$(this).val()},
             success: function(resp){
                playbackresponse(resp);
               }
    
        });
    });
    
    $("#vehicle_id_field").change( function(event) {
    urll = '/updatevehicle/';
    $.ajax({
        url:urll,
        type: 'get',
        data:  {vehicle_id:$(this).val()},
         success: function(resp){
            //  playbackresponse(resp);    
           }
    });
});

    $("#route_id_field").change( function(event) {
        // alert("You changed the button using JQuery!" + $(this).val());
        urll = "/vehiclesonroute/";
        $.ajax({
            url:urll,
            // headers: { "X-CSRFToken": getCookie("csrftoken") },
            type: 'get',
            // headers: { "X-CSRFToken": $.cookie("csrftoken") },
            data:  {route_id:$(this).val()},
             success: function(resp)
             {
                 playbackresponse(resp);
             }
    
        });
    });
    });