#
# Copyright (C) 2019-2024 Rodrigo A. Melo
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Implements support for Quartus.
"""

# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=duplicate-code

from pyfpga.project import Project


class Quartus(Project):
    """Class to support Quartus projects."""

    def _make_prepare(self, steps):
        context = {
            'PROJECT': self.name or 'quartus',
            'PART': self.data.get('part', '10M50SCE144I7G')
        }
        for step in steps:
            context[step] = 1
        if 'includes' in self.data:
            includes = []
            for include in self.data['includes']:
                includes.append(str(include))
            context['INCLUDES'] = ' '.join(includes)
        files = []
        if 'files' in self.data:
            types = {
                'slog': 'SYSTEMVERILOG_FILE',
                'vhdl': 'VHDL_FILE',
                'vlog': 'VERILOG_FILE'
            }
            for file in self.data['files']:
                hdl = self.data['files'][file]['hdl']
                lib = self.data['files'][file].get('lib', None)
                typ = types[hdl]
                line = f'set_global_assignment -name {typ} {file}'
                if lib:
                    line += f' -library {lib}'
                files.append(line)
        if 'constraints' in self.data:
            for file in self.data['constraints']:
                if file.suffix == '.sdc':
                    line = f'set_global_assignment -name SDC_FILE {file}'
                else:
                    line = f'source {file}'
                files.append(line)
        if files:
            context['FILES'] = '\n'.join(files)
        if 'top' in self.data:
            context['TOP'] = self.data['top']
        if 'defines' in self.data:
            defines = []
            for key, value in self.data['defines'].items():
                defines.append(f'{key} {value}')
            context['DEFINES'] = ' '.join(defines)
        if 'params' in self.data:
            params = []
            for key, value in self.data['params'].items():
                params.append(f'{key} {value}')
            context['PARAMS'] = ' '.join(params)
        if 'hooks' in self.data:
            for stage in self.data['hooks']:
                context[stage.upper()] = '\n'.join(self.data['hooks'][stage])
        self._create_file('quartus', 'tcl', context)
        return 'quartus_sh --script quartus.tcl'

    def _prog_prepare(self, bitstream, position):
        # sof: SRAM Object File
        # pof: Programming Object File
        if not bitstream:
            basename = self.name or 'quartus'
            bitstream = f'{basename}.sof'
        context = {'BITSTREAM': bitstream, 'POSITION': position}
        self._create_file('quartus-prog', 'tcl', context)
        return 'bash quartus-prog.sh'
