from printer import Printer
from time import localtime, strftime

def Printmain(data,fin):
    p = Printer()
    p.add_line("医琦健康")
    p.add_line("**************")
    p.add_line("下单时间:"+strftime("%d/%m/%Y %X", localtime()))
    p.add_line("**************")
    p.add_line("品名     数量   金额")
    for x in data:
        name = x[0]
        price = x[1]
        num = x[2]
        p.add_line(name,'    ',price,'   ',num)
    p.add_line("合计： "+fin)
    p.add_line("**************")
    p.add_line("欢迎光临，谢谢惠顾！")
    p.add_line("医琦健康中心")
    p.add_line("\n")
    p.output()

if __name__ == '__main__':
    Printmain()