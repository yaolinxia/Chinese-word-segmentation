import xml.dom.minidom
dom=xml.dom.minidom.parse('E:\python_workspace\WenShu_Test\C__Users_Administrator_Desktop_民事二审案件_民事二审案件_47.xml')
b=dom.getElementsByTagName('QW')
bb=b[0]
text=bb.getAttribute('value')

with open('E:\python_workspace\WenShu_Test\\test.txt','w',encoding="utf-8") as f:
    f.write(text)

#f=open('','w')
#f.write(text)
#f.close()
print(text);