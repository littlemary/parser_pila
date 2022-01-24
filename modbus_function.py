from pyModbusTCP.client import ModbusClient
c = ModbusClient(host='10.0.6.10', port=502, unit_id=1, auto_open=True)


def modbus_start_connection():
    if not c.is_open():
        if not c.open():
            return 0
        if c.is_open():
            return 1
    return 1
def check_value(c, num, step):
    # step 3 проверяем значение ready_take_sheet. должно быть 1
    res = c.read_coils(num)
    # заглушка. Записали в ПЛК нужную переменную.
    #return_flag = c.write_single_coil(num, True)
    # / заглушка. Записали в ПЛК нужную переменную.
    kol = 0
    while res == False:
        kol += 1
        res = c.read_coils(num)
        #if kol > 30:
            #str_res='Проблема со связью. Шаг '+step
            #return str_res
    return 1
def modbus_write_array(result_arr):
#step 1 записываем в 0 регистр все 0
    starting_address = 0x00
    output_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    return_flag = c.write_multiple_coils(starting_address, output_values)
    if not return_flag:
        return 'Проблема со связью. Шаг 1'
    #clear_array ставим в True
    return_flag = c.write_single_coil(22, True)
#step 2 command_write_sheet записываем  1
    return_flag = c.write_single_coil(0, True)
    if not return_flag:
        return 'Проблема со связью. Шаг 2'

# step 3 проверяем значение ready_take_sheet. должно быть 1
    res=check_value(c, 16, 3)
    if isinstance(res, str):
        return res
#step 4 записываем в number_records количество записей
    output_address = 12
    output_value=len(result_arr)
    c.write_single_register(output_address, output_value)

#step 5 com_write_num_records записываем 1
    c.write_single_coil(2, True)

# step 6 проверяем значение end_write_num_records. должно быть 1
    res = check_value(c, 20, 6)
    if isinstance(res, str):
        return res
#step 7 end_write_num_records записали 0
    c.write_single_coil(20, False)

# step 8 проверяем значение ready_take_records. должно быть 1
    res = check_value(c, 17, 8)
    if isinstance(res, str):
        return res
#шаг 9 end_take_records=0
    for cur in result_arr:
        c.write_single_coil(18, False)
#шаг 10 запись данных из массива
        #bar_length
        output_address = 2
        output_value = int(cur[0])
        c.write_single_register(output_address, output_value)
        #angles
        output_value=0
        l_a=int(cur[1])
        r_a=int(cur[2])
        if (l_a==45 and r_a==45):
            output_value = 0
        if (l_a==45 and r_a==90):
            output_value = 1
        if (l_a==90 and r_a==45):
            output_value = 2
        if (l_a==90 and r_a==90):
            output_value = 3

        c.write_single_register(3, output_value)


        #height_profile
        output_address = 4
        if cur[3]=='':
            output_value=100
        else:
            output_value = int(cur[3])
        c.write_single_register(output_address, output_value)
        #bar_number
        output_address = 5
        output_value = int(cur[10])
        output_value=1
        c.write_single_register(output_address, output_value)
        # bar_code
        output_address = 6
        #output_value = int(cur[9])
        output_value = 0
        c.write_single_register(output_address, output_value)
        # article_profile
        output_address = 8
        #output_value = int(cur[7])
        output_value = 0
        c.write_single_register(output_address, output_value)
        # qty_bar
        output_address = 10
        output_value = int(cur[8])
        c.write_single_register(output_address, output_value)
        # real_size
        output_address = 11
        output_value = int(cur[6])
        c.write_single_register(output_address, output_value)

#шаг 11 com_write_next_records=1
        c.write_single_coil(1, True)
#шаг 12 проверяем end_take_records==1
        res = check_value(c, 18, 12)
        if isinstance(res, str):
            return res
# шаг 13 проверяем ready_take_sheet==1
        res = check_value(c, 16, 13)
        if isinstance(res, str):
           return res
        c.write_single_coil(16, True)
# шаг 14 вышли из цикла проверяем end_write_full==True
                        #записываем end_write_full=False
                        #записываем commands_write_sheet=False
    res = check_value(c, 21, 14)
    if isinstance(res, str):
       return res
    c.write_single_coil(21, True)
    c.write_single_coil(0, True)

#шаг 15 все сбросить  в 0
    starting_address = 0x00
    output_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    return_flag = c.write_multiple_coils(starting_address, output_values)
    if not return_flag:
        return 'Проблема со связью. Шаг 15'

    return 1