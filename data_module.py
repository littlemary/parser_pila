def convert_base(num, to_base=10, from_base=10):
    # first convert to decimal number
    n = int(num, from_base) if isinstance(num, str) else num
    # now convert decimal to 'to_base' base
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = ""
    while n > 0:
        n,m = divmod(n, to_base)
        res += alphabet[m]
    return res[::-1]


def makearray(textstr, hex_arr):
    result=['', '', '', '', '', '', '', '', '']
    if (len(textstr)<108):
        return 0
    #bar_length
    mystr = hex_arr[5] + hex_arr[6]
    mystrdecode = convert_base(mystr, 10, 16)
    #mystrdecode = mystrdecode[:-1]
    result[0] = mystrdecode

    #angle_left_grad
    mystr = hex_arr[8] + hex_arr[9]
    mystrdecode = convert_base(mystr, 10, 16)
    result[1] = mystrdecode

    #angle_right_grad
    mystr = hex_arr[10] + hex_arr[11]
    mystrdecode = convert_base(mystr, 10, 16)
    mystrdecode = mystrdecode[:-1]
    result[2] = mystrdecode

    #height_profile
    mystr = hex_arr[12] + hex_arr[13]
    mystrdecode = convert_base(mystr, 10, 16)
    mystrdecode = mystrdecode[:-1]
    result[3] = mystrdecode

    # qty_bar
    mystr=hex_arr[15]
    mystrdecode = convert_base(mystr, 10, 18)
    result[4] = mystrdecode

    # bar_color
    mystrdecode = textstr[52:68]
    data = bytes(mystrdecode, "utf-8")
    data1 = bytes.fromhex(data.decode("ascii"))
    result[5] = data1.decode('utf-8')

    # bar_code
    mystrdecode = textstr[68:80]
    data = bytes(mystrdecode, "utf-8")
    data1 = bytes.fromhex(data.decode("ascii"))

    result[6] = data1.decode('utf-8')

    # bar_number
    mystrdecode = textstr[82:84]
    data = bytes(mystrdecode, "utf-8")
    data1 = bytes.fromhex(data.decode("ascii"))
    result[7] = data1.decode('utf-8')

    mystrdecode = textstr[84:96]
    data = bytes(mystrdecode, "utf-8")
    data1 = bytes.fromhex(data.decode("ascii"))
    result[8] = data1.decode('utf-8')
    return result

def parse_array(hex_arr):
    parserresult = []
    result_arr = []
    for cur in range(0, len(hex_arr), 54):
        start=cur
        end=cur+54
        if end>len(hex_arr):
            end=len(hex_arr)
        str_text = ''.join(hex_arr[start:end])
        res = makearray(str_text, hex_arr[start:end])
        if res != 0:
            parserresult.append(res)
    qty_bar=0
    for curw in parserresult:
        qty_bar+=1
        height_pr = curw[1]
        angleleft = curw[2]
        angleright=curw[3]
        addleft = '0'
        addright = '0'
        if angleright == "45":
            addright = height_pr
        if angleright == "90":
            addright = '0'
        if angleleft == "45":
            addleft = height_pr
        if angleleft == "90":
            addleft = '0'

        if addleft=='0' or addright=='0':
            realsize='0'
        else:
            realsize=str(int(curw[0]) - int(addleft) - int(addright))
        result_row=[]
        result_row.clear()
        result_row.append(curw[0])#bar_length
        result_row.append(curw[2])#angle_left_grad
        result_row.append(curw[3])#angle_right_grad
        result_row.append(height_pr)#height_profile
        result_row.append(addleft)#addleft
        result_row.append(addright)#addright
        result_row.append(realsize)#realsize
        result_row.append(curw[8])#article_profile
        result_row.append(str(qty_bar))#qty_bar
        result_row.append(curw[6])#bar_code
        result_row.append(curw[7])#bar_number
        result_row.append(curw[5])#bar_color
        result_row.append('')
        result_arr.append(result_row)
    return result_arr