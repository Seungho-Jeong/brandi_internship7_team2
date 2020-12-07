<template>
  <main>
    <PageHeading heading="셀러 계정 관리" subHeading="셀러 회원 목록 / 관리" />
    <PageBar
      class="page-bar"
      page="account"
      menuLevel1="회원 관리"
      menuLevel2="셀러 계정 관리"
      menuLevel3="셀러 회원 리스트"
    />
    <PageSection icon="list" sectionTitle="셀러 회원 리스트">
      <a-pagination
        class="pagination top"
        size="small"
        :total="sellerData.length"
        :show-total="(total) => `Total ${total} items`"
        :page-size-options="['10', '20', '50', '100', '150']"
        show-size-changer
      />
      <div class="table-container">
        <table>
          <thead>
            <tr class="table-header">
              <th class="header-checkbox">
                <input type="checkbox" name="sellerData" id="all" />
              </th>
              <th
                class="header-item"
                v-for="column in columns"
                :key="column.key"
              >
                <p>{{ column.title }}</p>
              </th>
            </tr>
            <tr class="data-filter">
              <th></th>
              <th
                class="filter-item"
                v-for="column in columns"
                :key="column.key"
              >
                <input
                  v-if="showFilterInput(column.key)"
                  class="filter-input"
                  type="search"
                  :id="column.key"
                />
                <select
                  v-if="showFilterDropdown(column.key)"
                  class="filter-dropdown"
                  :id="column.key"
                >
                  <option v-for="option in column.options" :key="option.key">
                    {{ option.label }}
                  </option>
                </select>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              class="data-row"
              v-for="seller in sellerData"
              :key="seller.id"
              :id="seller.id"
            >
              <td>
                <input type="checkbox" name="sellerData" :id="seller.id" />
              </td>
              <td>{{ seller.id }}</td>
              <td>
                <router-link
                  :to="{
                    name: 'Seller',
                    params: {
                      sellerId: seller.id
                    }
                  }"
                  class="seller-link"
                  >{{ seller.account }}</router-link
                >
              </td>
              <td>{{ seller.name_en }}</td>
              <td>{{ seller.name_ko }}</td>
              <td>{{ seller.manager_name }}</td>
              <td>{{ seller.shop_status_name }}</td>
              <td>{{ seller.manager_mobile }}</td>
              <td>{{ seller.manager_email }}</td>
              <td>{{ seller.category_name }}</td>
              <td>{{ seller.created_at }}</td>
              <td>
                <button
                  class="action"
                  :class="`type${action.key}`"
                  v-for="action in shopStatusActionMap[seller.shop_status_id]"
                  :key="action.key"
                  @click="updateShopStatus(action.key)"
                >
                  {{ action.label }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <a-pagination
        class="pagination bottom"
        size="small"
        :total="sellerData.length"
        :show-total="(total) => `Total ${total} items`"
        :page-size-options="['10', '20', '50', '100', '150']"
        show-size-changer
      />
    </PageSection>
  </main>
</template>

<script>
import { Pagination } from 'ant-design-vue';
import 'ant-design-vue/dist/antd.less';

import PageHeading from '../../components/reusables/PageHeading.vue';
import PageBar from '../../components/reusables/PageBar.vue';
import PageSection from '../../components/reusables/PageSection.vue';
import { SELLER_LIST } from '../../config.js';

export default {
  name: 'Account',
  inject: ['sellerData'],
  components: {
    'a-pagination': Pagination,
    PageHeading,
    PageBar,
    PageSection
  },
  data() {
    return {
      columns: [
        {
          title: '번호',
          dataIndex: 'seller_id',
          key: 'seller_id'
        },
        {
          title: '셀러아이디',
          dataIndex: 'account',
          key: 'account'
        },
        {
          title: '영문이름',
          dataIndex: 'seller_name_en',
          key: 'seller_name_en'
        },
        {
          title: '한글이름',
          dataIndex: 'seller_name_ko',
          key: 'seller_name_ko'
        },
        {
          title: '담당자이름',
          dataIndex: 'manager_name',
          key: 'manager_name'
        },
        {
          title: '셀러상태',
          dataIndex: 'shop_status',
          key: 'shop_status',
          options: [
            { key: 0, label: 'Select' },
            { key: 1, label: '입점대기' },
            { key: 2, label: '입점' },
            { key: 3, label: '퇴점' },
            { key: 4, label: '퇴점대기' },
            { key: 5, label: '휴점' }
          ]
        },
        {
          title: '담당자연락처',
          dataIndex: 'manager_mobile',
          key: 'manager_mobile'
        },
        {
          title: '담당지이메일',
          dataIndex: 'manager_email',
          key: 'manager_email'
        },
        {
          title: '셀러속성',
          dataIndex: 'seller_type',
          key: 'seller_type',
          options: [
            { key: 0, label: 'Select' },
            { key: 1, label: '쇼핑몰' },
            { key: 2, label: '마켓' },
            { key: 3, label: '로드샵' },
            { key: 4, label: '디자이너브랜드' },
            { key: 5, label: '제너럴브랜드' },
            { key: 6, label: '내셔널브랜드' },
            { key: 7, label: '뷰티' }
          ]
        },
        {
          title: '등록일시',
          dataIndex: 'created_at',
          key: 'created_at'
        },
        {
          title: 'Actions',
          key: 'actions',
          dataIndex: 'actions',
          slots: { customRender: 'actions' }
        }
      ],
      test: ['1', '2'],
      shopStatusActionMap: {
        1: [
          { key: 1, label: '입점 승인' },
          { key: 2, label: '입점 거절' }
        ],
        2: [
          { key: 3, label: '휴점 신청' },
          { key: 5, label: '퇴점 신청 처리' }
        ],
        3: [],
        4: [
          { key: 3, label: '휴점 신청' },
          { key: 6, label: '퇴점 확정 처리' },
          { key: 7, label: '퇴점 철회 처리' }
        ],
        5: [
          { key: 4, label: '휴점 해제' },
          { key: 5, label: '퇴점 신청 처리' }
        ]
      }
    };
  },
  methods: {
    showFilterInput(columnKey) {
      const filterInputKeyList = [
        'seller_id',
        'account',
        'seller_name_en',
        'seller_name_ko',
        'manager_name',
        'manager_mobile',
        'manager_email'
      ];
      return filterInputKeyList.includes(columnKey);
    },
    showFilterDropdown(columnKey) {
      const filterDropdownKeyList = ['shop_status', 'seller_type'];
      return filterDropdownKeyList.includes(columnKey);
    },
    async updateShopStatus(actionKey) {
      let newShopStatusId;
      let newShopStatusName;
      switch (actionKey) {
        case 1:
          newShopStatusId = 2;
          newShopStatusName = '입점';
          break;
        case 2:
          newShopStatusId = 3;
          newShopStatusName = '퇴점';
          break;
        case 3:
          newShopStatusId = 5;
          newShopStatusName = '휴점';
          break;
        case 4:
          newShopStatusId = 2;
          newShopStatusName = '입점';
          break;
        case 5:
          newShopStatusId = 4;
          newShopStatusName = '퇴점대기';
          break;
        case 6:
          newShopStatusId = 3;
          newShopStatusName = '퇴점';
          break;
        case 7:
          newShopStatusId = 2;
          newShopStatusName = '입점';
          break;
        default:
          console.log('shop status update error');
          break;
      }
      // const action = confirm(
      //   `셀러상태를 ${newShopStatusName}(으)로 변경하시겠습니까?`
      // );
      // if (action) {
      //   alert(`셀러상태가 ${newShopStatusName}(으)로 변경되었습니다.`);
      // }
      try {
        const res = await fetch(SELLER_LIST, {
          method: 'PUT',
          headers: {
            Authorization:
              'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50IjoibWFzdGVyMyIsImV4cCI6MTYwNzQwNTAzNH0.JiooF5kfRHafQdx2jtsw4AT7c0oujD0guyCXdLPmAxA',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            shop_status_id: newShopStatusId,
            shop_status_name: newShopStatusName
          })
        });
        const data = await res.json();
        if (data.message === 'success') {
          const action = confirm(
            `셀러상태를 ${newShopStatusName}(으)로 변경하시겠습니까?`
          );
          if (action) {
            alert(`셀러상태가 ${newShopStatusName}(으)로 변경되었습니다.`);
          }
        } else {
          alert('server message: FAIL');
        }
      } catch (err) {
        console.log(this.sellerData.shop_status_id);
        alert('PUT error: put request to server failed');
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.pagination {
  margin: 15px 0;
}

.table-container {
  overflow: auto;
}
table {
  border: 1px solid #ddd;
  border-collapse: collapse;

  thead,
  tbody {
    tr {
      height: 40px;
    }
    th,
    td {
      text-align: left;
      vertical-align: middle;
      white-space: nowrap;
      padding: 0 10px;
      border: 0.5px solid #ddd;
    }
    th {
      font-size: 14px;
    }
    td {
      font-size: 13px;
    }
  }

  tr.table-header {
    background: #555;
    color: white;

    th.header-item {
      p {
        font-weight: 200;
      }
    }
  }

  tr.data-filter {
    th.filter-item {
      .filter-input,
      .filter-dropdown {
        width: 100%;
        height: 30px;
        border: 1px solid #ddd;
        border-radius: 3px;
      }
    }
  }

  tr.data-row {
    &:nth-child(odd) {
      background: #eee;
    }
    .seller-link {
      color: #0d628f;
      &:hover {
        text-decoration: underline;
      }
    }

    button.action {
      font-size: 12px;
      color: #fff;
      border-radius: 3px;
      margin: 2px;
      padding: 4px 6px;
      cursor: pointer;
    }
    button.action.type1 {
      background: #5bc0de;
    }
    button.action.type2,
    .type5,
    .type6 {
      background: #d8534f;
    }
    button.action.type3 {
      background: #f0ad4e;
    }
    button.action.type4,
    .type7 {
      background: #5db85b;
    }
  }
}
</style>
