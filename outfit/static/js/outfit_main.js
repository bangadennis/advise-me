$(document).ready(function() {
    //delete activity
      $('.delete_activity').click(function()
            {
            var ans=confirm("Are you sure you want to delete that Activity/Event");
            if (ans) {
            var parent = $(this).parent();
                    
                    $.ajax({
                            type: 'get',
                            url: '/auth/delete_activity/',
                            data: {activity_id: parent.attr('id')},
                            beforeSend: function() {
                                $(parent.attr('id')).animate({'backgroundColor':'#fb6c6c'},300);
                            },
                            success: function() {
                                    parent.slideUp(300,function() {
                                            $(parent.attr('id')).remove();
                                    });
                            }
                    });
            }
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
      
      //Map Button
      $('.btn-show').click(function(){
        $(this).hide();
      });
      
      //Search function
      $('.search_cloth').keyup(function()
            {
            var ans=confirm("Are you sure you want to delete that Activity/Event");
            var search = $(this).value;
            alert(search);
            $.ajax({
                  type: 'get',
                  url: '/auth/search_closet/',
                  data: {search_name: search},
                  success: function() {
                  }
            });
      });
      
     
      //Image preview function       
      $('#id_cloth_image').change(function(){
                var oFReader = new FileReader();
                oFReader.readAsDataURL(document.getElementById("id_cloth_image").files[0]);
        
                oFReader.onload = function (oFREvent) {
                    document.getElementById("uploadPreview").src = oFREvent.target.result;
                };
      });
      
});