from sonyheadset import SonyHeadset, ANCMode


addr = "XX:XX:XX:XX:XX:XX"
headset = SonyHeadset(addr)
headset.connect()
#headset.set_noise_cancellation(ANCMode.AMBIENT_SOUND)
headset.set_noise_cancellation(ANCMode.NOISE_CANCELLING)
headset.disconnect()
