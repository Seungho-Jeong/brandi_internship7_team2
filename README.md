# BRANDI Admin
7차 인턴십 2팀이 진행한 관리자/판매자가 사용하는 실제 서비스를 클론한 프로젝트입니다.

## Features
- 판매자 등록신청 및 상태변경(입점 승인, 거절 등) 기능
- 판매자 상세 정보(유형, 상태, 주소, 배송지, 담당자 등) 제공
- 상품 등록, 수정, 삭제 기능 및 상품, 상품 카테고리 조회 기능
- 상품 등록 시 옵션(상품옵션, 최소/최대 발주수량, 할인적용 등) 등록 기능

## Tech Stack

### Back end
- **DB : MySQL + AWS S3**
- **RESTful API로 설계**
- API: Flask
- API 언어 : Python 3.7
- Library
  - Bcrypt
  - PyJWT
  - PyMySQL

### Front end
- **Webpack Build**
- **UI 언어 : Vue**
- **UI 라이브러리 : MeterialUI or Vuetify 등**
- 스타일 시트 : CSS or SCSS 등

### Tools
- Pycharm
- Workbench
- Postman
- Httpie

## Commit rules
- 1 Commit/day
  - 기능 단위 Commit (1일 초과 작업 시에는 끊어서 Commit 무관)
- Commit format

    ```
    [상위메뉴 > 하위메뉴]
    - 구현 내용을 구체적으로 적는다. 
    - 구현 내용을 구체적으로 적는다. 

    [구현명]
    - 구현 내용을 구체적으로 적는다. 
    - 구현 내용을 구체적으로 적는다. 
    ```
## Contributor

### Back-end(2명)
- 정승호
- 김형욱

### Front-end(2명)
- 이동훈
- 
