import time
from pySerialTransfer import pySerialTransfer as txfer

class sensorStruct(object):
    sensor_1 = 91.0
    sensor_2 = 81.0


class pantiltStruct(object):
    pan = 22.0
    tilt = 11.0


arr = ''

if __name__ == '__main__':
    try:
        testStruct = pantiltStruct
        dataStruct = sensorStruct
        link = txfer.SerialTransfer('/dev/ttyUSB1')
        
        link.open()
        time.sleep(5) # allow some time for the Arduino to completely reset
        
        while True:
            pantiltSendSize = 0
            #sendSize = link.tx_obj(testStruct.sensor_1, start_pos=sendSize)
            #sendSize = link.tx_obj(testStruct.sensor_2, start_pos=sendSize)
            pantiltSendSize = link.tx_obj(testStruct.pan, start_pos=pantiltSendSize)
            pantiltSendSize = link.tx_obj(testStruct.tilt, start_pos=pantiltSendSize)
            link.send(pantiltSendSize)
            
            ###################################################################
            # Wait for a response and report any errors while receiving packets
            ###################################################################
            while not link.available():
                if link.status < 0:
                    if link.status == txfer.CRC_ERROR:
                        print('ERROR: CRC_ERROR')
                    elif link.status == txfer.PAYLOAD_ERROR:
                        print('ERROR: PAYLOAD_ERROR')
                    elif link.status == txfer.STOP_BYTE_ERROR:
                        print('ERROR: STOP_BYTE_ERROR')
                    else:
                        print('ERROR: {}'.format(link.status))
            

                recSize = 0
                
                dataStruct.sensor_1 = link.rx_obj(obj_type='f', start_pos=recSize)
                recSize += txfer.STRUCT_FORMAT_LENGTHS['f']
                
                dataStruct.sensor_2 = link.rx_obj(obj_type='f', start_pos=recSize)
                recSize += txfer.STRUCT_FORMAT_LENGTHS['f']

                
                
                print('{} {} {} {}'.format(dataStruct.sensor_1, dataStruct.sensor_2,testStruct.pan, testStruct.tilt))
                time.sleep(1)
    
    except KeyboardInterrupt:
        try:
            link.close()
        except:
            pass
    
    except:
        import traceback
        traceback.print_exc()
        
        try:
            link.close()
        except:
            pass