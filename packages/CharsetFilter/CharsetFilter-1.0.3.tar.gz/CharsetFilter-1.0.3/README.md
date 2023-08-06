# 中文文本字符集分析过滤工具

## 概要说明 

UTF-8字符集分析过滤工具 CharsetFilter

版本: V 1.0.３

更新：xmxoxo 　2020/6/8


GitHub地址： https://github.com/xmxoxo/CharsetFilter

工具说明：本工具把UTF8字符集分成了39个子集，可对文本文件中的字符集进行分析，
统计各类字符的总数以及出现的种类数。同时还可以方便地过滤或者保留的字符，
特别适合NLP等领域中对不可见字符的过滤分析等处理。

注: 被分析的文本文件需要是UTF8格式


##　对象调用使用案例

```
# 测试 
def test ():
    objC = CharsetFilter()
    txt = '中大1三K┫□＼，≯ó㈥l｡ ･ ･ ｡ ﾉ ♡不ε﹣￥▽￣ˊˋ﹉▲āōē﹑'
    #s = '｡ ･ ･ ｡ ﾉ ♡'
    #a = objC.segIndex(0x25b2)
    #a = objC.segIndex(0x2EF4)
    #a = objC.segIndex(0xFFFD)
    #a = objC.segIndex(0x0006)
    #a = objC.segIndex(0xFFFE)
    #a = objC.segIndex(0xFFA1)
    #a = objC.segIndex(0x2453)
    #a = objC.segIndex(0x2580) #0x25BD 0x2580
    #for x in txt:
    #    a = objC.segIndex(ord(x))
    #    print(x,hex(ord(x)),a)
    
    #print('-'*40)
    strRet = objC.charAnalyze (txt, detail=1)
    print('字符集分析报告'.center(40,'-'))
    print(strRet)
    
    remove = []
    remain = [2, 36] # 只保留 中文汉字 和 英文半角
    rettxt = objC.txtfilter(txt, remove=remove, remain=remain)
    print('过滤结果：\n%s' % rettxt)
    print('原始长度:%d, 过滤后长度:%d' % ( len(txt), len(rettxt)))
```


## 命令行使用案例说明

分析文本字符集，输出简要信息
```
CharsetFilter --file ./111.txt 
```

分析文本字符集，输出详细信息，详细信息会保存到 xxx_report.txt 文件中
```
CharsetFilter --file ./111.txt --detail 1
```


分析文本字符集，按默认值过滤(过滤 "尚未识别 0", "控制字符 3")，并保存过滤结果(自动命名)
```
CharsetFilter --file ./111.txt --filter 1
```


分析文本字符集，仅保留 1,2,36,39，并保存过滤结果(自动命名为 xxx_out.txt)
```
CharsetFilter --file ./111.txt --filter 1 --remain_charset 1 2 36 39

```