$(document).ready(function(){
    $(".ajaxLoader").hide();

    $(".filter-checkbox").on("click", function(){
        var _filterObj = {};

       _filterObj['ordering'] = $(".orderButton").val();
        _filterObj['csrfmiddlewaretoken']=$('input[name=csrfmiddlewaretoken]').val();
        console.log($('input[name=csrfmiddlewaretoken]').val())
        var _shopObj = {};
        $(".shop_present").each(function(index, ele){
            var _shopVal=$(this).val();
            var _shopKey=$(this).data('filter');
        });

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
                $("#filterProducts").html(res.data);
                $(".ajaxLoader").hide();
                $("#amount").html(res.amount)
                $(".dives").show();

                if(res.limiter == false) {
                    $(".loadMore").remove();
                };
            }
        });
    });
});