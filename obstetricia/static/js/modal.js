$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-paciente").modal("show");
      },
      success: function (data) {
        $("#modal-paciente .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {

          $("#modal-paciente").modal("hide");
          alert('Se han Validado los Datos Correctamente');
        }
        else {
          $("#modal-paciente .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create paciente
  $(".js-paciente").click(loadForm);
  $("#modal-paciente").on("submit", ".js-paciente-form", saveForm);
  
  $(".js-paciente-edit").click(loadForm);
  $("#modal-paciente").on("submit", ".js-paciente-edit-form", saveForm);

  $(".js-delete").click(loadForm);
  $("#modal-paciente").on("submit", ".js-delete-form", saveForm);

 
});