import subprocess

subprocess.call('python mvmts_generator.py complete_movements_spreadsheet.csv', shell=True)
subprocess.call('python remove_incomplete_segments.py movements.csv valid_movements.csv', shell=True)