# -*- coding: utf-8 -*-
from pathlib import Path
from datetime import datetime

def main():
    template_path = Path("template.html")
    if not template_path.exists():
        raise FileNotFoundError("template.html 파일이 없습니다. 저장소 최상위에 template.html을 먼저 생성해주세요.")

    html = template_path.read_text(encoding="utf-8")
    Path("index.html").write_text(html, encoding="utf-8")
    print("index.html 생성 완료:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    main()
