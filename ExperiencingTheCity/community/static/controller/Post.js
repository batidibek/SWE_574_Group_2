$(document).ready(function(){ 
    $('input[type="file"]').change(function(e){ 
        var idVal = $(this).attr('id');
        var geekss = e.target.files[0].name; 

        labels = document.getElementsByTagName('label');
        for( var i = 0; i < labels.length; i++ ) {
            if (labels[i].htmlFor == idVal)
                labels[i].innerHTML = geekss;
        }
    }); 
}); 