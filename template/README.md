# 공통 상세페이지 템플릿

Figma 「상세페이지 작업」의 1200px 상세페이지(참다랑어 v1 기준) 구조를 HTML로 옮긴 템플릿입니다.
제품마다 `data.json`과 이미지만 바꾸면 같은 레이아웃의 상세페이지가 만들어집니다.

## 구성

```
template/
  build.mjs              생성 스크립트 (의존성 없음, Node 18+)
  detail.css             공통 스타일 (Figma 1px = --u, 최대 폭 860px로 비율 축소)
  products/<id>/data.json  제품 데이터
  products/<id>/*.webp     제품 이미지
  <id>.html              생성 결과 (미리보기 겸 Cafe24 붙여넣기용)
```

## 사용법

```bash
node template/build.mjs          # 전체 제품 생성
node template/build.mjs maguro   # 한 제품만 생성
```

`template/maguro.html`을 브라우저로 열어 확인합니다.
Cafe24 상세설명에 넣을 때는 `<style>` 블록과 `OCEANPERU DETAIL START ~ END` 주석 사이를 복사하고,
이미지 경로(`products/<id>/...`)를 Cafe24 업로드 주소로 바꿉니다.

## 페이지 순서

1. 물결 + 로고 + 히어로(태그라인 · 강조 부제 · 제품명) + 대표 사진
2. CHECK POINT: 용도 카드 2장 + 01~03 포인트
3. Q 섹션: `sections` 배열 순서대로 Q1, Q2 … 번호가 자동으로 붙습니다.

## 섹션 type

| type | 용도 | 필드 |
|---|---|---|
| `parts` | 세부 사항·부위 구성 | `image`, `headline[]`, `body`, `partsTitle`, `parts[{name, sub?, image, desc}]` |
| `steps` | 사이즈·가공 단계 | `notice?`, `steps[{image, caption}]`, `footnote?` |
| `packaging` | 포장 | `mainImage`, `subImage`, `note`, `boxImage`, `items[]` |
| `notice` | 정보 고시 표 | `rows[[항목, 값]]` |

모든 섹션은 `question`(제목)과 선택 `bgWord`(배경 큰 글자: 숫자면 왼쪽 큰 숫자, 글자면 가운데 워드)를 가집니다.

## 새 제품 추가

1. `products/maguro` 폴더를 복사해 `products/<새 id>`로 이름을 바꿉니다.
2. `data.json`의 `id`와 문구, 이미지 파일명을 수정합니다. 필요 없는 섹션은 배열에서 빼면 됩니다.
3. `node template/build.mjs <새 id>` 실행.

## 이미지 안내

`products/maguro`의 이미지는 Figma 화면을 캡처해 만든 것입니다.
`detail-main`, `step-01`, `step-03`, `pack-01~03`은 해상도가 낮은 임시본이므로, 실제 사용 전 원본 사진으로 교체하십시오.
