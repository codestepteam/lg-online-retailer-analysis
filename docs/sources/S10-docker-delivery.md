# S10 — 운영 Docker 이미지 v1.9.28 및 배포 키트 파일 목록

다운로드일: 2026-09-25. 원본 7개는 [전달본 폴더](<../../관련문서/운영 Docker 이미지(v1.9.28) 및 배포 키트/>)에 있다.

- [메일 출처·파일 크기·SHA-256](<../../관련문서/운영 Docker 이미지(v1.9.28) 및 배포 키트/다운로드-목록.json>)
- [API 이미지 메타데이터·선택 파일 목록과 레이어 출처](../../data/docker-inspection/v1.9.28/api/inventory.json)
- [Airflow 이미지 메타데이터·선택 파일 목록과 레이어 출처](../../data/docker-inspection/v1.9.28/airflow/inventory.json)
- [Airflow 컴파일 모듈의 추출 문자열 목록](../../data/docker-inspection/v1.9.28/airflow/strings/manifest.json)

이미지의 `/opt/project`, `/opt/airflow/dags`, `/app` 아래 일반 파일만 선택 추출했다. 심볼릭 링크를 따라가지 않았고 실행하지 않았다. 이미지 태그는 `lge-hs-clinic/api:v1.9.28`, `lge-hs-clinic/airflow:v1.9.28`, OS/architecture는 둘 다 `linux/amd64`다. 선택된 파일 수는 API 362개, Airflow 369개다.

문자열 추출은 ELF `.rodata`의 UTF-8 상수만 담는다. 원본 바이트 위치를 보존하며 복원된 소스코드 또는 함수 호출 검증이 아니다. 이미지 내부 값의 전체 의미를 해석한 문서는 [배포 자료·BCP 검토](../DOCKER_DELIVERY_REVIEW.md)에 따로 둔다.

대표 첨부 `clinic-collect-judge.md/html`은 전달된 AI 분석 문서다. 함수 호출로 확인했다는 문서 자체의 주장을 이번 작업에서 재실행·검증한 것으로 취급하지 않는다. 기존 `sources/manifest.json`은 최초 문서 8개용이며 S10은 위 별도 manifest로 관리한다.
