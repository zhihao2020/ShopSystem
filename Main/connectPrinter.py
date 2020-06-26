from printer import Printer
from time import localtime, strftime

def Printmain(data, fin, keyongThing=None, keyongHand=None):
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
        p.add_line(name+'    '+str(price)+'   '+str(num))
    p.add_line("合计： "+str(fin))
    if keyongHand:
        p.add_line("可用手法剩余金额："+str(keyongHand))
    if keyongThing:
        p.add_line("可用于购买商品的金额："+str(keyongThing))
    p.add_line("**************")
    p.add_line("欢迎光临，谢谢惠顾！")
    p.add_line("医琦健康调理中心")
    p.add_line("\n")
    p.output()