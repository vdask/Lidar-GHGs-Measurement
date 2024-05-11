import warnings
import serial
import time

def serialsend(ser_object, command):
    ser_object.reset_input_buffer()
    print("Writing: ", command)
    command = command.encode()
    ser_object.write(command)
    reply = ser_object.readline()
    print("Reading: ", reply.decode())
    return reply.decode()

def serialsend_mute(ser_object, command):
    ser_object.reset_output_buffer()
    ser_object.reset_input_buffer()
    command = command.encode()
    ser_object.write(command)
    reply = ser_object.readline()
    return reply.decode()


def read_serial(ser):
    reply = ser.readline()
    return reply.decode()



