
testMsgList = ['!AIVDM,1,1,,B,15MWKF0000rvJ>DHvVU:uJ8>0L0I,0*39\r\n',
'!AIVDM,1,1,,A,33ci1b1000rvU90HvmUVa6BJ0000,0*29\r\n',
'!AIVDM,1,1,,A,15MWKF0300rvJ>DHvVTruJ8R0H9t,0*2C\r\n',
'!AIVDM,2,1,0,B,53ci1b02??ShT<DJ221H4hhF08T4p<622222221@B`R8H6T10ID3lU30CQ:5,0*36\r\n',
'!AIVDM,2,2,0,B,DhJH8888880,2*09\r\n',
'!AIVDM,1,1,,B,33ci1b1000rvU<LHvm?6a6HJ0000,0*53\r\n',
'!AIVDM,1,1,,A,15MWKF0000rvJ=hHvVVbuJ9<0L0I,0*4D\r\n',
'!AIVDM,1,1,,A,15MWKF0000rvJ=DHvVW:uJ9l00RW,0*68\r\n',
'!AIVDM,1,1,,A,33ci1b11h0rvU<hHvm06a6LN0000,0*22\r\n',
'!AIVDM,1,1,,B,33ci1b11@0rvU>DHvlpVa6RN0000,0*18\r\n',
'!AIVDM,1,1,,A,15MWKF0vh0rvJ=VHvVS:uJ8V0L0I,0*5B\r\n',
'!AIVDM,1,1,,A,15MWKF0000rvJ=hHvVT:uJ;:0@E3,0*10\r\n',
'!AIVDM,1,1,,A,14`UtQhvh3rvLK:Hvkue2D>00D0?,0*09',
'!AIVDM,1,1,,A,14eG;o@034o8sd<L9i:a;WF>062D,0*7D' 
]


payloadencoding = {0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'.',11:',',12:'<',13:'=',14:'>',15:'?',16:'@',17:'A',18:'B',19:'C',20:'D',21:'E',22:'F',23:'G',24:'H',25:'I',26:'J',27:'K',28:'L',29:'M',30:'N',31:'O',32:'P',33:'Q',34:'R',35:'S',36:'T',37:'U',38:'V',39:'W',40:"`",41:'a',42:'b',43:'c',44:'d',45:'e',46:'f',47:'g', 48:'h',49:'i',50:'j',51:'k',52:'l',53:'m',54:'n',55:'o',56:'p',57:'q',58:'r',59:'s',60:'t',61:'u',62:'v',63:'w'}

def sixBit (raw) :
    tmpStr = raw[:6]
    leftOver = raw[6:]
    tmpInt = int(tmpStr,2)-48
    if tmpInt > 40 :
        tmpInt = tmpInt -8
    
    result = ""
    if ( tmpInt < 0 ) :
        result = bin(tmpInt)[3:].zfill(6)  
    else :
        result = bin(tmpInt)[2:].zfill(6)  
    #print ("step : " + str(i) + "result[" + bin(tmpInt) + "]" + str(tmpInt))

    if len(leftOver) > 0 :
        result += sixBit(leftOver)

    return result

def asciiToSixBit(raw) :
    i = ord(raw) - 48
    if i > 40 :
        i = i -8
    result = bin(i)[2:].zfill(6)
    return result

def decodeAIS ( msg ) :

    msgSplit = msg.split(',')
    msgInASCI = "Not AIS " + msgSplit[0]
    msgDict ={}

    if (msgSplit[0] == "!AIVDM" or msgSplit[0] == '!SAVDM'):
        msgInASCI = "Good Message ["

        if (msgSplit[1] == "2" ):
            msgInASCI += ", 2 part Mesg "
            fragNumb = ", 1"
            msgDict["fragNum"]=1
            if msgSplit[2] == "2" :
                fragNumb = ", 2"
                msgDict ["fragNum"] = 2

            msgInASCI + fragNumb

        else :
            msgInASCI += "Single Part Mesg"

        if msgSplit[3] == "" :
            msgDict ["seqID"] = ""
        else :
            msgInASCI += ", " + msgSplit[3]
            msgDict ["seqID"] = msgSplit[3]

        if (msgSplit[4] == "A") :
            msgInASCI += ", 161.975Mhz"
            msgDict ["Freq"] = 161.975
        else:
            msgInASCI += ", 162.025Mhz"
            msgDict ["Freq"] = 162.025

        msgDict ["rawPayload"] = msgSplit[5]
        msgInASCI += ", " + msgSplit[5]

        msgString = bytes(msgSplit[5])
        #msgString = bytes(msgSplit[5], 'ascii')
        msgBytes = ''
        for x in msgString :
            print(x + "::::" + asciiToSixBit(x))
            #msgBytes.join(asciiToSixBit(x))

        #msgDict ["bits"] = msgBytes

        #msgDict ["bits"] = ''.join(["{0:b}".format(x) for x in msg_bytes])
        
        #msgDict["type"] = str(int(sixBit(msgDict["bits"][:6]),2))
        
        #tmp6Bit = sixBit(msgDict["bits"][6:])
        #tmp = str(int(msgDict["bits"][8:30],2))
    
        #print ("[" + tmp6Bit[2:32] + "]")
        #print (msgDict["bits"])
        #print (sixBit(msgDict["bits"]))
        #print( "[" + str(int(tmp6Bit[2:32],2)) + "]")

    msgInASCI += "]"
    return msgInASCI

    


for msg in testMsgList :
    print (decodeAIS(msg))


    
    
