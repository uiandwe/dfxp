/**
 * Created by hyeonsj on 15. 12. 4..
 */


jQuery( document ).ready(function($) {
   $('#pdffile').change(function(){
         $('#subfile').val($(this).val().replace("C:\\fakepath\\", ""));
    });
});