# ChatChecker

## Description
채팅체로 쓰여진 한국어 문장을 문법에 맞는 문장으로 바꾸어주는 모듈입니다. Seq2Seq로 구현한 자체 모델과 Edit Distance를 활용해 교정 단어를 찾습니다.

## Functions
### Input: sentence
문장을 input으로 넣으면, 문장에서 표기 오류가 있는 단어를 찾아 교정 후 교정된 전체 문장을 return합니다.
- model_only(input):
  - 모델 예측 결과로만 문장을 교정합니다.
- both(input):
  - 자체 rule에 따라 모델, Edit Distance를 모두 활용해 문장을 교정합니다.
  - Edit Distance의 경우 동일한 거리를 갖는 모든 단어를 리스트로 return합니다.

### Input: word
표기 오류가 있는 단어를 input으로 넣으면, 모델과 edit distance가 예측한 교정 단어를 return합니다.
- model_only_word(input):
  - 모델 예측 결과 단어를 교정합니다.
- edit_only_word(input):
  - Edit Distance로 단어를 교정합니다.
- both_word(input):
  - 두 경우 모두의 output을 return합니다.
