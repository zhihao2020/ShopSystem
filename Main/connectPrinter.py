from printer import Printer
from time import localtime, strftime

def Printmain(name=None,phone=None,data=None, fin=None, keyongThing=None, Hand_FinList=None):

    p = Printer()
    p.lines = []
    p.add_line("医琦母婴护理")
    p.add_line("**************")
    p.add_line("下单时间:" + strftime("%d/%m/%Y %X", localtime()))
    if name:
        p.add_line("顾客姓名：" + name)
    if phone:
        p.add_line("顾客电话：" + phone)
    p.add_line("**************")
    if Hand_FinList:
        for temp in Hand_FinList:
            p.add_line("手法名称：" + str(temp[0]))
            p.add_line("使用次数："+str(temp[2]))
            p.add_line("剩余次数：" + str(temp[1]))
            p.add_line("         ")
    if data:
        p.add_line("品名     数量   金额")
        for x in data:
            name_id = x[0]
            price = x[1]
            num = x[2]
            p.add_line(name_id + '    ' + str(num) + '   ' + str(price))
        p.add_line("合计： " + str(fin))
        p.add_line("可用于购买商品的金额：" + str(keyongThing))
    p.add_line("**************")
    p.add_line("欢迎光临，谢谢惠顾！")
    p.add_line("医琦母婴护理")
    p.add_line("\n")

    p.add_line("******自此裁剪******")

    p.add_line("医琦母婴护理")
    p.add_line("**************")
    p.add_line("下单时间:" + strftime("%d/%m/%Y %X", localtime()))
    if name:
        p.add_line("顾客姓名：" + name)
    if phone:
        p.add_line("顾客电话：" + phone)
    p.add_line("**************")
    if Hand_FinList:
        for temp in Hand_FinList:
            p.add_line("手法名称：" + str(temp[0]))
            p.add_line("使用次数："+str(temp[2]))
            p.add_line("剩余次数：" + str(temp[1]))
            p.add_line("         ")
    if data:
        p.add_line("品名     数量   金额")
        for x in data:
            name_id = x[0]
            price = x[1]
            num = x[2]
            p.add_line(name_id + '    ' + str(num) + '   ' + str(price))
        p.add_line("合计： " + str(fin))
        p.add_line("可用于购买商品的金额：" + str(keyongThing))
    p.add_line("**************")
    p.add_line("欢迎光临，谢谢惠顾！")
    p.add_line("医琦母婴护理")
    p.add_line("\n")

    p.output()
