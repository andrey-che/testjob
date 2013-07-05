
function attacheEditable() {

    function saveValue(value, editField, url) {
        var editData = {}
        editData['value'] = value;
        editData['pk'] = editField.parent().attr("pk");
        editData['field_name'] = editField.attr("field_name");

        // Пытаемся сохранить отредактированное
        $.ajax({
            type: "POST",
            url: url,
            data: editData,

            success: function(response){
                response = $.parseJSON(response);

                // Если вернулась ошибка, то показываем сообщение и возвращаем старое значение поля
                if (response.result == false) {
                    for(var key in response.errors)
                        alert(response.errors[key]);

                    editField.html(response.oldValue)
                }

            },

            error:function (xhr, textStatus, thrownError){
                alert("Ошибка редактирования: " + thrownError);
            }
        });
    }

    // Обычное текстовое поле
    $('.edit_users').editable(
        function(value, settings) {
            saveValue(value, $(this), "/xhr_editUsers/");
            return(value);
        }
    );

    // Обычное текстовое поле
    $('.edit_rooms').editable(
        function(value, settings) {
            saveValue(value, $(this), "/xhr_editRooms/");
            return(value);
        }
    );

    // Календарь
    $('.date_edit').editable(
        function(value, settings){
            saveValue(value, $(this), "/xhr_editUsers/");
            return(value);
        },
        {type: 'datepicker', datepicker: {dateFormat: 'yy-mm-dd'}}
    );
}

function loadUsers() {
    // Прчем таблицу комнат и отображаем таблицу пользователей
    $('#RoomsTable').hide()
    $('#id_RoomsForm').hide()
    $('#UsersTable').show()
    $('#id_UsersForm').show()

    // Очистка таблицы
    $('*#dataTr').remove()

    // Загрузка таблицы
    $.get('/xhr_getUsers/', function(data) {
        data = $.parseJSON(data);
        data = $.parseJSON(data)

        for(var i=0; i<data.length; i++)
        {
            $('#UsersTable tr:last').after('<tr id="dataTr" pk="'+data[i].pk+'"><td class="edit_users" field_name="name">'+data[i].fields.name+'</td><td class="edit_users" field_name="paycheck">'+data[i].fields.paycheck+'</td><td class="date_edit" field_name="date_joined">'+data[i].fields.date_joined+'</td></tr>');
        }

        attacheEditable();
    });
}

function loadRooms() {
    // Прчем таблицу комнат и отображаем таблицу пользователей
    $('#UsersTable').hide()
    $('#id_UsersForm').hide()
    $('#RoomsTable').show()
    $('#id_RoomsForm').show()

    // Очистка таблицы
    $('*#dataTr').remove()

    // Загрузка таблицы
    $.get('/xhr_getRooms/', function(data) {
        data = $.parseJSON(data);
        data = $.parseJSON(data)

        for(var i=0; i<data.length; i++)
        {
            $('#RoomsTable tr:last').after('<tr id="dataTr" pk="'+data[i].pk+'"><td class="edit_rooms" field_name="department">'+data[i].fields.department+'</td><td class="edit_rooms" field_name="spots">'+data[i].fields.spots+'</td></tr>');
        }

        attacheEditable();
    });


}

function submitUsersForm() {
    $.ajax({
        url:"/xhr_postUsers/",
        type: "POST",
        data: $("#id_UsersForm").serialize(),

        success:function(response){
            response = $.parseJSON(response);

            if(response.result == false){
                var msg = "";
                for(var key in response.errors) {
                    msg = msg + key + ": " + response.errors[key] + "\n"
                }
                alert(msg);
            }
            else if (response.result == true) {
                // Очистка формы
                $("#id_UsersForm").closest('form').find("input[type=text], textarea").val("");

                // Добавление записи без перезагрузки
                $('#UsersTable tr:last').after('<tr id="dataTr"><td>'+response.data.name+'</td><td>'+response.data.paycheck+'</td><td>'+response.data.date_joined+'</td></tr>');

            }
        },

        complete:function(){},

        error:function (xhr, textStatus, thrownError){
            alert("Ошибка добавления: " + thrownError);
        }
    });
}


function submitRoomsForm() {
    $.ajax({
        url:"/xhr_postRooms/",
        type: "POST",
        data: $("#id_RoomsForm").serialize(),

        success:function(response){
            response = $.parseJSON(response);

            if(response.result == false){
                var msg = "";
                for(var key in response.errors) {
                    msg = msg + key + ": " + response.errors[key] + "\n"
                }
                alert(msg);
            }
            else if (response.result == true) {
                // Очистка формы
                $("#id_RoomsForm").closest('form').find("input[type=text], textarea").val("");

                // Добавление записи без перезагрузки
                $('#RoomsTable tr:last').after('<tr id="dataTr"><td>'+response.data.department+'</td><td>'+response.data.spots+'</td></tr>');

            }
        },

        complete:function(){},

        error:function (xhr, textStatus, thrownError){
            alert("Ошибка добавления: " + thrownError);
        }
    });
}