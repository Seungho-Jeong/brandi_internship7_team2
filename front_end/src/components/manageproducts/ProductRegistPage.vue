<template>
<div>
     <PageHeading heading="셀러 계정 관리" subHeading="셀러 회원 목록 / 관리" />
    <PageBar
      class="page-bar"
      page="account"
      menuLevel1="회원 관리"
      menuLevel2="셀러 계정 관리"
      menuLevel3="셀러 회원 리스트"
    />
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
              :key="seller.seller_id"
              :id="seller.seller_id"
            >
              <th>
                {{th}}
              </th>
              <td>
                  <input placeholder={{placeholder}} disabled value={{value}}/>
                  <button></button>
            </td>
              <td>
                <router-link
                  :to="`/seller/seller_my_page/${seller.seller_id}`"
                  class="seller-link"
                  >{{ seller.account }}</router-link
                >
              </td>
              <td>{{ seller.seller_name_en }}</td>
              <td>{{ seller.seller_name_ko }}</td>
              <td>{{ seller.manager_name }}</td>
              <td>{{ seller.shop_status }}</td>
              <td>{{ seller.manager_mobile }}</td>
              <td>{{ seller.manager_email }}</td>
              <td>{{ seller.seller_type }}</td>
              <td>{{ seller.created_at }}</td>
              <td>
                <button
                  class="action"
                  :class="`type${action.key}`"
                  v-for="action in seller.actions"
                  :key="action.key"
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
      </div>
</template>

<script>
export default {
    data(){
        
        registTable1 : [
             {thead : "기본 정보"},
             {type: "", th: "셀러선택", td: [] },
             {type: "radio", th: "판매여부", td: [] },
             {type: "", th: "진열여부", td: [] },
             {type: "", th: "카테고리", td: [] },
             {type: "", th: "상품 정보 고시", td: [] },
             {type: "", th: "상품명", td: [] },
             {type: "", th: "한줄 상품 설명", td: [] },
             {type: "", th: "이미지 등록", td: [] },
             {type: "", th: "연령필터", td: [] },
             {type: "", th: "상세 상품 정보", td: [] },
             {type: "", th: "유튜브 영상 URL", td: [] },
        ],
        registTable2 : [
             {thead : "태거 정보"},
             {type: "", th: "색상필터(썸네일 이미지)", td: [] },
             {type: "", th: "스타일필터", td: [] },
             {type: "", th: "상품 태그/속성 관리", td: [] },
        ],
        registTable3 : [
             {thead : "옵션 정보"},
             {type: "", th: "옵션 설정", td: [] },
             {type: "", th: "옵션 정보", td: [] },
             {type: "", th: "", td: [] },
        ],
        registTable4 : [
             {thead : "판매 정보"},
             {type: "", th: "도매 원가", td: [] },
             {type: "", th: "판매가", td: [] },
             {type: "", th: "할인정보", td: [] },
             {type: "", th: "최소판매수량", td: [] },
             {type: "", th: "최대판매수량", td: [] },
             {type: "", th: "안전인증정보", td: [] },
        ],
             registTable5 : [
             {thead : "도매 정보"},
             {type: "", th: "도매처 명", td: [] },
             {type: "", th: "도매처 전화번호", td: [] },
             {type: "", th: "도매처 휴대전화번호", td: [] },
             {type: "", th: "도매처 위치", td: [] },
             {type: "", th: "도매 상품명", td: [] },
        ],
         registTable6 : [
             {thead : "코디 상품"},
             {type: "", th: "코디 상품 사용 여부", td: [] },
         ]
    }
    
}
</script>