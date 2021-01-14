#   System specifications:
    Camera FoV: 120 degrees at least
    Camera cable length: at least 1m
    Camera fps: at least consistant 30 fps
    
    Proccessing rate: at least 25fps

    Raspberry Pi: 3+
    Operation system: PyFRC

#   JSON format:
    {
        "team": <team number>,
        "ntmode": <"client" or "server", "client" if unspecified>
        "cameras": [
            {
                "name": <camera name>
                "path": <path, e.g. "/dev/video0">
                "pixel format": <"MJPEG", "YUYV", etc>   // optional
                "width": <video mode width>              // optional
                "height": <video mode height>            // optional
                "fps": <video mode fps>                  // optional
                "brightness": <percentage brightness>    // optional
                "white balance": <"auto", "hold", value> // optional
                "exposure": <"auto", "hold", value>      // optional
                "properties": [                          // optional
                    {
                        "name": <property name>
                        "value": <property value>
                    }
                ],
                "stream": {                              // optional
                    "properties": [
                        {
                            "name": <stream property name>
                            "value": <stream property value>
                        }
                    ]
                }
            }
        ]
        "switched cameras": [
            {
                "name": <virtual camera name>
                "key": <network table key used for selection>
                // if NT value is a string, it's treated as a name
                // if NT value is a double, it's treated as an integer index
            }
        ]
    }