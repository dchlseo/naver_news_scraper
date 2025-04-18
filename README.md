
# Naver News Scraper (네이버 뉴스 스크래퍼)

네이버 오픈 API를 활용해 특정 검색어에 대한 뉴스 기사 목록을 날짜 범위 기준으로 수집하고, CSV 파일로 저장하는 Python 스크립트입니다.  
검색어 하이라이트(`<b></b>`)를 기반으로 키워드도 추출하며, 날짜 기반 파생 변수(`year`, `month`, `ym`, `yq`)도 포함됩니다.

---

## 주요 기능

- 네이버 뉴스 검색 API (JSON) 사용
- 검색어, 시작일, 종료일 설정 가능 (`YYYYMMDD` 형식)
- 최대 1000건까지 자동 페이지네이션 (`display=100`)
- 기사 본문에서 `<b>` 태그로 강조된 키워드 자동 추출
- 날짜별로 `year`, `month`, `ym (년월)`, `yq (분기)` 파생 칼럼 생성
- 결과를 CSV 파일로 저장

---

## 사용 방법

### 1. 필요 패키지 설치

```bash
pip install pandas
```

### 2. API 키 입력

파일 하단의 아래 부분에 본인의 NAVER API 키를 입력하세요.

```python
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
```

### 3. 실행

```bash
python naver_news_scraper.py --query "야놀자리서치" --start_date 20240101 --end_date 20240415
```

### ⚙️ 인자 설명

| 인자 | 설명 | 예시 |
|------|------|------|
| `--query` | 검색할 키워드 | `"야놀자"`, `"야놀자리서치"` |
| `--start_date` | 수집 시작일 (`YYYYMMDD`) | `20240101` |
| `--end_date` | 수집 종료일 (`YYYYMMDD`) | `20240415` |

> ※ 인자를 생략하면 다음 기본값이 적용됩니다:
> - `query = "야놀자리서치"`
> - `start_date = 20230101`
> - `end_date = 오늘 날짜`

---

## 출력 파일

스크립트 실행 후, 다음 형식의 파일이 생성됩니다:

```
naver_news_RESULTS_야놀자리서치_20240101_20240415.csv
```

### CSV 파일 구조

| year | month | ym | yq | Date | SearchDate | Keyword | Title | Desc | Link | Original |
|------|--------|----|----|-------|-------------|---------|--------|------|------|----------|
| 202치
```

---

## 작성자

- Yanolja Research
- Made by: SDC
