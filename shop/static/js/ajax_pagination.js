function ajaxPagination() {
    $("#pagination a.page-link").each(function(index, el) {
        $(el).click(function(e){
            e.preventDefault();

            let page_url = $(el).attr('href')
            console.log(page_url)
            $.ajax({
                url: page_url,
                type: 'GET',
                success: function(data){
                    console.log(data);
                    $("#test_block").empty();
                    $("#test_block").append($(data).filter('#test_block').html())

                    $("#pagination").empty();
                    $("#pagination").append($(data).find('#pagination').html())
                }
            });
        });
    });
}

$(document).ready(function(){
    ajaxPagination()
});

$(document).ajaxStop(function(){
    ajaxPagination()
});