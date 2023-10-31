import whisper
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument( 'infile', type = str)
parser.add_argument( '-n', '--max_files', type = int, default = 0 )
parser.add_argument( '--model', type = str, default = "base" )
parser.add_argument( '--task', type = str, default = "transcribe" )
parser.add_argument( '--lang', type = str, default = "en" )
parser.add_argument( '--beam_size', type = int, default = None)
parser.add_argument( '--best_of', type = int, default = None)
parser.add_argument( '--temperature', type = str, default = None)
parser.add_argument( '--condition_on_previous_text', type = str, default = None)
parser.add_argument( '--fp16', type = str, default = None)
parser.add_argument( '--list_options', action = "store_true")

args = parser.parse_args()
if args.list_options:
    opts = whisper.DecodingOptions()
    print(opts)
    sys.exit()

model = whisper.load_model(args.model)
option = {}
option["task"] = args.task
if args.lang:
    option["language"] = args.lang
if args.beam_size:
    option["beam_size"] = args.beam_size
if args.best_of:
    option["best_of"] = args.best_of
if args.temperature:
    temp = [ float(v) for v in args.temperature.split(",") ]
    if len(temp) > 1:
        option["temperature"] = tuple(temp)
    else:
        option["temperature"] = temp
if args.condition_on_previous_text:
    option["condition_on_previous_text"] = ( args.condition_on_previous_text == "True" )
if args.fp16:
    option["fp16"] = ( args.fp16 == "True" )

with open(args.infile, "r") as f:
    for n, line in enumerate(f):
        if args.max_files > 0 and args.max_files < n:
            break
        w = line.split()
        if len(w) != 2:
            raise f"Error in input file {args.infile} at line {line}"
        result = model.transcribe(w[1], **option)
        print(w[0], result["text"].strip())
