# X Publishing Media Library

X(@SinaBroys) / Buffer·Grok Bot을 위한 공개 이미지·영상 보관함입니다.

## 현재 상태

- 2026년 11월 인사이트 시리즈 이미지 **21장**을 업로드할 수 있도록 준비했습니다.
- **주의: 이 패키지의 PNG 21장은 모두 _preview_ 버전**입니다. 실제 Pretendard 적용본으로 확정된 이미지가 아니므로, 원문과 폰트·문구 검수 전에 자동 게시하지 마세요.
- 최종 검수한 PNG는 기존 preview 파일을 덮어쓰지 말고 `_final.png` 신규 파일명으로 저장하세요. 예약에 사용한 URL 파일은 수정·이동·삭제하지 않습니다.
- `media/videos/`는 향후 MP4용입니다. Git 대용량 파일 저장소는 피하고, 큰 영상은 전용 스토리지 사용을 권장합니다.

## Buffer가 사용할 공개 URL

저장소가 GitHub 계정 `<OWNER>` 아래 `x-publishing-media` 이름으로 공개 생성되고 파일을 push한 다음 다음 주소를 사용합니다.

```
https://raw.githubusercontent.com/<OWNER>/x-publishing-media/main/media/images/2026-11/01_fondo_preview.png
```

`<OWNER>`는 실제 GitHub 로그인 이름으로 바꿉니다. GitHub 웹페이지 `.../blob/main/...` URL은 **원본 이미지 URL이 아니므로** Buffer 미디어 첨부에 넣지 마세요.

추가로 GitHub Pages를 Settings → Pages → Deploy from a branch → `main` / `(root)`로 활성화하면:

```
https://<OWNER>.github.io/x-publishing-media/media/images/2026-11/01_fondo_preview.png
```

이 주소는 Pages가 실제 배포된 뒤에만 사용할 수 있습니다.

## 버퍼 게시 전 체크

1. 원문과 이미지 1:1 매칭, 실제 Pretendard 적용 여부, 문구/출처, 업로드 권한 검토
2. 공개 주소를 로그아웃한 시크릿 창에서 열어 실제 PNG 파일이 직접 표시되는지 확인
3. Buffer의 이미지 필드에 URL을 넣어 미리보기/예약 등록 여부 확인
4. 게시가 끝날 때까지 같은 URL을 보존하고, 게시물 ID와 발행 결과 별도 확인
5. 이미지 크기: X용 이미지 5 MB 이하 권장 (현재 모든 PNG 5MB 이하, 상세 manifest.json 확인)

## 업로드 방법

### GitHub CLI 사용 (WSL 권장)

아래 스크립트는 **사용자가 실행하고 확인해야** 공개 저장소를 만듭니다.

```
bash setup_repo.sh
```

스크립트는 로그인 계정, 저장소 이름, 공개 상태를 보여주고 확인을 받아 진행합니다.

### GitHub 웹 사용

1. https://github.com/new 에서 `x-publishing-media`라는 **Public** 저장소를 만듭니다 (README 자동 생성은 해제)
2. `git clone`한 뒤 이 디렉터리의 내용을 복사하고 `git add/commit/push`하거나 GitHub의 Upload files로 필요한 파일을 올립니다.
3. `manifest.json`과 `index.html`도 업로드하면 검색·미리보기로 편리합니다.

## 저작권과 공개 주의

공개 저장소에 올리는 모든 미디어는 누구나 접근할 수 있습니다. 미공개 콘텐츠, 고객 사진, 개인정보, 저작권 미확인 소스는 올리지 않습니다. 콘셉트 사진은 기업의 실제 촬영자료가 아닙니다.
