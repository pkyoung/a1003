# OpenAI Whisper 을 이용한 음성인식 실습

Whisper를 이용하여 음성인식을 수행합니다. 본 실습에서는 음성인식 모델의 훈련은
포함하지 않습니다. OpenAI에서 제공하는 음성인식 모델을 이용하여 평가데이터에
대하여 인식을 수행하고 인식률을 측정하는 방법을 설명합니다.


## 환경 설정
먼저 실습환경을 설정합니다. 
일반 리눅스 환경에서는 먼저 https://github.com/pkyoung/a1003.git 를 내려받습니다.

        conda create -n a1003 python=3.10
        conda activate a1003

        git clone https://github.com/pkyoung/a1003.git ~/a1003


## OpenAI Whisper 설치

Whisper는 아래와 같이 `openai-whisper` 패키지를 설치하면 됩니다. 여러가지 의존성 패키지가 설치되기때문에 시간이 소요됩니다.

        pip install openai-whisper

## 평가용 데이터셋 다운로드

huggingface에서 테스트용 데이터셋을 내려받습니다.
9명의 화자가 20개의 짧은 문장을 발성한 wav 파일과 정답전사문 파일입니다.


        cd ~/a1003
        git clone https://hf.co/datasets/pkyoung/a1003.git ./data/a1003

내려받은 파일을 확인해봅니다.
내려받은 디렉토리의 구조는 다음과 같습니다.
```
data/a1003
    ├── README.md
    ├── result_espnet_ma16k2401a.txt
    ├── result_whisper_turbo.txt
    ├── text
    ├── wav.scp
    ├── wav
    │   ├── spk1
    │   │   ├── 1.wav
    │   │   ├── 10.wav
    │   │   ├── 11.wav
    ...
```
`text` 파일과 `wav.scp` 파일은 앞서 설명한 `kaldi` 파일과 같은 형식을 갖습니다. 파일은 다음과 같은 방법으로 들어볼 수 있습니다.

## Whipser 음성인식

한개의 wav 파일에 대해서 인식을 수행해봅니다. 간단하게 파일을 입력으로 `whisper` 명령어를 실행합니다.

        whisper data/a1003/wav/spk1/1.wav

whisper는 task로 transcribe와 translate 두가지를 할 수 있습니다. 인식에 사용할 모델, 인식대상 언어를 지정하여 음성인식을 수행합니다.


        whisper --model large-v3 --language ko --task transcribe data/a1003/wav/spk6/recording_17.wav

파이선 코드 안에서는 다음과 같은 방법으로 이용할 수 있습니다. Low-level 핸들링을 위해서는 `transcribe()` 함수 외에 `decode()` 함수를 사용할 수 있습니다.


        import whisper
        model = whisper.load_model("tiny")
        result = model.transcribe("data/a1003/wav/spk6/recording_17.wav")
        print(result["text"])


전체 테스트 데이터셋 (180개) 에 대해서 인식을 수행해서 결과를 `result.txt`
파일에 저장합니다.

        python whisper-infer.py data/a1003/wav.scp result.txt

보통의 GPU 카드가 설치된 머신에서는 수 분 이내로 인식이 완료됩니다. Colab
환경에서는 10분 이상 소요될 수 있습니다.

실행이 끝나면 인식성능을 측정합니다. `editdistance` 모듈이 필요합니다.

        pip install editdistance
        python uttcer.py data/a1003/text result.txt

화자별 음성인식 성능도 측정해봅니다.
평균 오류율이 높은 화자에 대해서는 몇몇 파일을 들어봅니다.

        for s in spk{1..9}; do
          echo -n "$s " >&2
          python uttcer.py data/a1003/text <(grep "$s/" result.txt) > /dev/null
        done

문장부호를 제외한 CER을 계산합니다.

        python uttwer.py <(python pp.py -s data/a1003/text) \
          <(python pp.py -s result.txt) > /dev/null

## Whisper 모델별 음성인식 성능 및 속도

각 모델별 모델크기, 인식 소요 시간 및 인식 성능은 다음 표와 같습니다.
인식소요시간 및 인식성능은 환경에 따라 달라질 수 있습니다. (WER1, CER1: 문장부호 제외 전/WER2, CER2: 문장부호 제외 후)

| Model          | Size | Elapsed | RTF | WER1 | CER1 | WER2 | CER2 |
| ---            | ---  | ---     | --- | ---  | ---  | ---  | ---  |
| tiny           | 73M  | 1m6s    |0.04 |50.11 |26.62 |44.10 |24.55 |
| base           | 139M | 1m2s    |0.04 |38.94 |17.74 |32.76 |15.61 |
| small          | 462M | 1m38s   |0.06 |32.73 |13.07 |24.55 |10.13 |
| medium         | 1.5G | 3m5s    |0.11 |29.57 |11.14 |21.90 | 8.46 |
| large-v1       | 2.9G | 4m0s    |0.15 |25.33 | 9.03 |16.98 | 6.15 |
| large-v2       | 2.9G | 3m46s   |0.14 |30.34 |13.43 |21.64 |10.24 |
| large-v3       | 2.9G | 4m1s    |0.15 |29.44 |13.46 |20.40 |10.43 |
| large-v3-turbo | 1.6G | 1m19s   |0.05 |24.18 | 8.29 |14.67 | 5.05 |
