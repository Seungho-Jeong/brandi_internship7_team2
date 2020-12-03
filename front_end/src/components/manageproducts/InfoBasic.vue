<template>
  <table>
    <thead>
      기본 정보
    </thead>

    <tbody>
      <tr>
        <th>셀러선택</th>
        <td>
          <SelectSeller></SelectSeller>
        </td>
      </tr>
      <tr>
        <th>판매여부</th>
        <td>
          <a-radio-group name="radioGroup" :default-value="1">
            <a-radio :value="1"> A </a-radio>
            <a-radio :value="2"> B </a-radio>
            <a-radio :value="3"> C </a-radio>
            <a-radio :value="4"> D </a-radio>
          </a-radio-group>
        </td>
      </tr>
      <tr>
        <th>진열여부</th>
        <td>
          <a-radio-group name="radioGroup" :default-value="1">
            <a-radio :value="1"> A </a-radio>
            <a-radio :value="2"> B </a-radio>
            <a-radio :value="3"> C </a-radio>
            <a-radio :value="4"> D </a-radio>
          </a-radio-group>
        </td>
      </tr>
      <tr>
        <th>카테고리</th>
        <td>
          <table>
            <thead>
              <tr>
                <th>1차 카테고리</th>
                <th>2차 카테고리</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>셀러를 먼저 선택해주세요.</td>
                <td>셀러를 먼저 선택해주세요.</td>
              </tr>
            </tbody>
          </table>
        </td>
      </tr>
      <tr>
        <th>상품 정보 고시</th>
        <td>
          <a-radio-group name="radioGroup" :default-value="1">
            <a-radio :value="1"> A </a-radio>
            <a-radio :value="2"> B </a-radio>
            <a-radio :value="3"> C </a-radio>
            <a-radio :value="4"> D </a-radio>
          </a-radio-group>
        </td>
      </tr>
      <tr>
        <th>상품명</th>
        <td>
          <a-input placeholder="Basic usage" />

          <p>상품명에는 쌍따옴표(")또는 홑따옴표(')를 포함할 수 없습니다.</p>
          <p>상품명에는 4byte 이모지를 포함할 수 없습니다.</p>
        </td>
      </tr>
      <tr>
        <th>한줄 상품 설명</th>
        <td>
          <a-input placeholder="Basic usage" />
        </td>
      </tr>
      <tr>
        <th>이미지 등록</th>
        <td>
          <Upload></Upload>
          <p>
            640*720 사이즈 이상 등록 가능하며 확장자는 jpg만 등록 가능합니다.
          </p>
        </td>
      </tr>
      <tr>
        <th>연령필터</th>
        <td></td>
      </tr>
      <tr>
        <th>상세 상품 정보</th>
        <td>
          <div>
            <a-radio-group name="radioGroup" :default-value="1">
              <a-radio :value="1"> A </a-radio>
              <a-radio :value="2"> B </a-radio>
              <a-radio :value="3"> C </a-radio>
              <a-radio :value="4"> D </a-radio>
            </a-radio-group>
            <InsertImage></InsertImage>
          </div>
        </td>
      </tr>
      <tr>
        <th>유튜브 영상 URL</th>
        <td>
          <a-input placeholder="Basic usage" />

          <a-button> <a-icon type="upload" /> upload </a-button>
          <p>
            https://www.youtube.com 또는 https://youtu.be로 시작하는 URL만 등록
            가능합니다.
          </p>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import SelectSeller from './PRcomponents/SelectSeller.vue';
import Upload from './PRcomponents/Upload.vue';
import InsertImage from './PRcomponents/InsertImage.vue';
export default {
  components: {
    SelectSeller,
    Upload,
    InsertImage
  },
  data() {
    return {};
  },
  methods: {}
};
</script>

<style lang="scss" scoped>
table,
td,
th {
  border: 1px solid #ddd;
}

table {
  thead {
    border-collapse: collapse;
    background: #eee;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
}
</style>
