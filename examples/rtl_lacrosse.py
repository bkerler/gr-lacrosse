#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Rtl Lacrosse
# GNU Radio version: v3.11.0.0git-55-g8526e6f8

from gnuradio import analog
import math
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import gnuradio.lacrosse as lacrosse
import osmosdr
import time
import reveng




class rtl_lacrosse(gr.top_block):

    def __init__(self, rf_gain=25):
        gr.top_block.__init__(self, "Rtl Lacrosse", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.rf_gain = rf_gain

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1e6

        ##################################################
        # Blocks
        ##################################################
        self.rtlsdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ''
        )
        self.rtlsdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(915e6, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(rf_gain, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
        self.reveng_pattern_dump = reveng.pattern_dump([1,0]*16, 24+8+8+8+8+16, '%Y-%m-%d %H:%M:%S,%[bits]', False, '', False)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=4,
                decimation=58,
                taps=[],
                fractional_bw=0)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                200e3,
                100e3,
                window.WIN_HAMMING,
                6.76))
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(4, 0.25*0.175*0.175, 0.5, 0.175, 0.005)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.dc_blocker_xx_0 = filter.dc_blocker_ff(32, True)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(1)
        self.TX29U_0 = lacrosse.TX29U()


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.reveng_pattern_dump, 'out'), (self.TX29U_0, 'in'))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.dc_blocker_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.reveng_pattern_dump, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.dc_blocker_xx_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.low_pass_filter_0, 0))


    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.rtlsdr_source_0.set_gain(self.rf_gain, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 200e3, 100e3, window.WIN_HAMMING, 6.76))
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-g", "--rf-gain", dest="rf_gain", type=intx, default=25,
        help="Set RF Gain [default=%(default)r]")
    return parser


def main(top_block_cls=rtl_lacrosse, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(rf_gain=options.rf_gain)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
