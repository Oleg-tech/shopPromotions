$(document).ready(function(){
    console.log('test')
    $(".orderButton").on("click", function(event){
        event.preventDefault();

        $(".right_info").each(function() {
            console.log($(this).attr('id'));
//            if (res.ordering == $(this).attr('id')) {
//                console.log($(this).attr('id'));
//            }
        });
        console.log($(".right_info").html())
        var _filterObj = {};
        var _shopObj = {};
        var order = $(this).val();
        _filterObj['ordering'] = order;
//        console.log(order)
        $(".filter-checkbox").ready(function(){
            _filterObj['csrfmiddlewaretoken']=$('input[name=csrfmiddlewaretoken]').val();
            $(".shop_present").each(function(index, ele){
                var _shopVal=$(this).val();
                var _shopKey=$(this).data('filter');
            });
//            console.log(_filterObj[''])
            $(".filter-checkbox").each(function(index, ele){
                var _filterVal=$(this).val();
                var _filterKey=$(this).data('filter');
                _filterObj[_filterKey]=Array.from(document.querySelectorAll('input[data-filter='+_filterKey+']:checked')).map(function(el){
                    return el.value;
                });
            });

            $.ajax({
                url:'/filter-data',
                data:_filterObj,
                dataType:'json',
                beforeSend:function(){
                    $(".ajaxLoader").show();
                    $(".dives").hide();
                },
                success:function(res){
                    console.log(res.order_part);
                    $("#filterProducts").html(res.data);
                    $(".right_info").html(res.order_part);
                    $(".ajaxLoader").hide();
                    $("#amount").html(res.amount);
                    $(".dives").show();
                }
            });
        });
    });
});