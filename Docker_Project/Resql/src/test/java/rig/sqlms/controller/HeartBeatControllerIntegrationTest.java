package rig.sqlms.controller;

import org.junit.jupiter.api.Test;
import org.skyscreamer.jsonassert.JSONAssert;
import rig.sqlms.BaseIntegrationTest;

import static org.skyscreamer.jsonassert.JSONCompareMode.LENIENT;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

class HeartBeatControllerIntegrationTest extends BaseIntegrationTest {

    @Test
    void get_shouldReturnApplicationInformation() throws Exception {
        String responseBody = mockMvc.perform(get("/healthz"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.appStartTime").exists())
                .andExpect(jsonPath("$.serverTime").exists())
                .andReturn().getResponse().getContentAsString();

        JSONAssert.assertEquals("""
                {
                  "appName": "rig-sqlms",
                  "version": "1.0",
                  "packagingTime": 1590762565458
                }
                """, responseBody, LENIENT);
    }

}
