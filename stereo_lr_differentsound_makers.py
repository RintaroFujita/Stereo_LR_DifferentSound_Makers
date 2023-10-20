import os
import random
from pydub import AudioSegment

# ランダムに2つの音声ファイルを選択するディレクトリを指定
input_dir = '/content/drive/MyDrive/finrand/finland_cut'  # 入力ディレクトリを指定
output_dir = '/content/drive/MyDrive/finrand/finLR_5sec'  # 出力ディレクトリを指定

# 出力ディレクトリが存在しない場合は作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 2つの音声ファイルをランダムに選び、左右別々の音声を生成して保存
total_files = 1500  # 生成するファイルの総数を指定

for i in range(total_files):
    # ランダムに2つの音声ファイルを選択
    selected_files = random.sample(os.listdir(input_dir), 2)

    # 選ばれたファイルのパスを生成
    sound1_path = os.path.join(input_dir, selected_files[0])
    sound2_path = os.path.join(input_dir, selected_files[1])

    # 2つの音声ファイルを読み込む
    sound1 = AudioSegment.from_file(sound1_path)
    sound2 = AudioSegment.from_file(sound2_path)

    # 音声ファイルの長さを同じに調整
    duration = max(len(sound1), len(sound2))

    if len(sound1) < duration:
        silence1 = AudioSegment.silent(duration - len(sound1))
        sound1 = sound1 + silence1

    if len(sound2) < duration:
        silence2 = AudioSegment.silent(duration - len(sound2))
        sound2 = sound2 + silence2

    # ステレオに変換
    sound1 = sound1.set_channels(2)
    sound2 = sound2.set_channels(2)

    # 左右チャネルに音声を配置
    stereo_sound = sound1.pan(-1).overlay(sound2.pan(1))

    # 出力ファイル名を生成
    output_file = os.path.join(output_dir, f'stereo_audio_{i + 1}.wav')

    if os.path.exists(output_file):
        base, ext = os.path.splitext(output_file)
        output_file = f'{base}_{i + 1}{ext}'

    # 生成された音声を保存
    stereo_sound.export(output_file, format="wav")

print(f"{total_files} 個のファイルを生成しました。")