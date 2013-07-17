function attacheEditable(modelName) {
    function saveValue(value, editField) {
        var editData = {}
        editData['value'] = value;
        editData['pk'] = editField.parent().find('td.pk').html();
        editData['modelName'] = modelName;
        editData['fieldName'] = editField.attr("field_name");
        editData['csrfmiddlewaretoken'] = $.cookie("csrftoken");

        // Пытаемся сохранить отредактированное
        $.ajax({
            type: "POST",
            url: "/xhr_editField/",
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
    $('.AnotherField').editable(
        function(value, settings) {
            saveValue(value, $(this));
            return(value);
        }
    );

    // Календарь
    $('.DateField').editable(
        function(value, settings){
            saveValue(value, $(this));
            return(value);
        },
        {type: 'datepicker', datepicker: {dateFormat: 'yy-mm-dd'}}
    );
}


function generateRow(item) {
    var row = '<tr id="dataTr">';

    for(var j=0; j<item.length; j++) {
        // Чтобы к полю ID не прицеплялся editable
        if (item[j]['fieldName'] == 'id')
            var fieldType = 'pk'
        else
            var fieldType = item[j]['fieldType']

        row = row + '<td class="'+fieldType+'" field_name="'+item[j]['fieldName']+'">'+item[j]['value']+'</td>';
    }

    row = row + "</tr>";

    return row;
}


function loadTable(modelName) {
    // Очистка таблицы
    $('*#dataTr').remove();

    // Прячем все таблицы
    $('.data_table').hide();
    $('.data_form').hide();

    // Показываем нужную таблицу
    $('#id_table_'+modelName).show();
    $('#id_form_'+modelName).show();

    $.ajax({
        type: "GET",
        url: "/xhr_getModel/",
        data: {"modelName": modelName},

        success: function(response){
            response = $.parseJSON(response);
            //response = $.parseJSON(response);

            // Генерация строки таблицы
            for(var i=0; i<response.length; i++) {
                var row = generateRow(response[i]);

                $('#id_table_'+modelName+' tr:last').after(row);
            }

            attacheEditable(modelName);
        }
    });
}


function addLastRow(modelName) {
    $.ajax({
        type: "GET",
        url: "/xhr_getLastRow/",
        data: {"modelName": modelName},

        success: function(response){
            response = $.parseJSON(response);
            var row = generateRow(response);

            $('#id_table_'+modelName+' tr:last').after(row);

            attacheEditable(modelName);
        }
    });
}


function submitForm(modelName) {
    // Формируем пост-запрос и добавляем в него имя модели
    var data = $("#id_form_" + modelName).serialize();
    data = data + "&__modelName__=" + modelName;
    //var dataArray = $("#id_form_" + modelName).serializeArray();

    $.ajax({
        url:"/xhr_postRow/",
        type: "POST",
        data: data,

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
                $("#id_form_" + modelName).closest('form').find("input[type=text], textarea").val("");

                // Обновляем таблицу
                addLastRow(modelName);
            }
        },

        complete:function(){},

        error:function (xhr, textStatus, thrownError){
            alert("Ошибка добавления: " + thrownError);
        }
    });
}
