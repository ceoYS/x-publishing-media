#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
REPO="x-publishing-media"
if ! command -v gh >/dev/null 2>&1; then
  echo 'GitHub CLI(gh)가 없습니다. https://cli.github.com/ 를 설치하거나 GitHub 웹으로 저장소를 만들어 주세요.'
  exit 2
fi
if ! command -v git >/dev/null 2>&1; then echo 'git이 필요합니다.'; exit 2; fi
if ! gh auth status >/dev/null 2>&1; then
  echo '로그인이 필요합니다: gh auth login'; exit 2
fi
OWNER="$(gh api user --jq .login)"
echo "계정: $OWNER"
echo "생성될 공개 저장소: https://github.com/$OWNER/$REPO"
echo '중요: 아래 PNG 21장은 preview이며, Pretendard 최종 파일이 아닙니다.'
read -r -p '이 계정에 PUBLIC 저장소를 만들고 21장 미리보기를 올릴까요? [yes/no] ' ANSWER
if [ "$ANSWER" != 'yes' ]; then echo '취소했습니다.'; exit 0; fi
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo '현재 폴더가 이미 git 저장소이므로 안전을 위해 중단합니다.'; exit 3
fi
if gh repo view "$OWNER/$REPO" >/dev/null 2>&1; then
  echo "동일 이름의 저장소가 이미 존재합니다: https://github.com/$OWNER/$REPO";exit 4
fi
git init -b main
git add README.md index.html manifest.json .nojekyll .gitignore setup_repo.sh media
git commit -m 'chore: initialize X media library with 21 preview cards'
gh repo create "$REPO" --public --source=. --remote=origin --push
echo "등록 요청 완료: https://github.com/$OWNER/$REPO"
echo "첫 이미지: https://raw.githubusercontent.com/$OWNER/$REPO/main/media/images/2026-11/01_fondo_preview.png"
echo '링크는 반드시 시크릿 창과 Buffer에서 재확인하세요.'
