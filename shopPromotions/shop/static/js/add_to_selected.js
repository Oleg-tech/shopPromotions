$(document).ready(function(){

    $(".like-form").submit(function(e){
        e.preventDefault()
        const post_id = $(this).attr('id')
        console.log($('input[name=csrfmiddlewaretoken]').val())

        $.ajax({
            type:'POST',
            url: '/add_selected_to_model',
            dataType: 'json',
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'post_id': post_id,
            },
            success: function(){
                $("#"+post_id).remove();
//                $("#product_"+post_id).html(response.data);
            },
            error: function(response){
                console.log('error');
            }
        });
    });
});