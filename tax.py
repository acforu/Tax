monthlyBaseLine = [
    (1500,0.03,0), 
    (4500, 0.1,105), 
    (9000, 0.2,555), 
    (35000,0.25,1005), 
    (55000, 0.3,2755), 
    (80000, 0.35,5505), 
    (0x7ffffff, 0.45,13505)]

yearBaseLine = [
    (1500*12,0.03,0), 
    (4500*12, 0.1,105), 
    (9000*12, 0.2,555), 
    (35000*12,0.25,1005), 
    (55000*12, 0.3,2755), 
    (80000*12, 0.35,5505), 
    (0x7ffffff, 0.45,13505)]


def texReverse(tax):
    prveBase = 0
    for base,ratio,magic in monthlyBaseLine:
        guess =  (tax + magic)/ratio + 3500
        if guess >= prveBase and guess < base:
            return guess
        prveBase = base
    raise

def tax(value):
    return taxImpl(value,monthlyBaseLine,3500)

def taxYear(value):
    return taxImpl(value,yearBaseLine,0)

def taxImpl(value,baseline,freebase):
    if value <= freebase:
        return 0
    value = value - freebase
    for base,ratio,magic in baseline:
        if value <= base:
            return value*ratio-magic
    raise

# secondMonthAdd 挪到第二个月
# saveTax 避税额
# salaryTax 每月缴纳个人所得税
# 返回税前和税后数目
def calcYearTotal(secondMonthAdd,saveTax,salaryTax):
    diff = 0x7ffffff
    ret = (0,0)
    for yearBase,_,_ in yearBaseLine[:-1]:
        t1 = taxYear(yearBase + secondMonthAdd)
        s1 = t1 + salaryTax
        s2 = taxYear(yearBase) + tax(secondMonthAdd + texReverse(salaryTax))
        if abs(s1-s2-saveTax)<diff:
            diff = abs(s1-s2-saveTax)
            total = yearBase + secondMonthAdd 
            get = int(total - taxYear(yearBase + secondMonthAdd) + saveTax)
            ret = (total,get)
    return ret

