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
$(document).ready(function() {

    $("#starttime").change( function(event) {
        // alert("You changed the button using JQuery!" + $(this).val());
        urll = "/updatestart/"
        $.ajax({
            url:urll,
            type: 'get',
            data:  {start_time:$(this).val()},
             success: function(resp){
            //   for (var i=0; i < resp['routestops'].length;++i){
    
            //     addOption(document.getElementById("vehicle_id_field"), resp['vehicle_id'][i], resp['vehicle_id'][i]);
            //   }
    
               }
    
        });
    });
    $("#endtime").change( function(event) {
        // alert("You changed the button using JQuery!" + $(this).val());
        urll = "/updatestart/"
        $.ajax({
            url:urll,
            type: 'get',
            data:  {start_time:$(this).val()},
             success: function(resp){
            //   for (var i=0; i < resp['routestops'].length;++i){
    
            //     addOption(document.getElementById("vehicle_id_field"), resp['vehicle_id'][i], resp['vehicle_id'][i]);
            //   }
    
               }
    
        });
    });
    $("#route_id_field").change( function(event) {
        // alert("You changed the button using JQuery!" + $(this).val   ());
        urll = "/vehiclesonroute/";
        $.ajax({
            url:urll,
            // headers: { "X-CSRFToken": getCookie("csrftoken") },
            type: 'get',
            // headers: { "X-CSRFToken": $.cookie("csrftoken") },
            data:  {route_id:$(this).val()},
             success: function(resp){
              for (var i=0; i < resp['routestops'].length;++i){
    
                addOption(document.getElementById("vehicle_id_field"), resp['vehicle_id'][i], resp['vehicle_id'][i]);
              }
    
               }
    
        });
    
    
    
    });
    // $(function(){  
    //     $("select#id_prodtopcat").change(function(){
    //       $.getJSON("/products/feeds/subcat/"+$(this).val()+"/", function(j) {
    //         var options = '<option value="">---------- </option>';
    //         for (var i = 0; i < j.length; i++) {
    //           options += '<option value="' + parseInt(j[i].pk) + '">' + j[i].fields['longname'] + '</option>';
    //         }
    //         $("#id_prodsubcat").html(options);
    //         $("#id_prodsubcat option:first").attr('selected', 'selected');
    //         $("#id_prodsubcat").attr('disabled', false);
    //       })
    //       $("#id_prodtopcat").attr('selected', 'selected');
    //     })
    //   })
    });