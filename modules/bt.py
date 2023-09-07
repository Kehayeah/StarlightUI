elif id == 0x123:
            print("123")
            print((msg.data).hex("#"))
            message = (msg.data).hex("#")
            messageSplit = message.split("#")
            if messageSplit[0] == "10" and messageSplit[2] == "81":
                task.stop()
                time.sleep(1)
                msgList = can.Message(arbitration_id=0x2DF, data=[0x05,0x01,0x30,0x30,0x30,0x30], is_extended_id=False)
                bus.send(msgList)
                print ("sent first pin")
                
            elif messageSplit[0] == "23":
                if test:
                    #task.stop()
                    test = False
                else: 
                    msgList = can.Message(arbitration_id=0x1DF, data=[0x00, 0x00, 0x20, 0x00], is_extended_id=False)
                    task = bus.send_periodic(msgList, 0.2)
                    # time.sleep(0.2)
                    # msgList = can.Message(arbitration_id=0x2DF, data=[0x01,0x30, 0x30,0x30,0x30, 0x00, 0x00, 0x00], is_extended_id=False)
                    # task.start()
            else :
                msgFCF = can.Message(arbitration_id=0x29F, data=[0x30, 0x00, 0x0A], is_extended_id=False)
                bus.send(msgFCF)
                time.sleep(0.2)
                msgList = can.Message(arbitration_id=0x2DF, data=[0x01,0x30,0x30,0x30,0x30,0x0,0x0,0x0], is_extended_id=False)
                bus.send(msgList)
        elif id == 0x263:
            print("263")
            print((msg.data).hex("#"))
            msgList = can.Message(arbitration_id=0x2DF, data=[0x20, 0x00, 0x00, 0x00], is_extended_id=False)
            bus.send(msgList)
            print ("sent Empty")
            time.sleep(0.2)
            msgList = can.Message(arbitration_id=0x1DF, data=[0x00, 0x00, 0x20, 0x00], is_extended_id=False)
            task = bus.send_periodic(msgList, 0.2)
            task.start()
            test = True