$(document).ready(function() {

    var shared_users_input = $("#id_shared_users");
    shared_users_input.attr("multiple", "multiple");
    shared_users_input.select2();
    shared_users_input.parent().find(".select2-container").css("width", "100%");

    var public_view_input = $("#id_public_view");
    public_view_input.click(disable_shared_users_when_public_view);

    disable_shared_users_when_public_view();

    function disable_shared_users_when_public_view() {
        if (public_view_input.prop("checked")) {
            shared_users_input.parent().parent().hide()
        } else {
            shared_users_input.parent().parent().show()
        }
    }

});