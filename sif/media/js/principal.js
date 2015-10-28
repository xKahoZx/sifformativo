$(function(){
	$("#id_tipo_salida").change(function(){
		if ($("#id_tipo_salida").val() == "Cliente"){
			$("#id_numero_contrato").show();
			$("label[for='id_numero_contrato']").show();
		}else{
			$("#id_numero_contrato").hide();
			$("label[for='id_numero_contrato']").hide();
		}
	});
	$("#id_codigobarras").scannerDetection({stopPropagation:true,preventDefault:true},function(datos){
		$("#id_cantidad").focus();
	});
	$('.datepicker').pickadate({
    	selectMonths: true, // Creates a dropdown to control month
    	selectYears: 15 // Creates a dropdown of 15 years to control year
  	});
  	 $('.parallax').parallax();
  	 //$('select').material_select();
	$('select').material_select();
	$(".button-collapse").sideNav();
	$('.modal-trigger').leanModal();
	$('.datepicker').pickadate({
		selectMonths: true, // Creates a dropdown to control month
		selectYears: 15 // Creates a dropdown of 15 years to control year
	});
});