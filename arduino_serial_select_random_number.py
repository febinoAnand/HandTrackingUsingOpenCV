import serial 
import time 
import random
import serial.tools.list_ports


def list_the_port():
    serialList = list(serial.tools.list_ports.comports())
    portList = []
    print ()
    for n,port in enumerate(serialList):
        k = n + 1
        portList.append(port.device)
        print ("%d). %s"%(k,port.device))
    print ()
    return portList

def select_port_from_list(ports):
    
    selectedValue = input()
    selectedPort = 0
    try:
        selectedPort = eval(selectedValue)
        if selectedPort > len(ports) or selectedPort <= 0:
            print ("Error in inputs. Give correct Value....")
            return 0
        return (ports[selectedPort - 1])
    except Exception as e:
        print ("Error in inputs. Enter Numbers only")
        return 0
    
def connect_device(deviceToConnect):
    connectedDevice = serial.Serial(port=deviceToConnect, baudrate=9600, timeout=.1) 
    return connectedDevice

def send_data(connectedDevice, dataToSend):
    connectedDevice.write(bytes(dataToSend, 'utf-8')) 


if __name__ == '__main__':
    listedPort = list_the_port()
    print ("Select Port Number from the list:",)
    device = select_port_from_list(listedPort)
    
    if(device != 0):
        connectedDevice = connect_device(device)
        while(connectedDevice.is_open):
            data = random.randint(0,31)
            binary_data = "{0:05b}\n".format(data)
            print (binary_data)
            send_data(connectedDevice,binary_data)
            time.sleep(1)
    else:
        print ("Device not connected...")


    

    
        
