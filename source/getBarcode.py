import usb.core
from httplib2 import Http
from urllib import urlencode

def processBarcode(barcode):
    url = 'http://127.0.0.1:5000'
    h = Http()
    data = dict(code=barcode)
    print data
    resp, content = h.request(url,"POST", urlencode(data))
    print resp['status']
    print content
    print barcode

# find our device
dev = usb.core.find(idVendor=0x13ba, idProduct=0x0018)

# was it found?
if dev is None:
    print 'Device not found'
else:
    print 'Device found'

# first endpoint
interface = 0
endpoint = dev[0][(0,0)][0]

if dev.is_kernel_driver_active(interface) is True:
    dev.detach_kernel_driver(interface)
    # claim the device
    usb.util.claim_interface(dev, interface)

collected = 0
attempts = 50

liste = []
collected = 0
dataToCollect = 26

while True :
    try:
        data = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize)
        #print data
        if collected < dataToCollect:
            if collected % 2 == 0:
                number = data[2] - 29
                if number > 9:
                    number -= 10
                liste.append(number)

        collected += 1
            
        if collected > 27:
            barCode = ''.join(map(str, liste))
            processBarcode(barCode)
            collected = 0
            liste[:] = []
        
    except usb.core.USBError as e:
        data = None
        if e.args == ('Operation timed out',):
            continue
        
# release the device
usb.util.release_interface(dev, interface)
# reattach the device to the OS kernel
dev.attach_kernel_driver(interface)
    
