 var overviews;
 var init = 0;


 $(function() {
     if (init != 0)
         return;
     init = 1;

     $('#sel1').html('<option selected hidden>Toy Story (1995)</option>');
     $('#sel2').html('<option selected hidden>Lion King, The (1994)</option>');
     $('#sel3').html('<option selected hidden>Aladdin (1992)</option>');

     $("#form-button").on("click", function() {
         //$('#recom_message').html('').css({'margin-bottom': '30px'});
         //$('#recom_result').hide();

         var params = $('#recom-form').serialize();
         $.ajax({
             type: 'GET',
             url: '/recommender/recommender?' + params,
             success: function(recom_results) {
                 //$('#recom_message').html('Recommended movies for you: ');
                 //$('#recom_results').html(recom_results['img_urls']);
                 var img_urls = recom_results['img_urls'];
                 for (i = 0; i < 6; i++) {
                     $('#image' + (i + 1)).attr('src', img_urls[i]);
                 }
                 //$('#recom_result').show();
                 overviews = recom_results['overviews'];
             }
         })


     })

     $.ajax({
         type: 'GET',
         url: '/recommender/recommender?cmd=get_movie_list',
         success: function(response) {
             var movie_list = response['movie_list'];
             var select_opt1 = '<option selected hidden>Toy Story (1995)</option>';
             $('#sel1').html(select_opt1 + movie_list);
             var select_opt2 = '<option selected hidden>Lion King, The (1994)</option>';
             $('#sel2').html(select_opt2 + movie_list);
             var select_opt3 = '<option selected hidden>Aladdin (1992)</option>';
             $('#sel3').html(select_opt3 + movie_list);
         }
     })



     function on_button_click() {
         var x = document.getElementById('recom_result');
         if (x.style.display === 'none') {
             x.style.display = 'block';
         } else {
             x.style.display = 'none';
         }
     }

     $("#show-button").on("click", on_button_click)

     for (i = 0; i < 6; i++) {
         $('#image' + (i + 1)).mouseenter(
             function() {
                 var src = $(this).attr('src');
                 $('#select-image').attr('src', src);
                 var index = $(this).attr('index');
                 $('#overview').text(overviews[index - 1]);
             }
         )

     }
 })