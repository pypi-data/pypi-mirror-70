class EPDconst():
    """Contains constants common to all Waveshare e-Ink displays"""
    pass


class EPD4in2const(EPDconst):

    # These are very similar to the ones in WaveshareFull, but very different
    # from the ones in WavesharePartial

    PANEL_SETTING                  = 0x00
    POWER_SETTING                  = 0x01
    POWER_OFF                      = 0x02
    POWER_OFF_SEQUENCE_SETTING     = 0x03
    POWER_ON                       = 0x04
    POWER_ON_MEASURE               = 0x05
    BOOSTER_SOFT_START             = 0x06
    DEEP_SLEEP                     = 0x07
    DATA_START_TRANSMISSION_1      = 0x10
    DATA_STOP                      = 0x11
    DISPLAY_REFRESH                = 0x12
    DATA_START_TRANSMISSION_2      = 0x13
    VCOM_LUT                       = 0x20
    W2W_LUT                        = 0x21
    B2W_LUT                        = 0x22
    W2B_LUT                        = 0x23
    B2B_LUT                        = 0x24
    PLL_CONTROL                    = 0x30
    TEMPERATURE_SENSOR_CALIBRATION = 0x40
    TEMPERATURE_SENSOR_SELECTION   = 0x41
    TEMPERATURE_SENSOR_WRITE       = 0x42
    TEMPERATURE_SENSOR_READ        = 0x43
    VCOM_AND_DATA_INTERVAL_SETTING = 0x50
    LOW_POWER_DETECTION            = 0x51
    TCON_SETTING                   = 0x60
    RESOLUTION_SETTING             = 0x61
    GET_STATUS                     = 0x71
    AUTO_MEASURE_VCOM              = 0x80
    READ_VCOM_VALUE                = 0x81
    VCM_DC_SETTING                 = 0x82
    PARTIAL_WINDOW                 = 0x90
    PARTIAL_IN                     = 0x91
    PARTIAL_OUT                    = 0x92
    PROGRAM_MODE                   = 0xA0
    ACTIVE_PROGRAM                 = 0xA1
    READ_OTP_DATA                  = 0xA2
    POWER_SAVING                   = 0xE3

    # luts for full screen updates

    LUT_VCOM0 = [
        0x00, 0x17, 0x00, 0x00, 0x00, 0x02,
        0x00, 0x17, 0x17, 0x00, 0x00, 0x02,
        0x00, 0x0a, 0x01, 0x00, 0x00, 0x01,
        0x00, 0x0e, 0x0e, 0x00, 0x00, 0x02,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00,
    ]

    LUT_WW = [
        0x40, 0x17, 0x00, 0x00, 0x00, 0x02,
        0x90, 0x17, 0x17, 0x00, 0x00, 0x02,
        0x40, 0x0a, 0x01, 0x00, 0x00, 0x01,
        0xa0, 0x0e, 0x0e, 0x00, 0x00, 0x02,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    LUT_BW = [
        0x40, 0x17, 0x00, 0x00, 0x00, 0x02,
        0x90, 0x17, 0x17, 0x00, 0x00, 0x02,
        0x40, 0x0a, 0x01, 0x00, 0x00, 0x01,
        0xa0, 0x0e, 0x0e, 0x00, 0x00, 0x02,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    LUT_WB = [
        0x80, 0x17, 0x00, 0x00, 0x00, 0x02,
        0x90, 0x17, 0x17, 0x00, 0x00, 0x02,
        0x80, 0x0a, 0x01, 0x00, 0x00, 0x01,
        0x50, 0x0e, 0x0e, 0x00, 0x00, 0x02,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    LUT_BB = [
        0x80, 0x17, 0x00, 0x00, 0x00, 0x02,
        0x90, 0x17, 0x17, 0x00, 0x00, 0x02,
        0x80, 0x0a, 0x01, 0x00, 0x00, 0x01,
        0x50, 0x0e, 0x0e, 0x00, 0x00, 0x02,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    # luts for partial screen updates

    PARTIAL_LUT_VCOM1 = [
        0x00, 0x19, 0x01, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00
    ]

    PARTIAL_LUT_WW1 = [
        0x00, 0x19, 0x01, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    PARTIAL_LUT_BW1 = [
        0x80, 0x19, 0x01, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    PARTIAL_LUT_WB1 = [
        0x40, 0x19, 0x01, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    PARTIAL_LUT_BB1 = [
        0x00, 0x19, 0x01, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    # gray

    # 0~3 gray
    GRAY_LUT_VCOM = [
        0x00, 0x0a, 0x00, 0x00, 0x00, 0x01,
        0x60, 0x14, 0x14, 0x00, 0x00, 0x01,
        0x00, 0x14, 0x00, 0x00, 0x00, 0x01,
        0x00, 0x13, 0x0a, 0x01, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    ]

    # r21
    GRAY_LUT_WW = [
        0x40, 0x0a, 0x00, 0x00, 0x00, 0x01,
        0x90, 0x14, 0x14, 0x00, 0x00, 0x01,
        0x10, 0x14, 0x0a, 0x00, 0x00, 0x01,
        0xa0, 0x13, 0x01, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    # r22h	r
    GRAY_LUT_BW = [
        0x40, 0x0a, 0x00, 0x00, 0x00, 0x01,
        0x90, 0x14, 0x14, 0x00, 0x00, 0x01,
        0x00, 0x14, 0x0a, 0x00, 0x00, 0x01,
        0x99, 0x0c, 0x01, 0x03, 0x04, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    # r23h	w
    GRAY_LUT_WB = [
        0x40, 0x0a, 0x00, 0x00, 0x00, 0x01,
        0x90, 0x14, 0x14, 0x00, 0x00, 0x01,
        0x00, 0x14, 0x0a, 0x00, 0x00, 0x01,
        0x99, 0x0b, 0x04, 0x04, 0x01, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    # r24h	b
    GRAY_LUT_BB = [
        0x80, 0x0a, 0x00, 0x00, 0x00, 0x01,
        0x90, 0x14, 0x14, 0x00, 0x00, 0x01,
        0x20, 0x14, 0x0a, 0x00, 0x00, 0x01,
        0x50, 0x13, 0x01, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
