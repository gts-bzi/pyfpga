"""Openflow examples."""

import argparse

from pyfpga.openflow import Openflow


parser = argparse.ArgumentParser()
parser.add_argument(
    '--board', choices=['icestick', 'edu-ciaa', 'orangecrab', 'ecp5evn'],
    default='icestick'
)
parser.add_argument(
    '--source', choices=['vlog', 'vhdl', 'slog'], default='vlog'
)
parser.add_argument(
    '--action', choices=['make', 'prog', 'all'], default='make'
)
args = parser.parse_args()

prj = Openflow(odir='../build/openflow')

if args.board == 'icestick':
    prj.set_part('hx1k-tq144')
    prj.add_param('FREQ', '100000000')
    prj.add_cons('../sources/icestick/clk.pcf', 'par')
    prj.add_cons('../sources/icestick/led.pcf', 'par')
if args.board == 'edu-ciaa':
    prj.set_part('hx1k-tq144')
    prj.add_param('FREQ', '100000000')
    prj.add_cons('../sources/edu-ciaa/clk.pcf', 'par')
    prj.add_cons('../sources/edu-ciaa/led.pcf', 'par')
if args.board == 'orangecrab':
    prj.set_part('25k-CSFBGA285')
    prj.add_param('FREQ', '100000000')
    prj.add_cons('../sources/orangecrab/clk.lpf', 'par')
    prj.add_cons('../sources/orangecrab/led.lpf', 'par')
if args.board == 'ecp5evn':
    prj.set_part('um5g-85k-CABGA381')
    prj.add_param('FREQ', '100000000')
    prj.add_cons('../sources/ecp5evn/clk.lpf', 'par')
    prj.add_cons('../sources/ecp5evn/led.lpf', 'par')

prj.add_param('FREQ', '100000000')
prj.add_param('SECS', '1')

if args.source == 'vhdl':
    prj.add_vhdl('../sources/vhdl/*.vhdl', 'blink_lib')
if args.source == 'vlog':
    prj.add_include('../sources/vlog/include1')
    prj.add_include('../sources/vlog/include2')
    prj.add_vlog('../sources/vlog/*.v')
if args.source == 'slog':
    prj.add_include('../sources/slog/include1')
    prj.add_include('../sources/slog/include2')
    prj.add_vlog('../sources/slog/*.sv')
if args.source in ['vlog', 'slog']:
    prj.add_define('DEFINE1', '1')
    prj.add_define('DEFINE2', '1')

prj.set_top('Top')

if args.action in ['make', 'all']:
    prj.make()

if args.action in ['prog', 'all']:
    prj.prog()