$(document).ready(function() {
    //delete activity
      $('.delete_activity').confirm({
            text: "Are you sure you want to delete that Activity",
            title: "Delete Activity",
            confirm: function(button) {
                var parent = $('.delete_activity').parent();
                    $.ajax({
                            type: 'get',
                            url: '/auth/delete_activity/',
                            data: {activity_id: parent.attr('id')},
                            beforeSend: function() {
                                    parent.animate({'backgroundColor':'#fb6c6c'},300);
                            },
                            success: function() {
                                    parent.slideUp(300,function() {
                                            parent.remove();
                                    });
                            }
                    });
            },
            cancel: function(button) {
                // nothing to do
            },
            confirmButton: "Yes",
            cancelButton: "No",
            post: true,
            confirmButtonClass: "btn-danger",
            cancelButtonClass: "btn-default",
            dialogClass: "modal-dialog modal-sm" // Bootstrap classes for large modal
        });
        //end_delete activity
        
        //delete Cloth
      $('.delete_cloth').confirm({
            text: "Are you sure you want to delete that Cloth",
            title: "Delete Cloth",
            confirm: function(button) {
                var parent = $('.delete_cloth').attr('id');
                window.location= "http://127.0.0.1:8000/auth/delete_cloth/"+parent+"/delete";
    
            },
            cancel: function(button) {
                // nothing to do
            },
            confirmButton: "Yes",
            cancelButton: "No",
            post: true,
            confirmButtonClass: "btn-danger",
            cancelButtonClass: "btn-default",
            dialogClass: "modal-dialog modal-sm" // Bootstrap classes for large modal
        });//delete cloth
});