FROM manimcommunity/manim

USER root

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    xdg-utils \
    vlc \
    libasound-dev \
    libportaudio2  \ 
    libportaudiocpp0 \ 
    portaudio19-dev

# RUN pip install -r requirements.txt
# RUN pip install pyaudio

USER manimuser
