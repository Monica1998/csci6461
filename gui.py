import time
from tkinter import *
from CPU import *
from converter import *

# Initialize Tkinter
gui = Tk()
gui.title("Assemble Simulator")

cpu = CPU(2048)

# Initialize and Place Frames
frameswitches = LabelFrame(gui, borderwidth=0, highlightthickness=0)
frameswitches.grid(row=9, column=0, columnspan=5, padx=50, pady=10)
frameregister = LabelFrame(gui, borderwidth=0, highlightthickness=0)
frameregister.grid(row=0, column=0)
frameoperation = LabelFrame(gui, borderwidth=0, highlightthickness=0)
frameoperation.grid(row=8, column=6, columnspan=1, padx=50, pady=10)
framerun = LabelFrame(gui, borderwidth=0, highlightthickness=0)
framerun.grid(row=9, column=6, columnspan=1, padx=50, pady=10)

# Initialize and Place Register Labels
GPR0Label = Label(gui, text="GRP 0(16bits)").grid(row=0, column=0)
GPR1Label = Label(gui, text="GRP 1(16bits)").grid(row=1, column=0)
GPR2Label = Label(gui, text="GRP 2(16bits)").grid(row=2, column=0)
GPR3Label = Label(gui, text="GRP 3(16bits)").grid(row=3, column=0)

SpaceLabelGPR = Label(gui, text=" ").grid(row=4, column=0)

IXR1Label = Label(gui, text="IXR1(16bits)").grid(row=5, column=0)
IXR2Label = Label(gui, text="IXR2(16bits)").grid(row=6, column=0)
IXR3Label = Label(gui, text="IXR3(16bits)").grid(row=7, column=0)

SpaceLabelIXR = Label(gui, text=" ").grid(row=8, column=0)

PCLabel = Label(gui, text="PC(12bits)").grid(row=0, column=5)
MARLabel = Label(gui, text="MAR(12bits)").grid(row=1, column=5)
MBRLabel = Label(gui, text="MBR(16bits)").grid(row=2, column=5)
IRLabel = Label(gui, text="IR(16bits)").grid(row=3, column=5)
MFRLabel = Label(gui, text="MFR(4bits)").grid(row=4, column=5)
PrivilegedLabel = Label(gui, text="Privileged(1bits)").grid(row=5, column=5)

# Initialize Switch Values to 0
num15: int = 0
num14: int = 0
num13: int = 0
num12: int = 0
num11: int = 0
num10: int = 0
num9: int = 0
num8: int = 0
num7: int = 0
num6: int = 0
num5: int = 0
num4: int = 0
num3: int = 0
num2: int = 0
num1: int = 0
num0: int = 0

# Initalize Switch Labels
Status15 = Label(frameswitches, text="" + str(num15))
Status14 = Label(frameswitches, text="" + str(num14))
Status13 = Label(frameswitches, text="" + str(num13))
Status12 = Label(frameswitches, text="" + str(num12))
Status11 = Label(frameswitches, text="" + str(num11))
Status10 = Label(frameswitches, text="" + str(num10))
Status9 = Label(frameswitches, text="" + str(num9))
Status8 = Label(frameswitches, text="" + str(num8))
Status7 = Label(frameswitches, text="" + str(num7))
Status6 = Label(frameswitches, text="" + str(num6))
Status5 = Label(frameswitches, text="" + str(num5))
Status4 = Label(frameswitches, text="" + str(num4))
Status3 = Label(frameswitches, text="" + str(num3))
Status2 = Label(frameswitches, text="" + str(num2))
Status1 = Label(frameswitches, text="" + str(num1))
Status0 = Label(frameswitches, text="" + str(num0))


# Switch Toggle Functions for 16 switches, the values toggle between 0 and 1
def Click15():
    global Status15
    global num15
    global Btn15
    if num15 != 1:
        num15 = 1
        Btn15.grid_forget()
        Btn15 = Button(frameswitches, text="15", padx=5, pady=15, command=Click15)
        Btn15.grid(row=14, column=0)
    else:
        num15 = 0
        Btn15.grid_forget()
        Btn15 = Button(frameswitches, text="15", padx=5, pady=15, command=Click15)
        Btn15.grid(row=14, column=0)
    Status15 = Label(frameswitches, text="" + str(num15))
    Status15.grid(row=15, column=0)
    print(num15)
    return


def Click14():
    global Status14
    global num14
    global Btn14
    if num14 != 1:
        num14 = 1
        Btn14.grid_forget()
        Btn14 = Button(frameswitches, text="14", padx=5, pady=16, command=Click14)
        Btn14.grid(row=14, column=1)
    else:
        num14 = 0
        Btn14.grid_forget()
        Btn14 = Button(frameswitches, text="14", padx=5, pady=16, command=Click14)
        Btn14.grid(row=14, column=1)
    Status14 = Label(frameswitches, text="" + str(num14))
    Status14.grid(row=15, column=1)
    print(num14)
    return


def Click13():
    global Status13
    global num13
    global Btn13
    if num13 != 1:
        num13 = 1
        Btn13.grid_forget()
        Btn13 = Button(frameswitches, text="13", padx=5, pady=16, command=Click13)
        Btn13.grid(row=14, column=2)
    else:
        num13 = 0
        Btn13.grid_forget()
        Btn13 = Button(frameswitches, text="13", padx=5, pady=16, command=Click13)
        Btn13.grid(row=14, column=2)
    Status13 = Label(frameswitches, text="" + str(num13))
    Status13.grid(row=15, column=2)
    print(num13)
    return


def Click12():
    global Status12
    global num12
    global Btn12
    if num12 != 1:
        num12 = 1
        Btn12.grid_forget()
        Btn12 = Button(frameswitches, text="12", padx=5, pady=16, command=Click12)
        Btn12.grid(row=14, column=3)
    else:
        num12 = 0
        Btn12.grid_forget()
        Btn12 = Button(frameswitches, text="12", padx=5, pady=16, command=Click12)
        Btn12.grid(row=14, column=3)
    Status12 = Label(frameswitches, text="" + str(num12))
    Status12.grid(row=15, column=3)
    print(num12)
    return


def Click11():
    global Status11
    global num11
    global Btn11
    if num11 != 1:
        num11 = 1
        Btn11.grid_forget()
        Btn11 = Button(frameswitches, text="11", padx=5, pady=16, command=Click11)
        Btn11.grid(row=14, column=4)
    else:
        num11 = 0
        Btn11.grid_forget()
        Btn11 = Button(frameswitches, text="11", padx=5, pady=16, command=Click11)
        Btn11.grid(row=14, column=4)
    Status11 = Label(frameswitches, text="" + str(num11))
    Status11.grid(row=15, column=4)
    print(num11)
    return


def Click10():
    global Status10
    global num10
    global Btn10
    if num10 != 1:
        num10 = 1
        Btn10.grid_forget()
        Btn10 = Button(frameswitches, text="10", padx=5, pady=16, command=Click10)
        Btn10.grid(row=14, column=5)
    else:
        num10 = 0
        Btn10.grid_forget()
        Btn10 = Button(frameswitches, text="10", padx=5, pady=16, command=Click10)
        Btn10.grid(row=14, column=5)
    Status10 = Label(frameswitches, text="" + str(num10))
    Status10.grid(row=15, column=5)
    print(num10)
    return


def Click9():
    global Status9
    global num9
    global Btn9
    if num9 != 1:
        num9 = 1
        Btn9.grid_forget()
        Btn9 = Button(frameswitches, text="9", padx=5, pady=16, command=Click9)
        Btn9.grid(row=14, column=6)
    else:
        num9 = 0
        Btn9.grid_forget()
        Btn9 = Button(frameswitches, text="9", padx=5, pady=16, command=Click9)
        Btn9.grid(row=14, column=6)
    Status9 = Label(frameswitches, text="" + str(num9))
    Status9.grid(row=15, column=6)
    print(num9)
    return


def Click8():
    global Status8
    global num8
    global Btn8
    if num8 != 1:
        num8 = 1
        Btn8.grid_forget()
        Btn8 = Button(frameswitches, text="8", padx=5, pady=16, command=Click8)
        Btn8.grid(row=14, column=7)
    else:
        num8 = 0
        Btn8.grid_forget()
        Btn8 = Button(frameswitches, text="8", padx=5, pady=16, command=Click8)
        Btn8.grid(row=14, column=7)
    Status8 = Label(frameswitches, text="" + str(num8))
    Status8.grid(row=15, column=7)
    print(num8)
    return


def Click7():
    global Status7
    global num7
    global Btn7
    if num7 != 1:
        num7 = 1
        Btn7.grid_forget()
        Btn7 = Button(frameswitches, text="7", padx=5, pady=16, command=Click7)
        Btn7.grid(row=14, column=8)
    else:
        num7 = 0
        Btn7.grid_forget()
        Btn7 = Button(frameswitches, text="7", padx=5, pady=16, command=Click7)
        Btn7.grid(row=14, column=8)
    Status7 = Label(frameswitches, text="" + str(num7))
    Status7.grid(row=15, column=8)
    print(num7)
    return


def Click6():
    global Status6
    global num6
    global Btn6
    if num6 != 1:
        num6 = 1
        Btn6.grid_forget()
        Btn6 = Button(frameswitches, text="6", padx=5, pady=16, command=Click6)
        Btn6.grid(row=14, column=9)
    else:
        num6 = 0
        Btn6.grid_forget()
        Btn6 = Button(frameswitches, text="6", padx=5, pady=16, command=Click6)
        Btn6.grid(row=14, column=9)
    Status6 = Label(frameswitches, text="" + str(num6))
    Status6.grid(row=15, column=9)
    print(num6)
    return


def Click5():
    global Status5
    global num5
    global Btn5
    if num5 != 1:
        num5 = 1
        Btn5.grid_forget()
        Btn5 = Button(frameswitches, text="5", padx=5, pady=16, command=Click5)
        Btn5.grid(row=14, column=10)
    else:
        num5 = 0
        Btn5.grid_forget()
        Btn5 = Button(frameswitches, text="5", padx=5, pady=16, command=Click5)
        Btn5.grid(row=14, column=10)
    Status5 = Label(frameswitches, text="" + str(num5))
    Status5.grid(row=15, column=10)
    print(num5)
    return


def Click4():
    global Status4
    global num4
    global Btn4
    if num4 != 1:
        num4 = 1
        Btn4.grid_forget()
        Btn4 = Button(frameswitches, text="4", padx=5, pady=16, command=Click4)
        Btn4.grid(row=14, column=11)
    else:
        num4 = 0
        Btn4.grid_forget()
        Btn4 = Button(frameswitches, text="4", padx=5, pady=16, command=Click4)
        Btn4.grid(row=14, column=11)
    Status4 = Label(frameswitches, text="" + str(num4))
    Status4.grid(row=15, column=11)
    print(num4)
    return


def Click3():
    global Status3
    global num3
    global Btn3
    if num3 != 1:
        num3 = 1
        Btn3.grid_forget()
        Btn3 = Button(frameswitches, text="3", padx=5, pady=16, command=Click3)
        Btn3.grid(row=14, column=12)
    else:
        num3 = 0
        Btn3.grid_forget()
        Btn3 = Button(frameswitches, text="3", padx=5, pady=16, command=Click3)
        Btn3.grid(row=14, column=12)
    Status3 = Label(frameswitches, text="" + str(num3))
    Status3.grid(row=15, column=12)
    print(num3)
    return


def Click2():
    global Status2
    global num2
    global Btn2
    if num2 != 1:
        num2 = 1
        Btn2.grid_forget()
        Btn2 = Button(frameswitches, text="2", padx=5, pady=16, command=Click2)
        Btn2.grid(row=14, column=13)
    else:
        num2 = 0
        Btn2.grid_forget()
        Btn2 = Button(frameswitches, text="2", padx=5, pady=16, command=Click2)
        Btn2.grid(row=14, column=13)
    Status2 = Label(frameswitches, text="" + str(num2))
    Status2.grid(row=15, column=13)
    print(num2)
    return


def Click1():
    global Status1
    global num1
    global Btn1
    if num1 != 1:
        num1 = 1
        Btn1.grid_forget()
        Btn1 = Button(frameswitches, text="1", padx=5, pady=16, command=Click1)
        Btn1.grid(row=14, column=14)
    else:
        num1 = 0
        Btn1.grid_forget()
        Btn1 = Button(frameswitches, text="1", padx=5, pady=16, command=Click1)
        Btn1.grid(row=14, column=14)
    Status1 = Label(frameswitches, text="" + str(num1))
    Status1.grid(row=15, column=14)
    print(num1)
    return


def Click0():
    global Status0
    global num0
    global Btn0
    if num0 != 1:
        num0 = 1
        Btn0.grid_forget()
        Btn0 = Button(frameswitches, text="0", padx=5, pady=16, command=Click0)
        Btn0.grid(row=14, column=15)
    else:
        num0 = 0
        Btn0.grid_forget()
        Btn0 = Button(frameswitches, text="0", padx=5, pady=16, command=Click0)
        Btn0.grid(row=14, column=15)
    Status0 = Label(frameswitches, text="" + str(num0))
    Status0.grid(row=15, column=15)
    print(num0)
    return


# Individual switch buttons and function
Btn15 = Button(frameswitches, text="15", padx=5, pady=15, command=Click15)
Btn14 = Button(frameswitches, text="14", padx=5, pady=15, command=Click14)
Btn13 = Button(frameswitches, text="13", padx=5, pady=15, command=Click13)
Btn12 = Button(frameswitches, text="12", padx=5, pady=15, command=Click12)
Btn11 = Button(frameswitches, text="11", padx=5, pady=15, command=Click11)
Btn10 = Button(frameswitches, text="10", padx=5, pady=15, command=Click10)
Btn9 = Button(frameswitches, text="9", padx=5, pady=15, command=Click9)
Btn8 = Button(frameswitches, text="8", padx=5, pady=15, command=Click8)
Btn7 = Button(frameswitches, text="7", padx=5, pady=15, command=Click7)
Btn6 = Button(frameswitches, text="6", padx=5, pady=15, command=Click6)
Btn5 = Button(frameswitches, text="5", padx=5, pady=15, command=Click5)
Btn4 = Button(frameswitches, text="4", padx=5, pady=15, command=Click4)
Btn3 = Button(frameswitches, text="3", padx=5, pady=15, command=Click3)
Btn2 = Button(frameswitches, text="2", padx=5, pady=15, command=Click2)
Btn1 = Button(frameswitches, text="1", padx=5, pady=15, command=Click1)
Btn0 = Button(frameswitches, text="0", padx=5, pady=15, command=Click0)

# Place Switch Button in grid
Btn15.grid(row=14, column=0)
Btn14.grid(row=14, column=1)
Btn13.grid(row=14, column=2)
Btn12.grid(row=14, column=3)
Btn11.grid(row=14, column=4)
Btn10.grid(row=14, column=5)
Btn9.grid(row=14, column=6)
Btn8.grid(row=14, column=7)
Btn7.grid(row=14, column=8)
Btn6.grid(row=14, column=9)
Btn5.grid(row=14, column=10)
Btn4.grid(row=14, column=11)
Btn3.grid(row=14, column=12)
Btn2.grid(row=14, column=13)
Btn1.grid(row=14, column=14)
Btn0.grid(row=14, column=15)

# Place Switch Status in grid
Status15.grid(row=15, column=0)
Status14.grid(row=15, column=1)
Status13.grid(row=15, column=2)
Status12.grid(row=15, column=3)
Status11.grid(row=15, column=4)
Status10.grid(row=15, column=5)
Status9.grid(row=15, column=6)
Status8.grid(row=15, column=7)
Status7.grid(row=15, column=8)
Status6.grid(row=15, column=9)
Status5.grid(row=15, column=10)
Status4.grid(row=15, column=11)
Status3.grid(row=15, column=12)
Status2.grid(row=15, column=13)
Status1.grid(row=15, column=14)
Status0.grid(row=15, column=15)

# Initialize Register textboxes
GPR0 = Entry(gui, width=30, borderwidth=5)
GPR1 = Entry(gui, width=30, borderwidth=5)
GPR2 = Entry(gui, width=30, borderwidth=5)
GPR3 = Entry(gui, width=30, borderwidth=5)

IXR1 = Entry(gui, width=30, borderwidth=5)
IXR2 = Entry(gui, width=30, borderwidth=5)
IXR3 = Entry(gui, width=30, borderwidth=5)

PC = Entry(gui, width=30, borderwidth=5)
MAR = Entry(gui, width=30, borderwidth=5)
MBR = Entry(gui, width=30, borderwidth=5)
IR = Entry(gui, width=30, borderwidth=5)
MFR = Entry(gui, width=30, borderwidth=5)
Privileged = Entry(gui, width=30, borderwidth=5)

# Initialize register values
GPR0.insert(0, "0000000000000000")
GPR1.insert(0, "0000000000000000")
GPR2.insert(0, "0000000000000000")
GPR3.insert(0, "0000000000000000")
IXR1.insert(0, "0000000000000000")
IXR2.insert(0, "0000000000000000")
IXR3.insert(0, "0000000000000000")
PC.insert(0, "000000000000")
MAR.insert(0, "000000000000")
MBR.insert(0, "0000000000000000")
IR.insert(0, "0000000000000000")
MFR.insert(0, "0000")
Privileged.insert(0, "0")

# Placing Register textboxes
GPR0.grid(row=0, column=1)
GPR1.grid(row=1, column=1)
GPR2.grid(row=2, column=1)
GPR3.grid(row=3, column=1)

IXR1.grid(row=5, column=1)
IXR2.grid(row=6, column=1)
IXR3.grid(row=7, column=1)

PC.grid(row=0, column=6)
MAR.grid(row=1, column=6)
MBR.grid(row=2, column=6)
IR.grid(row=3, column=6)
MFR.grid(row=4, column=6)
Privileged.grid(row=5, column=6)


# LD function for each register
def LD_GPR0():
    GPR0.delete(0, END)
    GPR0.insert(0, str(num15) + str(num14) + str(num13) + str(num12) + str(num11) + str(num10) + str(num9) + str(
        num8) + str(num7) + str(num6) + str(num5) + str(num4) + str(num3) + str(num2) + str(num1) + str(num0))
    GPR0_num = binary_string_to_decimal(GPR0.get())
    cpu.GRs[0].set_val(GPR0_num)
    print(GPR0.get())  # Setting the Register in memory
    return  # Print the register value


def LD_GPR1():
    GPR1.delete(0, END)
    GPR1.insert(0, str(num15) + str(num14) + str(num13) + str(num12) + str(num11) + str(num10) + str(num9) + str(
        num8) + str(num7) + str(num6) + str(num5) + str(num4) + str(num3) + str(num2) + str(num1) + str(num0))
    GPR1_num = binary_string_to_decimal(GPR1.get())
    cpu.GRs[1].set_val(GPR1_num)
    print(GPR1.get())
    return


def LD_GPR2():
    GPR2.delete(0, END)
    GPR2.insert(0, str(num15) + str(num14) + str(num13) + str(num12) + str(num11) + str(num10) + str(num9) + str(
        num8) + str(num7) + str(num6) + str(num5) + str(num4) + str(num3) + str(num2) + str(num1) + str(num0))
    GPR2_num = binary_string_to_decimal(GPR2.get())
    cpu.GRs[2].set_val(GPR2_num)
    print(GPR2.get())
    return


def LD_GPR3():
    GPR3.delete(0, END)
    GPR3.insert(0, str(num15) + str(num14) + str(num13) + str(num12) + str(num11) + str(num10) + str(num9) + str(
        num8) + str(num7) + str(num6) + str(num5) + str(num4) + str(num3) + str(num2) + str(num1) + str(num0))
    GPR3_num = binary_string_to_decimal(GPR3.get())
    cpu.GRs[3].set_val(GPR3_num)
    print(GPR3.get())
    return


def LD_IXR1():
    IXR1.delete(0, END)
    IXR1.insert(0, str(num15) + str(num14) + str(num13) + str(num12) + str(num11) + str(num10) + str(num9) + str(
        num8) + str(num7) + str(num6) + str(num5) + str(num4) + str(num3) + str(num2) + str(num1) + str(num0))
    IXR1_num = binary_string_to_decimal(IXR1.get())
    cpu.IndexRegisters[1].set_val(IXR1_num)
    print(IXR1.get())
    return


def LD_IXR2():
    IXR2.delete(0, END)
    IXR2.insert(0, str(num15) + str(num14) + str(num13) + str(num12) + str(num11) + str(num10) + str(num9) + str(
        num8) + str(num7) + str(num6) + str(num5) + str(num4) + str(num3) + str(num2) + str(num1) + str(num0))
    IXR2_num = binary_string_to_decimal(IXR2.get())
    cpu.IndexRegisters[2].set_val(IXR2_num)
    print(IXR2.get())
    return


def LD_IXR3():
    IXR3.delete(0, END)
    IXR3.insert(0, str(num15) + str(num14) + str(num13) + str(num12) + str(num11) + str(num10) + str(num9) + str(
        num8) + str(num7) + str(num6) + str(num5) + str(num4) + str(num3) + str(num2) + str(num1) + str(num0))
    IXR3_num = binary_string_to_decimal(IXR3.get())
    cpu.IndexRegisters[3].set_val(IXR3_num)
    print(IXR3.get())
    return


def LD_PC():
    PC.delete(0, END)
    PC.insert(0,
              str(num15) + str(num14) + str(num13) + str(num12) + str(num11) + str(num10) + str(num9) + str(num8) + str(
                  num7) + str(num6) + str(num5) + str(num4) + str(num3) + str(num2) + str(num1) + str(num0))
    cpu.PC.set_addr(binary_string_to_decimal(PC.get()))
    return


def LD_MAR():
    MAR.delete(0, END)
    MAR.insert(0, str(num15) + str(num14) + str(num13) + str(num12) + str(num11) + str(num10) + str(num9) + str(
        num8) + str(num7) + str(num6) + str(num5) + str(num4) + str(num3) + str(num2) + str(num1) + str(num0))
    cpu.MAR.set_val(binary_string_to_decimal(MAR.get()))
    return


def LD_MBR():
    MBR.delete(0, END)
    MBR.insert(0, str(num15) + str(num14) + str(num13) + str(num12) + str(num11) + str(num10) + str(num9) + str(
        num8) + str(num7) + str(num6) + str(num5) + str(num4) + str(num3) + str(num2) + str(num1) + str(num0))
    cpu.MBR.set_val(binary_string_to_decimal(MBR.get()))
    return


def show_general_register(general_register):
    match general_register:
        case 0:
            GPR0.delete(0, END)
            GPR0.insert(0, str(decimal_to_binary(cpu.GRs[0].get_val())))
        case 1:
            GPR1.delete(0, END)
            GPR1.insert(0, str(decimal_to_binary(cpu.GRs[1].get_val())))
        case 2:
            GPR2.delete(0, END)
            GPR2.insert(0, str(decimal_to_binary(cpu.GRs[2].get_val())))
        case 3:
            GPR3.delete(0, END)
            GPR3.insert(0, str(decimal_to_binary(cpu.GRs[3].get_val())))


def show_index_register(index_register):
    match index_register:
        case 0:
            pass
        case 1:
            IXR1.delete(0, END)
            IXR1.insert(0, str(decimal_to_binary(cpu.IndexRegisters[0].get_val())))
        case 2:
            IXR2.delete(0, END)
            IXR2.insert(0, str(decimal_to_binary(cpu.IndexRegisters[1].get_val())))
        case 3:
            IXR3.delete(0, END)
            IXR3.insert(0, str(decimal_to_binary(cpu.IndexRegisters[2].get_val())))


def reset():
    GPR0.delete(0, END)
    GPR1.delete(0, END)
    GPR2.delete(0, END)
    GPR3.delete(0, END)
    IXR1.delete(0, END)
    IXR2.delete(0, END)
    IXR3.delete(0, END)
    PC.delete(0, END)
    MAR.delete(0, END)
    MBR.delete(0, END)
    IR.delete(0, END)
    MFR.delete(0, END)
    Privileged.delete(0, END)

    GPR0.insert(0, "0000000000000000")
    GPR1.insert(0, "0000000000000000")
    GPR2.insert(0, "0000000000000000")
    GPR3.insert(0, "0000000000000000")
    IXR1.insert(0, "0000000000000000")
    IXR2.insert(0, "0000000000000000")
    IXR3.insert(0, "0000000000000000")
    PC.insert(0, "000000000000")
    MAR.insert(0, "000000000000")
    MBR.insert(0, "0000000000000000")
    IR.insert(0, "0000000000000000")
    MFR.insert(0, "0000")
    Privileged.insert(0, "0")
    cpu.reset()


# Functions for Load, Store, StorePlus, Run, SS, Init

#Loads instruction pointed to by MAR and places it into MBR
def Load():
    cpu.MBR.set_val(cpu.Memory.words[cpu.MAR.get_val()])
    MBR.delete(0, END)
    MBR.insert(0, str(decimal_to_binary(cpu.MBR.get_val())))

#gets data from MBR and stores it in addres defined in MAR
def store():
    cpu.Memory.words[cpu.MAR.get_val()] = cpu.MBR.get_val()

#gets data from MBR and stores it in address defined in MAR, then increments MAR to next memory address
def storeplus():
    cpu.Memory.words[cpu.MAR.get_val()] = cpu.MBR.get_val()
    cpu.MAR.set_val(cpu.MAR.get_val() + 1)
    MAR.delete(0, END)
    MAR.insert(0, str(decimal_to_binary(cpu.MAR.get_val(), 12)))

#fetches address from Program Counter and executes corresponding instruction 
def singlestep():
    cpu.MAR.set_val(cpu.PC.get_addr())
    cpu.PC.increment_addr()  # points to next instruction
    addr = cpu.MAR.get_val()
    cpu.MBR.set_val(cpu.Memory.words[addr])
    cpu.IR.set_instruction(cpu.MBR.get_val())
    opcode, operand, index_register, mode, general_register = cpu.IR.decode()
    code = cpu.single_step(opcode, operand, index_register, mode, general_register)

    if code == -1:
        HaltLight.delete(0, END)
        HaltLight.insert(0, str(1))
        reset()
        return -1

    PC.delete(0, END)
    PC.insert(0, str(decimal_to_binary(cpu.PC.get_addr(), 12)))
    MAR.delete(0, END)
    MBR.delete(0, END)
    MAR.insert(0, str(decimal_to_binary(cpu.MAR.get_val(), 12)))
    MBR.insert(0, str(decimal_to_binary(cpu.MBR.get_val())))
    show_general_register(general_register)
    show_index_register(index_register)
    return 0


def run():
    while 1:
        code = singlestep()
        gui.update()
        time.sleep(3)
        if code == -1:
            return


def init():
    cpu.Memory.read_mem()


# Place the LD buttons in the grid
GPR0_LD = Button(gui, text="LD", padx=1, pady=1, command=LD_GPR0).grid(row=0, column=2)
GPR1_LD = Button(gui, text="LD", padx=1, pady=1, command=LD_GPR1).grid(row=1, column=2)
GPR2_LD = Button(gui, text="LD", padx=1, pady=1, command=LD_GPR2).grid(row=2, column=2)
GPR3_LD = Button(gui, text="LD", padx=1, pady=1, command=LD_GPR3).grid(row=3, column=2)

IXR1_LD = Button(gui, text="LD", padx=1, pady=1, command=LD_IXR1).grid(row=5, column=2)
IXR2_LD = Button(gui, text="LD", padx=1, pady=1, command=LD_IXR2).grid(row=6, column=2)
IXR3_LD = Button(gui, text="LD", padx=1, pady=1, command=LD_IXR3).grid(row=7, column=2)

PC_LD = Button(gui, text="LD", padx=1, pady=1, command=LD_PC).grid(row=0, column=7)
MAR_LD = Button(gui, text="LD", padx=1, pady=1, command=LD_MAR).grid(row=1, column=7)
MBR_LD = Button(gui, text="LD", padx=1, pady=1, command=LD_MBR).grid(row=2, column=7)

# Initializing operation buttons
Store = Button(frameoperation, text="Store", command=store)
StorePlus = Button(frameoperation, text="St+", command=storeplus)
Load = Button(frameoperation, text="Load", command=Load)
Init = Button(frameoperation, text="Init", command=init)
SS = Button(framerun, text="SS", command=singlestep)
Run = Button(framerun, text="Run", command=run)

# Initializing Halt and Run Light
HaltLabel = Label(framerun, text="Halt")
RunLabel = Label(framerun, text="Run")
SpaceSSRUN = Label(framerun, text="          ")
RunLight = Entry(framerun, width=1, borderwidth=1)
HaltLight = Entry(framerun, width=1, borderwidth=1)

# Setting both to zero, change to be implemented based on further function
RunLight.insert(0, "0")
HaltLight.insert(0, "0")

# Placing Run and Halt labels and lights on the grid
HaltLabel.grid(row=7, column=4)
RunLabel.grid(row=7, column=5)
HaltLight.grid(row=1, column=4)
RunLight.grid(row=1, column=5)

# Placing operarion buttons on the grid
Store.grid(row=7, column=7)
StorePlus.grid(row=7, column=8)
Load.grid(row=7, column=9)
Init.grid(row=7, column=10)
SS.grid(row=1, column=0)

Run.grid(row=1, column=3)

gui.mainloop()
