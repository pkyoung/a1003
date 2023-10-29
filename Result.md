# ASR Results with ESPnet

| exp-id | model  | train-db | token-type | ntoken | specaug | nepoch   | navidlg |
| ---    | ---    | ---      | ---        | ---    | ---     | ---      | ---     |
| exp01  | def-cf | 01       | char       | 1906   | O       | avg30-30 | 29.45   |
|        | def-tf | 01       | char       | 1906   | O       | avg30-10 |         |
|        | def-cf | 01,03,05 | bpe        | 5000   | O       | avg30-10 |         |
|        | def-tf | all      | char       | 1906   | O       | 100      |         |
