from credenciales import ssid, password
from machine import Pin
import network
import utime
def conectar_wifi():
    led = Pin(2, Pin.OUT)
    led.value(0)  # led inicialmente encendido para indicar que nos estamos intentando conectar a la wifi
    print("\nConectado a {} ...".format(ssid), end='')
    red = network.WLAN(network.STA_IF)
    red.active(True)
    # red.scan()  # Escanea y te muestra redes disponibles
    red.connect(ssid, password)
    while not red.isconnected():  # Espera hasta que este conectado
        utime.sleep(0.1)
    print("conectado!")
    print(red.ifconfig())  # ver la ip que se nos ha asignado por DHCP
    led.value(1)  # apagamos led para indicar que ya estamos conectados


# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------

import urandom
from umqtt.simple import MQTTClient
from machine import ADC, Timer

class Mymqtt:
    def callback_msg(self, topic, msg):
        print("{}: {}".format(topic.decode(),msg.decode()))

    def timer_check_msg(self,inst):
        if self.check_msg:
            self.client.check_msg()

    def __init__(self, topic=None, server="broker.hivemq.com", client=None, callback=None, check_msg=False):
        conectar_wifi()
        urandom.seed(ADC(0).read())
        self.server = server
        self.id_client = str(urandom.getrandbits(18)) if client is None else client
        self.topic = topic
        self.client = MQTTClient(self.id_client, self.server)
        self.client.set_callback(self.callback_msg if callback is None else callback)
        self.client.connect()
        self.check_msg = check_msg
        self.timer = Timer(-1)
        self.timer.init(period=1000, mode=Timer.PERIODIC, callback=self.timer_check_msg)

    def msg_off(self):
        self.check_msg=False

    def msg_on(self):
        self.check_msg=True

    def send(self, msg, topic=None):
        topic = self.topic if topic is None else topic
        if topic is None: # Si no se ha dado un topic nuevo
            print("NO ENVIADO, no se ha proporcionado ningún topic")
            return False
        self.client.publish(topic, msg)
        return True

    def subscribe(self, *topics):
        for top in topics:
            self.client.subscribe(b'{}'.format(top))



# -------------------------------------------------------------------------
# USO:
#
# from mymqtt import Mymqtt
# mq = Mymqtt("topic_molon")
# mq.subscribe("topic_molon")   # mq.subscribe("topic1","topic2","topic3", ...)
# mq.msg_on()                   # mq = Mymqtt("topic_molon", check_msg=True)
# mq.send("hola topic")
# mq.send("hola topic 2", "otro_topic_molon")
