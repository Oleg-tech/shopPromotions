$(document).ready(function(){
    var _filterObj = {};
    var _shopObj = {};

    function Check() {
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
//            console.log(_filterVal)
            console.log(_filterKey)
        });
    }
    $(".loadMore").on("click", function(){

        var _currentProducts = $(".dives").length;
        var _limit = $(this).attr('data-limit');
        var _total = $(this).attr('data-total');
        Check();
//        console.log('length: ', _currentProducts, '\n', _limit, '\n');
//        console.log('filter: ', _filterObj['shops']);
        $.ajax({
            url:'/load-more-data',
            data:{
                limit: _limit,
                offset: _currentProducts,
                shops: _filterObj['shops'],
                cats: _filterObj['categories'],
            },
            dataType:'json',
            beforeSend:function(){
                $(".loadMore").attr('disabled', true);
            },
            success:function(res){
                $('#filterProducts').append(res.data);
                $(".loadMore").attr('disabled', false);

                console.log(res.limiter);

                if(res.limiter == False) {
                    $(".loadMore").remove();
                };

                var _totalProducts = $(".dives").length;
            }
        });
    });
});