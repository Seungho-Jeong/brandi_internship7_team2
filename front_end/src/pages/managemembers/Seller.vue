<template>
  <main>
    <PageHeading
      class="page-heading"
      heading="셀러정보 수정페이지"
      subHeading="셀러 정보 조회 / 수정"
    />
    <PageBar
      class="page-bar"
      page="account"
      menuLevel1="회원 관리"
      menuLevel2="셀러 계정 관리"
      menuLevel3="셀러 정보 조회 / 수정"
    />
    <PageSection icon="user" sectionTitle="기본 정보">
      <table>
        <tbody>
          <tr>
            <th>셀러 프로필</th>
            <td>
              <p class="explanation">
                셀러 프로필 확장자는 jpg, jpeg, png 만 가능하며, 허용 가능한
                최대 파일사이즈 크기는 5MB 입니다.
              </p>
            </td>
          </tr>
          <tr>
            <th>셀러 상태</th>
            <td>ㅇ</td>
          </tr>
          <tr>
            <th>셀러 속성</th>
            <td>ㅇ</td>
          </tr>
          <tr>
            <td class="explanation" colspan="2">
              셀러명(한글, 영문) 변경시 셀러명과 동일하게 등록된 브랜드 정보는
              자동으로 변경되지 않습니다. 관리자께서는 이점 유의해주시기 바라며,
              브랜드 정보 수정은 [이전 버전 관리 > 브랜드관리] 에서 가능합니다.
            </td>
          </tr>
          <tr>
            <th>셀러 한글명</th>
            <td>ㅇ</td>
          </tr>
          <tr>
            <th>셀러 영문명</th>
            <td>ㅇ</td>
          </tr>
          <tr>
            <th>셀러 계정</th>
            <td>ㅇ</td>
          </tr>
        </tbody>
      </table>
    </PageSection>
    <PageSection icon="user" sectionTitle="상세 정보">
      <table>
        <tbody>
          <tr>
            <th>셀러페이지 배경이미지</th>
            <td>
              <p class="explanation">
                브랜디 앱과 웹 사이트의 셀러 페이지에 보여질
                배경이미지입니다.<br />
                배경이미지는 1200 * 850 사이즈 이상으로 등록해주세요.<br />확장자는
                jpg, jpeg, png 만 가능하며, 허용 가능한 최대 파일사이즈 크기는
                5MB 입니다.
              </p>
            </td>
          </tr>
          <tr>
            <th>셀러 한줄소개</th>
            <td>ㅇ</td>
          </tr>
          <tr>
            <th>셀러 상세소개</th>
            <td>
              <p>셀러 상세 소개 글은 최소10자 이상 입니다.</p>
            </td>
          </tr>
          <tr>
            <th>담당자 정보</th>
            <td>ㅇ</td>
          </tr>
          <tr>
            <th>고객센터</th>
            <td>ㅇ</td>
          </tr>
          <tr>
            <th>고객센터 운영시간 (주중)</th>
            <td>ㅇ</td>
          </tr>
        </tbody>
      </table>
    </PageSection>
    <PageSection icon="user" sectionTitle="수수료">
      <div class="container"></div>
    </PageSection>
    <PageSection icon="user" sectionTitle="배송정보 및 교환/환불 정보">
      <table>
        <tbody>
          <tr>
            <th>배송 정보</th>
            <td>
              <p class="explanation">문장이 끝나면 엔터로 줄바꿈을 해주세요.</p>
            </td>
          </tr>
          <tr>
            <th>교환/환불 정보</th>
            <td>
              <p class="explanation">문장이 끝나면 엔터로 줄바꿈을 해주세요.</p>
            </td>
          </tr>
        </tbody>
      </table>
    </PageSection>
  </main>
</template>
<script>
import PageHeading from '../../components/reusables/PageHeading.vue';
import PageBar from '../../components/reusables/PageBar.vue';
import PageSection from '../../components/reusables/PageSection.vue';

export default {
  name: 'Seller',
  components: {
    PageHeading,
    PageBar,
    PageSection
  }
};
</script>

<style lang="scss" scoped>
table {
  width: 100%;
  tbody {
    tr {
      min-height: 40px;
      &:nth-child(odd) {
        background: #eee;
      }
    }
    th,
    td {
      font-size: 13px;
      font-weight: 400;
      text-align: left;
      vertical-align: middle;
      padding: 10px;
      border: 0.5px solid #ddd;
    }
    th {
      width: 22%;
      background: #555;
      color: #fff;
    }
    .explanation {
      color: #1f91ff;
    }
  }
}

.container {
  min-height: 100px;
  width: 100%;
  background: #eee;
}
</style>
