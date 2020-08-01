$(function () {

  $(".js-paciente-edit").click(function () {
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

  $("#modal-paciente").on("submit", ".js-paciente-edit-form", function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) { 
          $('#modal-paciente').modal('hide');
          alert("Paciente Registrado!");
          return false;
        }
        else {
          $("#modal-paciente .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  });
});
});
