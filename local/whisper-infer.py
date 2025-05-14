import whisper
import tqdm
import warnings
import sys
warnings.filterwarnings("ignore")

model = whisper.load_model("large-v3-turbo")

with open(sys.argv[1], "r") as fscp:
    lines = fscp.readlines()

with open(sys.argv[2], "w") as f:
    for line in  tqdm.tqdm(lines, desc="Transcribing", unit="utterance"):
        uttid, filepath = line.split()
        result = model.transcribe(filepath)
        print(uttid, result["text"], file=f)
