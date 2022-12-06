package rig.sqlms.controller;

import org.junit.jupiter.api.Test;
import org.skyscreamer.jsonassert.JSONAssert;
import rig.sqlms.BaseIntegrationTest;

import static org.skyscreamer.jsonassert.JSONCompareMode.STRICT;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

class DataSourceControllerIntegrationTest extends BaseIntegrationTest {

    @Test
    void findAll_shouldReturnDataSourcesWithoutSensitiveData() throws Exception {
        String responseBody = mockMvc.perform(get("/datasources"))
                .andExpect(status().isOk())
                .andReturn().getResponse().getContentAsString();

        JSONAssert.assertEquals("""
                [
                  {
                    "name": "crm",
                    "jdbcUrl": "jdbc:h2:mem:crm-db;DATABASE_TO_UPPER=false",
                    "username": "crm-user",
                    "driverClassName": "org.h2.Driver"
                  },
                  {
                    "name": "debt",
                    "jdbcUrl": "jdbc:h2:mem:debt-db;DATABASE_TO_UPPER=false",
                    "username": "debt-user",
                    "driverClassName": "org.h2.Driver"
                  }
                ]
                """, responseBody, STRICT);
    }
}
