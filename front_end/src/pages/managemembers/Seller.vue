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
              <a-upload
                v-model="fileList"
                name="avatar"
                list-type="picture-card"
                class="avatar-uploader"
                :show-upload-list="false"
                action="https://www.mocky.io/v2/5cc8019d300000980a055e76"
                :before-upload="beforeUpload"
                @change="handleChange"
              >
                <img v-if="imageUrl" :src="imageUrl" alt="avatar" />
                <div v-else>
                  <!-- todo -->
                  <loading-outlined v-if="loading" />
                  <plus-outlined v-else />
                  <div class="ant-upload-text">Upload</div>
                </div>
              </a-upload>
              <p class="explanation">
                셀러 프로필 확장자는 jpg, jpeg, png 만 가능하며, 허용 가능한
                최대 파일사이즈 크기는 5MB 입니다.
              </p>
            </td>
          </tr>
          <tr>
            <th>셀러 상태</th>
            <td>{{ shop_status }}</td>
          </tr>
          <tr>
            <th>셀러 속성</th>
            <td>{{ seller_category_id }}</td>
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
            <td>{{ seller_name_ko }}</td>
          </tr>
          <tr>
            <th>셀러 영문명</th>
            <td>{{ seller_name_en }}</td>
          </tr>
          <tr>
            <th>셀러 계정</th>
            <td>{{ account }}</td>
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

import { Upload } from 'ant-design-vue';
import { PlusOutlined, LoadingOutlined } from '@ant-design/icons-vue';
import 'ant-design-vue/dist/antd.less';
import { message } from 'ant-design-vue';
function getBase64(img, callback) {
  const reader = new FileReader();
  reader.addEventListener('load', () => callback(reader.result));
  reader.readAsDataURL(img);
}

export default {
  name: 'Seller',
  inject: ['sellerData'],
  props: ['sellerId'],
  components: {
    'a-upload': Upload,
    PlusOutlined,
    LoadingOutlined,
    PageHeading,
    PageBar,
    PageSection
  },
  data() {
    return {
      seller_id: '',
      account: '',
      seller_name_en: '',
      seller_name_ko: '',
      manager_name: '',
      shop_status: '',
      manager_mobile: '',
      manager_email: '',
      seller_category_id: '',
      created_at: '',
      fileList: [],
      loading: false,
      imageUrl: ''
    };
  },
  created() {
    const { sellerData, sellerId } = this;
    const selectedSeller = sellerData.find(
      (seller) => seller.seller_id == sellerId
    );
    this.seller_id = selectedSeller.seller_id;
    this.account = selectedSeller.account;
    this.seller_name_en = selectedSeller.seller_name_en;
    this.seller_name_ko = selectedSeller.seller_name_ko;
    this.manager_name = selectedSeller.manager_name;
    this.shop_status = selectedSeller.shop_status;
    this.manager_mobile = selectedSeller.manager_mobile;
    this.manager_email = selectedSeller.manager_email;
    this.seller_category_id = selectedSeller.seller_category_id;
    this.created_at = selectedSeller.created_at;
  },
  methods: {
    // 이미지 업로드 ant design 컴포넌트 관련 함수
    handleChange(info) {
      if (info.file.status === 'uploading') {
        this.loading = true;
        return;
      }
      if (info.file.status === 'done') {
        // Get this url from response in real world.
        getBase64(info.file.originFileObj, (response) => {
          console.log(info.file.originFileObj);
          console.log(response);
          this.imageUrl = response;
          this.loading = false;
        });
      }
      if (info.file.status === 'error') {
        this.loading = false;
      }
    },
    beforeUpload(file) {
      const isJpgOrPng =
        file.type === 'image/jpeg' || file.type === 'image/png';
      if (!isJpgOrPng) {
        message.error('You can only upload JPG file!');
      }
      const isLt5M = file.size / 1024 / 1024 < 5;
      if (!isLt5M) {
        message.error('허용 가능한 최대 파일사이즈 크기는 5MB 입니다.');
      }
      return isJpgOrPng && isLt5M;
    }
  },
  beforeUpdate() {
    console.log(this.fileList);
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
  .avatar-uploader > .ant-upload {
    width: 128px;
    height: 128px;
  }
  .ant-upload-select-picture-card {
    // width: 128px;
    // height: 128px;
    i {
      font-size: 32px;
      color: #999;
    }
  }

  .ant-upload-select-picture-card .ant-upload-text {
    margin-top: 8px;
    color: #666;
  }
}

.container {
  min-height: 100px;
  width: 100%;
  background: #eee;
}
</style>
