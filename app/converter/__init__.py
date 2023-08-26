if __name__ == "__main__":
    from app.converter.deezer_playlist import *
    from app.converter.converter import *
    from app.converter.spotify_playlist import *
else:
    from .converter import *

if __name__ == "__main__":
    DEEZER_ACCESS_TOKEN = "frSQDkMaW8JVoZnqjFP0ucxi1UuqfsfKdbRryOtXWV4ITJXkhG2"
    SPOTIFY_ACCESS_TOKEN = "BQCYzIJYjtZ4jYWQxevFW7W6PiwryuJ5t8rSs9AfpdyazoIOWVtzaNZBUQKjBxy4auQwf-P3xprADn5zhCkysDy2wnT5HpW10ttCWliZd2Byu4rCWVGqTV1cpXY6lrsw6DQNEwr-K_TdExP5dvgxXYdBjD91ejD-Y5RqLZ06O3vwi-x_HFh-PqNeRLB34RX_xP34Dd_2sjq49ZwV1g_AwOL2jwN0KfuZbS6xBC3O8Ap0ICr7LI54RtDhr_L4w12xAwVsDkH49wY89XsL"
    SPOTIFY_USER_ID = "21nhr55xfe73uiranugaysfqy"

    converter = Converter(SPOTIFY_ACCESS_TOKEN, DEEZER_ACCESS_TOKEN, SPOTIFY_USER_ID)
    converter.convert_deezer_to_spotify("11499268504")