$(document).ready(function(){
    $('#frm-start-date').datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true
    });
});

$(document).ready(function(){
    $('#frm-end-date').datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true
    });
});

$(document).ready(function(){
    $('#frm-delivery-date').datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true
    });
});

$(document).ready(function() {
    $(".delete").click(function() {
        var deleteUrl = $(this).data("delete-url");
        var itemId = $(this).data("item-id");
        $("#frm-item-id").attr('value', itemId);
        $('#confirm-delete').attr('action', deleteUrl);
    });
});