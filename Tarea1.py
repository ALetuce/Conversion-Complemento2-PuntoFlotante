import sys
import re
from tabulate import tabulate

# FUNCIONES AUXILIARES
def Decimal_To_Binary(D_num):
    D_num = int(D_num)
    reversed_BinaryForm = ""
    while D_num >= 2:
        reversed_BinaryForm += str(D_num%2)
        D_num //= 2
    if D_num:
        reversed_BinaryForm += str(1)

    BinaryForm = ""
    for i in reversed_BinaryForm:
        BinaryForm = i + BinaryForm

    return BinaryForm

def Binary_to_Decimal(B_num):
    num_digits = list(str(B_num))
    num_digits.reverse()
    pos = 0
    decimal_form = 0 
    for d in num_digits:
        decimal_form += (2**pos)*int(d)
        pos += 1
    return decimal_form

def get_C2(num):
    # encontramos el Complemento 1
    num_C1 = ""
    for d in num:
        if int(d):
            num_C1 += "0"
        else:
            num_C1 += "1"
    # sumamos 1 
    num_C2 = sum_BinaryNumers(num_C1, "00000001")
    return num_C2

def sum_BinaryNumers(num1, num2):
    d_num1 = re.findall('\d', num1)
    d_num2 = re.findall('\d', num2)
    d_num1.reverse()
    d_num2.reverse()
    reversed_sumResult = ""
    carry = 0
    for i in range(0,8):
        n = int(d_num1[i]) + int(d_num2[i])
        if n == 2:
            if carry:
                reversed_sumResult += str(1)
            else:
                carry = 1
                reversed_sumResult += str(0)
        elif n == 1:
            if carry:
                reversed_sumResult+= str(0)
            else:
                reversed_sumResult += str(1)
        elif n == 0:
            if carry:
                carry = 0
                reversed_sumResult += str(1)
            else:
                reversed_sumResult += str(0)
    sum_Result = ""
    for i in reversed_sumResult:
        sum_Result = i + sum_Result

    return sum_Result

# FUNCIONES PRINCIPALES
# conversion numerica bases 1 a 64
def Conversion_BaseN(num, O_base, D_base): # baseO de Origen y baseD de Destino
    O_base = int(O_base)
    D_base = int(D_base)
    # separamos el numero para poder analizarlo
    all_digits = re.findall(".", str(num))
    num_digits = []
    for d in all_digits:
        if re.match("\d", d):
            num_digits.append(int(d))
        elif re.match("[a-z]", d):
            n = ord(d) - 87
            num_digits.append(n)
        elif re.match("[A-Z]", d):
            n = ord(d) - 29
            num_digits.append(n)
        elif re.match("\+", d):
            n = ord("+") + 19
            num_digits.append(n)
        elif re.match("\?", d):
            n = ord("?")
            num_digits.append(n)
    
    # buscamos su equivalente en base 10
    num_digits.reverse()
    pos = 0
    decimal_form = 0 
    for d in num_digits:
        decimal_form += (O_base**pos)*d
        pos += 1

    # convertir de decimal a la base de Destino D_base
    dividend = decimal_form
    new_number = []
    while D_base <= dividend:
        new_number.append(dividend % D_base)
        dividend //= D_base
    new_number.append(dividend)
    
    # acomodamos el numero, giramos la lista y lo retornamos como entero int
    new_number.reverse()
    converted_number = ""
    for digit in new_number:
        if digit < 10:
            converted_number += str(digit)
        elif 9 < digit < 36:
            converted_number += chr(digit + 87)
        elif 35 < digit < 61:
            converted_number += chr(digit + 29)  
        elif digit == 61:
            converted_number += "+"
        elif digit == 62:
            converted_number += "?"
    
    sys.stdout.write("Base "+ str(D_base) + ": "+ converted_number  + "\n")
    return 1

# suma y resta binario complemento 2 
def BinaryOperations_Comp2(num1, num2): # pasar como str
    if re.match("1", num1):
        positive_binaryForm = get_C2(num1)
        positive_decimalForm = Binary_to_Decimal(positive_binaryForm)
        decimal_num1 = positive_decimalForm*-1
    else:
        decimal_num1 = Binary_to_Decimal(num1)
    if re.match("1", num2):
        positive_binaryForm = get_C2(num2)
        positive_decimalForm = Binary_to_Decimal(positive_binaryForm)
        decimal_num2 = positive_decimalForm*-1
    else:
        decimal_num2 = Binary_to_Decimal(num2)
    
    addi_BinaryNum = 0
    subt_BinaryNum = 0
    if decimal_num1 + decimal_num2 > 127:
        addi_BinaryNum = "OVERFLOW"
    if decimal_num1 - decimal_num2 < -128:
        subt_BinaryNum = "OVERFLOW"
    
    if not addi_BinaryNum:
        addi_BinaryNum = sum_BinaryNumers(num1, num2)
    if not subt_BinaryNum:
        num2_C2 = get_C2(num2)
        subt_BinaryNum = sum_BinaryNumers(num1, num2_C2) 

    GraficRepresentation_sumBinary = num1 + " + " + num2 + " = " + addi_BinaryNum
    GraficRepresentation_subsBinary = num1 + " + " + num2_C2 + " = " + subt_BinaryNum

    table = [["Suma", GraficRepresentation_sumBinary],["Resta", GraficRepresentation_subsBinary]]    
    sys.stdout.write(tabulate(table))
    sys.stdout.write("\n")
    return 1

# representacion punto flotante 
def FloatP_Represent(num):
    num = float(num)
    if num < 0:
        sign_bit = 1
    else:
        sign_bit = 0
    
    if sign_bit:
        num = str(num)[1:]
        num = float(num)

    int_Part = num
    decimal_Part = 0
    if re.search('\.', str(num)):
        split_num = str(num).split(".")
        int_Part = int(split_num[0])
        decimal_Part = split_num[1]
        e = len(decimal_Part)
        decimal_Part = int(decimal_Part) / 10**e

    # en caso de estaer entre -1 y 1 , osea de la forma 0. algo
    if re.match("0", str(int_Part)):
        # encontrar una expresion binaria para la parte decimal 
        mantissa = ""
        for i in range(36): # 2 max size of the mantissa, para estar seguros 
            decimal_Part *= 2
            if decimal_Part > 10:
                mantissa += "1"
                decimal_Part -= 10
            else:
                mantissa += "0"
        
        # normalizamos (prefijo N) la mantisa
        exp = -1
        for i in range(46): 
            if re.match("1", mantissa[i]):
                N_mantissa = mantissa[i+1:]
                break
            exp -= 1

        # buscamos la expresion para el exponente 8 bits con bias
        exp += 127
        exp_withBias = Decimal_To_Binary(exp)

        # mantisa total 23 bits
        mantissa_23bits = ""
        for noUse_variable in range(23):
            mantissa_23bits += N_mantissa[0]
            N_mantissa = N_mantissa[1:]

    else:
        int_mantissa = Decimal_To_Binary(int_Part)

        # normalizamos (prefijo N) la parte entera de la mantisa
        exp = 1
        original_len = len(int_mantissa)
        for i in range(23): # size of the mantissa
            if re.match("1", int_mantissa[i]):
                int_mantissa = int_mantissa[i+1:]
                break
            exp += 1
        exp = original_len - exp
        # buscamos la expresion para el exponente 8bits con bias
        exp += 127
        if exp < 0 or 254 < exp:
            sys.stdout.write("01111111100000000000000000000000")
            return 1
        exp_withBias = Decimal_To_Binary(exp)
        missing_part = 8 - len(exp_withBias)
        for i in range(missing_part):
            exp_withBias = "0" + exp_withBias 

        # para la parte decimal
        decimal_mantissa = ""
        for i in range(23): 
            decimal_Part *= 2
            if decimal_Part >= 1:
                decimal_mantissa += "1"
                decimal_Part -= 1
            else:
                decimal_mantissa += "0"
        
        # mantisa total 23 bits
        mantissa_23bits = ""
        for noUse_variable in range(23):
            if int_mantissa != "":
                mantissa_23bits += int_mantissa[0]
                int_mantissa = int_mantissa[1:]
            else:
                mantissa_23bits += decimal_mantissa[0]
                decimal_mantissa = decimal_mantissa[1:]

    # generacion formato IEEE754
    IEEE754_format = ""
    IEEE754_format += str(sign_bit)
    IEEE754_format += exp_withBias
    IEEE754_format += mantissa_23bits
    sys.stdout.write(IEEE754_format + "\n")
    return 1

M = 4
flag = True
while flag:
    M = sys.stdin.readline()

    if re.search("1", M):
        info = sys.stdin.readline()
        info.strip()
        info_list = re.findall("[a-zA-Z0-9+?]+", info)
        num = info_list[0]
        O = info_list[1]
        D = info_list[2]
        Conversion_BaseN(num, O, D)
        
    if re.search("2", M):
        sys.stdout.write("Halo")
        info = sys.stdin.readline()
        info.strip()
        info_list = re.findall("[01]+", info)
        num1 = info_list[0]
        num2 = info_list[1]
        BinaryOperations_Comp2(num1, num2)

    if re.search("3", M):
        info = sys.stdin.readline()
        data = re.search("[\d\.-]+", info).group()
        FloatP_Represent(data)

    if re.search("0", M):
        flag = False

sys.stdout.write("gracias por usar nuestro servicio")


        


