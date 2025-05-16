
# ESPnet 을 이용한 음성인식 실습

ESPnet 툴킷을 이용하여 음성인식을 수행합니다. 본 실습에서는 음성인식 모델의
훈련은 포함하지 않습니다. 이미 훈련된 모델을 이용하여 평가데이터에 대하여
인식을 수행하고 인식률을 측정하는 방법을 설명합니다.


## 환경 설정

먼저 실습환경을 설정합니다. `conda`는 설치되어있다고 가정합니다.
`conda` 설치는 [Setup.md](Setup.mp) 파일을 참고하세요.

        conda activate a1003
        pip install espnet torchaudio

실습에 필요한 코드를 아래와 같이 내려받습니다.

        git clone "https://github.com/pkyoung/a1003.git" ~/a1003

## ESPnet 소스코드

다음과 같이 ESPnet 소스코드를 내려받을 수 있습니다.
내려받지 않아도 음성인식 수행에는 영향이 없습니다.

        cd ~
        git clone https://github.com/espnet/espnet

`VScode`에서 `~/espent` 디렉토리를 열어봅니다.

## 평가용 데이터 다운로드

huggingface에서 테스트용 데이터셋을 내려받습니다. 9명의 화자가 각각 20개의 짧은
문장을 발성한 wav 파일과 정답전사문 파일입니다.

        cd ~/a1003/local
        git clone https://hf.co/datasets/pkyoung/a1003.git ./data/a1003

내려받은 파일을 확인해봅니다. 디렉토리의 구조는 다음과 같습니다.
```
data/a1003
    ├── README.md
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
`text` 파일과 `wav.scp` 파일은 앞서 설명한 `kaldi` 파일과 같은 형식을 갖습니다.
wav 파일을 직접 들어 봅니다. `local/play-wav.ipynb` 파일을 이용해서도 wav
파일을 들어볼 수 있습니다.

## 모델 다운로드

먼저 모델을 내려받습니다. 아래 모델은 약 8,000시간의 한국어 음성을 이용하여
ESPnet으로 훈련된 attenion/CTC 하이브리드 모델입니다. ma16k2401a 외에
ma16k2401b 모델과 ma16k2401c 모델도 내려받을 수 있습니다. 세 모델이 디코더는
동일한 구조인데, 인코더만 각각 트랜스포머, 컨포머, 이브랜치포머 입니다.


`git lfs` 가 필요합니다.

        conda install git-lfs
        git lfs install

Download models from huggingface

        cd ~/a1003/local
        mkdir -p models
        cd models
        git clone https://hf.co/pkyoung/ma16k2401a
        git clone https://hf.co/pkyoung/ma16k2401b
        git clone https://hf.co/pkyoung/ma16k2401c


내려받은 모델의 구조를 확인해봅니다.

        ls -lh ma16k2401a/

## Run inference

`espnet-infer.sh` 파일을 열어서 필요한 설정을 변경하고 저장한 후 실행합니다.

        cd ~/a1003/local
        bash espnet-infer.sh

`$odir`에 저장된 결과 파일을 살펴봅니다. 예를 들어 `odir=results`라고 설정한
경우, `results/1best_recog/text` 파일에 인식결과가 기록됩니다.

## 음성인식 오류율 측정

발화별 CER과 평균 CER을 계산합니다.

`data/a1003/result_espnet_ma16k2401a.txt` 파일에 `ma16k2401a` 모델로 인식을
수행한 결과를 저장해 두었습니다. 인식을 모두 수행하지 않은 경우라면 이 파일을
사용해서 오류율을 측정해봅니다.

* 수행결과 사용

        cd ~/a1003/local
        cp results/1best_recog/text ./result.txt

* 저장된 결과 사용

        cd ~/a1003/local
        cp data/a1003/result_espnet_ma16k2401a.txt ./result.txt

* 음절 오류율 측정

        python uttcer.py data/a1003/text result.txt

* 화자별 오류율을 측정할 수 있습니다.

        for s in spk{1..9}; do
          echo -n "$s " >&2
          python uttcer.py data/a1003/text <(grep "$s/" result.txt) > /dev/null
        done

평균오류율이 높은 화자에 대해서는 몇몇 파일을 들어봅니다.

* 문장부호를 제외한 오류율을 측정해봅니다.


        python uttwer.py \
          <(python pp.py -s data/a1003/text) \
          <(python pp.py -s result.txt) > /dev/null


## ESPnet 모델별 음성인식 성능 및 속도

각 모델별 모델크기, 인식 소요 시간 및 인식 성능은 다음 표와 같습니다.
인식소요시간 및 인식성능은 환경에 따라 달라질 수 있습니다. (WER1, CER1: 문장부호 제외 전/WER2, CER2: 문장부호 제외 후)

| Model          | Size | Elapsed | RTF | WER1  |  CER1 | WER2  | CER2 |
| ---            | ---  | ---     | --- | ---   |  ---  |  ---  | ---  |
| ma16k2401a     | 280M | 4m8s    |0.15 | 28.20 | 10.09 | 20.10 | 7.36 |
| ma16k2401b     | 425M | 4m5s    |0.15 | 28.37 |  9.79 | 19.55 | 6.95 |
| ma16k2401c     | 550M | 4m21s   |0.16 | 26.44 |  8.89 | 17.45 | 5.88 |


