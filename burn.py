"""手元の動画ファイルに、Lyric Overlay で書き出した ASS/SRT 歌詞を焼き込む。

使い方:
    python burn.py 動画.mp4 歌詞.ass [出力.mp4]

前提: ffmpeg が PATH にあること（未導入なら: winget install Gyan.FFmpeg）
"""
import os
import shutil
import subprocess
import sys
import tempfile


def main() -> None:
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    video, subs = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    out = os.path.abspath(sys.argv[3]) if len(sys.argv) > 3 else os.path.splitext(video)[0] + "_lyrics.mp4"

    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg が見つかりません。`winget install Gyan.FFmpeg` で導入後、ターミナルを開き直してください。")

    # ffmpeg の subtitles/ass フィルタは Windows パス (C:\...) のエスケープが面倒なので、
    # 字幕を一時フォルダへコピーし、そこを作業ディレクトリにして相対名で渡す
    ext = os.path.splitext(subs)[1].lower()
    with tempfile.TemporaryDirectory() as tmp:
        local = "subs" + ext
        shutil.copy(subs, os.path.join(tmp, local))
        vf = f"ass={local}" if ext == ".ass" else f"subtitles={local}"
        cmd = ["ffmpeg", "-y", "-i", video, "-vf", vf,
               "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "copy", out]
        print(" ".join(cmd))
        subprocess.run(cmd, cwd=tmp, check=True)
    print("完成:", out)


if __name__ == "__main__":
    main()
