import re
import argparse as ap

PAL_ENTRY = re.compile(r'((\d{1,3})\s+(\d{1,3})\s+(\d{1,3}))\s+Index\s+\d+$', re.M)

parser = ap.ArgumentParser(description="Convert GIMP .gpl palette files to JASC format PAL files.")
parser.add_argument('gpl_file', type=ap.FileType('r'), help='GPL palette file exported from GIMP.')
parser.add_argument('output_pal', type=ap.FileType('wb'), help='Target JASC-PAL formatted palette file.')

args = parser.parse_args()

entries = [x[1:] for x in re.findall(PAL_ENTRY, args.gpl_file.read())]

if len(entries) <= 16:
	while len(entries) < 16:
		entries.append((0,0,0))
else:
	while len(entries) < 256:
		entries.append((0,0,0))

args.output_pal.write(b'JASC-PAL\r\n')
args.output_pal.write(b'0100\r\n')
args.output_pal.write(bytes('{}\r\n'.format(len(entries)), 'ascii'))
for entry in entries:
	args.output_pal.write(bytes('{0} {1} {2}\r\n'.format(*entry), 'ascii'))
